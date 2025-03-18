#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import subprocess
import structlog
from structlog.dev import set_exc_info, ConsoleRenderer
from structlog.processors import StackInfoRenderer, TimeStamper, add_log_level
import logging
import sys

# Настройка стандартного логгера
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

def config_structlog():
    structlog.configure_once(
        processors=[
            add_log_level,
            StackInfoRenderer(),
            set_exc_info,
            TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False),
            ConsoleRenderer(),
        ], 
	logger_factory=structlog.stdlib.LoggerFactory(), 
	cache_logger_on_first_use=True, 
    )

def config_JSON_logger(): 
    fileHandler = logging.FileHandler("1log. json") 
    fileFormatter = structlog.stdlib.ProcessorFormatter ( 
        processor=structlog.processors.JSONRenderer(),
	foreign_pre_chatn=[ 
	    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False), 
	    structlog.processors.StackInfoRenderer(), 
	    set_exc_info, 
	    add_log_level, 
	], 
    ) 
    fileHandler.setFormatter(fileFormatter) 
    logging.getLogger().addHandler(fileHandler)

# Вызов конфигурации логирования
config_structlog()
config_JSON_logger() 
# Создание логгера
logger = structlog.get_logger()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        name = query_components.get("name", ["world"])[0]
        logger.info("GET request received", path=self.path, name=name)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response_message = f"Hello, {name}!"
        self.wfile.write(response_message.encode())
        logger.info("Response sent", response=response_message)

    def do_POST(self):
        logger.info("POST request received", path=self.path)
        if '/calc' not in self.path:
            logger.error("Invalid request", path=self.path)
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
            logger.error("Bad request: missing expression")
            self.send_response(500)
            self.end_headers()
            return
        
        mode_flag = '--float' if is_float_mode else '--int'
        logger.info("Calculating expression", expression=expression, mode=mode_flag)
        result = subprocess.run("./../build/app.exe", mode_flag, input = expression, text=True, capture_output=True)
        
        if result.returncode == 0:
            response = {"result": result.stdout.strip()}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            logger.info("Calculation successful", result=response["result"])
        else:
            logger.error("Calculation failed", error=result.stderr)
            self.send_response(500)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info("Starting HTTP server", port=port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

