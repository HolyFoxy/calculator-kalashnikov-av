from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, World!")
    
    def do_POST(self):
        if '/calc' not in self.path:
            self.send_response(500)
            self.end_headers()
            return

        query_components = parse_qs(urlparse(self.path).query)
        is_float_mode = query_components.get("float", ["False"])[0].lower() == "true"
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        expression = data.get('expression')
        
        if expression is None:
            self.send_response(500)
            self.end_headers()
            return
        
        mode_flag = '--float' if is_float_mode else '--int'
        result = subprocess.run(["./build/app.exe", mode_flag, expression], text=True, capture_output=True)
        
        if result.returncode == 0:
            response = {"result": result.stdout.strip()}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(result.stderr.encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting http server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

