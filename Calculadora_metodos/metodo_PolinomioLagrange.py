from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox, QPushButton, QTextEdit, QWidget, QSpinBox
)
import numpy as np
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from decimal import Decimal, getcontext
getcontext().prec = 20
class CalculadoraLagrangeInterpolator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Interpolación de Lagrange")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Entrada de los puntos (x, y)
        self.label_points = QLabel("Ingrese los puntos (x, y) separados por comas:")
        self.layout.addWidget(self.label_points)
        self.input_points = QLineEdit()
        self.layout.addWidget(self.input_points)

        # Entrada del valor de x para evaluar el polinomio
        self.label_x_value = QLabel("Ingrese el valor de x para evaluar el polinomio:")
        self.layout.addWidget(self.label_x_value)
        self.input_x_value = QDoubleSpinBox()
        self.input_x_value.setRange(-1e6, 1e6)
        self.input_x_value.setDecimals(6)
        self.input_x_value.setValue(1.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_x_value)

        # Botón de calcular
        self.calculate_button = QPushButton("Calcular Polinomio")
        self.calculate_button.clicked.connect(self.calculate_lagrange)
        self.layout.addWidget(self.calculate_button)

        # Salida de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def calculate_lagrange(self):
        # Obtener los puntos ingresados
        points_text = self.input_points.text()
        try:
            points = [tuple(map(float, point.split(','))) for point in points_text.split(';')]
        except Exception as e:
            self.result_area.setText(f"Error en los puntos: {e}")
            return

        # Extraer los valores de x e y
        x_values = np.array([point[0] for point in points])
        y_values = np.array([point[1] for point in points])

        # Obtener el valor de x para evaluar el polinomio
        x_eval = self.input_x_value.value()

        # Cálculo del polinomio de Lagrange
        def lagrange_polynomial(x_values, y_values, x_eval):
            n = len(x_values)
            result = 0.0
            for i in range(n):
                term = y_values[i]
                for j in range(n):
                    if j != i:
                        term *= (x_eval - x_values[j]) / (x_values[i] - x_values[j])
                result += term
            return result

        # Evaluar el polinomio en el punto dado
        lagrange_result = lagrange_polynomial(x_values, y_values, x_eval)

        # Mostrar el resultado
        self.result_area.setText(f"El valor del polinomio de Lagrange evaluado en x = {x_eval} es: {lagrange_result:.6f}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CalculadoraLagrangeInterpolator()
    window.show()
    sys.exit(app.exec_())
