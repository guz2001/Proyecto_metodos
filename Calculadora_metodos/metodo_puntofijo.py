import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QWidget, QTextEdit, QDoubleSpinBox
)
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from decimal import Decimal, getcontext
getcontext().prec = 20
class PuntoFijoCalculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Método del Punto Fijo")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Entrada de función
        self.label_function = QLabel("Ingrese la función (en x):")
        self.layout.addWidget(self.label_function)
        self.input_function = QLineEdit()
        self.layout.addWidget(self.input_function)

        # Entrada de iteraciones
        self.label_iterations = QLabel("Número máximo de iteraciones:")
        self.layout.addWidget(self.label_iterations)
        self.input_iterations = QSpinBox()
        self.input_iterations.setRange(1, 1000)
        self.layout.addWidget(self.input_iterations)

        # Entrada del punto inicial
        self.label_initial = QLabel("Valor inicial (x0):")
        self.layout.addWidget(self.label_initial)
        self.input_initial = QDoubleSpinBox()
        self.input_initial.setRange(-1e6, 1e6)
        self.input_initial.setDecimals(6)
        self.input_initial.setValue(1.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_initial)

        # Tolerancia
        self.label_tolerance = QLabel("Tolerancia (ε):")
        self.layout.addWidget(self.label_tolerance)
        self.input_tolerance = QDoubleSpinBox()
        self.input_tolerance.setRange(1e-10, 1.0)
        self.input_tolerance.setDecimals(10)
        self.input_tolerance.setValue(1e-6)  # Tolerancia predeterminada
        self.layout.addWidget(self.input_tolerance)

        # Botón de calcular
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.clicked.connect(self.calculate_punto_fijo)
        self.layout.addWidget(self.calculate_button)

        # Salida de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def calculate_punto_fijo(self):
        # Obtener la función ingresada
        function_text = self.input_function.text()
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(function_text, transformations=transformations)
        except Exception as e:
            self.result_area.setText(f"Error en la función: {e}")
            return

        # Obtener el número de iteraciones, valor inicial y tolerancia
        max_iterations = self.input_iterations.value()
        x0 = self.input_initial.value()
        tolerance = self.input_tolerance.value()

        # Método del Punto Fijo
        results = []
        try:
            for i in range(max_iterations):
                x1 = expr.subs(symbols('x'), x0)
                results.append(f"Iteración {i + 1}: x = {x1:.6f}, f(x) = {expr.subs(symbols('x'), x1):.6f}")
                # Verificar convergencia
                if abs(x1 - x0) < tolerance:
                    results.append(f"Convergencia alcanzada en la iteración {i + 1}.")
                    break
                x0 = x1
            else:
                results.append("No se alcanzó la convergencia en el número máximo de iteraciones.")
            self.result_area.setText("\n".join(results))
        except Exception as e:
            self.result_area.setText(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = PuntoFijoCalculadora()
    window.show()
    sys.exit(app.exec_())
