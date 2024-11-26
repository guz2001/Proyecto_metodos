import numpy as np
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox, QWidget, QTextEdit, QSpinBox
from decimal import Decimal, getcontext
getcontext().prec = 20

class CalculadoraIntegracionNumerica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Integración Numérica")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Entrada de la función
        self.label_function = QLabel("Ingrese la función a integrar (en x):")
        self.layout.addWidget(self.label_function)
        self.input_function = QLineEdit()
        self.layout.addWidget(self.input_function)

        # Intervalo [a, b]
        self.label_interval = QLabel("Intervalo [a, b]:")
        self.layout.addWidget(self.label_interval)
        self.input_a = QDoubleSpinBox()
        self.input_a.setRange(-1e6, 1e6)
        self.input_a.setDecimals(6)
        self.input_a.setValue(0.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_a)

        self.input_b = QDoubleSpinBox()
        self.input_b.setRange(-1e6, 1e6)
        self.input_b.setDecimals(6)
        self.input_b.setValue(1.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_b)

        # Número de subintervalos
        self.label_subintervals = QLabel("Número de subintervalos:")
        self.layout.addWidget(self.label_subintervals)
        self.input_subintervals = QSpinBox()
        self.input_subintervals.setRange(1, 1000)
        self.input_subintervals.setValue(10)  # Valor predeterminado
        self.layout.addWidget(self.input_subintervals)

        # Botón para calcular
        self.calculate_button = QPushButton("Calcular Integral")
        self.calculate_button.clicked.connect(self.calculate_integral)
        self.layout.addWidget(self.calculate_button)

        # Área de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def calculate_integral(self):
        # Obtener la función ingresada
        function_text = self.input_function.text()
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(function_text, transformations=transformations)
        except Exception as e:
            self.result_area.setText(f"Error en la función: {e}")
            return

        # Obtener el intervalo [a, b] y número de subintervalos
        a = self.input_a.value()
        b = self.input_b.value()
        n = self.input_subintervals.value()

        # Métodos de integración
        results = []

        # Método de Trapecio
        trapecio_result = self.trapecio(expr, a, b, n)
        results.append(f"Resultado de la integral usando el Método del Trapecio: {trapecio_result:.6f}")

        # Método de Simpson
        simpson_result = self.simpson(expr, a, b, n)
        results.append(f"Resultado de la integral usando el Método de Simpson: {simpson_result:.6f}")

        # Mostrar resultados
        self.result_area.setText("\n".join(results))

    def trapecio(self, expr, a, b, n):
        # Método de integración por Trapecio
        x = symbols('x')
        h = (b - a) / n
        integral_value = (expr.subs(x, a) + expr.subs(x, b)) / 2
        for i in range(1, n):
            xi = a + i * h
            integral_value += expr.subs(x, xi)
        integral_value *= h
        return integral_value

    def simpson(self, expr, a, b, n):
        # Método de integración por Simpson
        x = symbols('x')
        h = (b - a) / n
        integral_value = expr.subs(x, a) + expr.subs(x, b)
        for i in range(1, n, 2):
            xi = a + i * h
            integral_value += 4 * expr.subs(x, xi)
        for i in range(2, n, 2):
            xi = a + i * h
            integral_value += 2 * expr.subs(x, xi)
        integral_value *= h / 3
        return integral_value

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CalculadoraIntegracionNumerica()
    window.show()
    sys.exit(app.exec_())
