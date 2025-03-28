import sys
import requests
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

class CalculatorApp(QWidget):
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

    def calculate_expression(self):
        expression = self.expression_input.text()
        url1="http://192.168.43.110:8000/calc"
        url2="http://192.168.43.110:8000/calc?float=true"
        try:
            if self.float_mode_checkbox.isChecked():
                response=requests.post(url2,json={"expression": expression})
                response.raise_for_status()
                result=response.json().get("result")
            else:
                response=requests.post(url1,json={"expression": expression})
                response.raise_for_status()
                result=response.json().get("result")

            self.result_output.setText(f"Результат: {result}")
            self.history_output.append(f"{expression} = {result}")
            self.expression_input.clear()  # Очистить поле ввода после вычисления
        except Exception as e:
            self.result_output.setText(f"Ошибка: {str(e)}")
        #except requests.exceptions.RequestException as e:
        #    self.result_output.setText(f"Ошибка: {str(e)}")

    def clear_fields(self):
        self.expression_input.clear()
        self.result_output.setText("Результат: ")
        self.history_output.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())

