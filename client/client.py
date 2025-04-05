import sys
import requests
import socket
import json
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QTextEdit,
)
from PySide6.QtCore import (QObject, QThread, Signal, QTimer)

class CalculatorApp(QWidget):
    past_exp = ""
    url="http://localhost:8000/calc"
    his_url = "http://localhost:8000/history"
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        # Ввод арифметического выражения
        self.expression_input = QLineEdit()
        self.layout.addWidget(QLabel("Введите арифметическое выражение:"))
        self.layout.addWidget(self.expression_input)

        # Чекбокс для режима с плавающей точкой
        self.float_mode_checkbox = QCheckBox("Режим с плавающей точкой")
        self.layout.addWidget(self.float_mode_checkbox)

        # Кнопка посчитать
        self.calculate_button = QPushButton("Посчитать")
        self.calculate_button.clicked.connect(self.calculate_expression)
        self.layout.addWidget(self.calculate_button)

        # Кнопка очистить
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_fields)
        self.layout.addWidget(self.clear_button)

        # Окно для вывода результата
        self.result_output = QLabel("Результат: ")
        self.layout.addWidget(self.result_output)

        # Окно с историей вычислений
        self.history_output = QTextEdit()
        self.history_output.setReadOnly(True)
        self.layout.addWidget(QLabel("История вычислений:"))
        self.layout.addWidget(self.history_output)

        self.setLayout(self.layout)
        
        self.setup_socket_thread()
        self.load_history()

    def load_history(self):
        try:
            response = requests.get(self.his_url)
            for i in response.json():
                data = json.loads(i.replace('\'', '\"'))
                self.history_output.append(f'<<History>>: {data.get("expression")} = {data.get("result")}')
        except Exception as e:
            print ("failed uploading history: {str(e)}")

    def setup_socket_thread(self):
        self.socket_thread = QThread()
        self.socket_worker = SocketWorker()
        self.socket_worker.moveToThread(self.socket_thread)
        
        self.socket_thread.started.connect(self.socket_worker.listen)
        self.socket_worker.data_received.connect(self.handle_socket_data)
        
        self.socket_thread.start()


    def handle_socket_data(self, data):
        try:
            message = data.decode('utf-8')
            data_json = json.loads(message)
            print('msg', message)
            if (data_json.get("expression") != self.past_exp): 
                self.history_output.append(f'<<Online>>: {data_json.get("expression")} = {data_json.get("result")}')
            self.past_exp = ''
        except UnicodeDecodeError:
            print("Получены бинарные данные")

    def calculate_expression(self):
        expression = self.expression_input.text()
        self.past_exp = expression
        try:
            if self.float_mode_checkbox.isChecked():
                response=requests.post(self.url,json={"expression": expression, "is_float":True}, timeout=5)
                response.raise_for_status()
                result=response.json().get("result")
            else:
                response=requests.post(self.url,json={"expression": expression, "is_float":False}, timeout=5)
                response.raise_for_status()
                result=response.json().get("result")
            error = response.json().get("error")
            
            if (error == None):
                self.result_output.setText(f"Результат: {result}")
                self.history_output.append(f"{expression} = {result}")
                self.expression_input.clear()  # Очистить поле ввода после вычисления
            else:
                self.result_output.setText(f"Ошибка: {error}")
        except Exception as e:
            self.result_output.setText(f"Ошибка: {str(e)}")

    def clear_fields(self):
        self.expression_input.clear()
        self.result_output.setText("Результат: ")
        
class SocketWorker(QObject):
    data_received = Signal(bytes)
    def __init__(self):
        super().__init__()
        self._active = True
        self.host = "127.0.0.1"
        self.port = 8001
        self.socket = None
        self.connection_attempts = 0
        self.reconnect_interval = 5000
        self.current_time = 0


    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.host, self.port))
            self.connection_attempts = 0
            return True
        except Exception as e:
            return False


    def listen(self):
        while self._active:
            try:
                if self.socket is None and self.create_socket():
                    continue
                
                data = self.socket.recv(1024)
                if data:
                    self.data_received.emit(data)
                else:
                    raise ConnectionError("Соединение закрыто сервером")
                    
            except socket.timeout:
                continue
            except Exception as e:
                print('error while trying to connect to server...')
                self.try_reconnect()


    def try_reconnect(self):
        while self._active and not self.create_socket():
            self.current_time = 0
            self.connection_attempts += 1
            while self._active and self.current_time < self.reconnect_interval:
                time.sleep(0.050)
                self.current_time = self.current_time + 50
        
        return self.socket is not None


    def reconnect(self):
        while self.current_time < self.reconnect_interval:
            time.sleep(0.050)
            self.current_time = self.current_time + 50
        self.connection_attempts = self.connection_attempts + 1
    
    def stop(self):
        self._active = False
        if self.socket:
            self.socket.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())

