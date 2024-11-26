from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDoubleSpinBox, QWidget, QSpinBox,QTableWidget
)
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 20
class CalculadoraGaussSeidel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Gauss-Seidel")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Selección del número de ecuaciones
        self.label_num_equations = QLabel("Número de ecuaciones:")
        self.layout.addWidget(self.label_num_equations)
        self.input_num_equations = QSpinBox()
        self.input_num_equations.setRange(2, 10)
        self.input_num_equations.setValue(3)
        self.input_num_equations.valueChanged.connect(self.generate_table)
        self.layout.addWidget(self.input_num_equations)

        # Generar tabla para los coeficientes
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.generate_table()  # Crear la tabla al iniciar

        # Número de iteraciones
        self.label_iterations = QLabel("Número máximo de iteraciones:")
        self.layout.addWidget(self.label_iterations)
        self.input_iterations = QSpinBox()
        self.input_iterations.setRange(1, 1000)
        self.input_iterations.setValue(25)
        self.layout.addWidget(self.input_iterations)

        # Tolerancia
        self.label_tolerance = QLabel("Tolerancia (ε):")
        self.layout.addWidget(self.label_tolerance)
        self.input_tolerance = QDoubleSpinBox()
        self.input_tolerance.setRange(1e-10, 1.0)
        self.input_tolerance.setDecimals(10)
        self.input_tolerance.setValue(1e-6)
        self.layout.addWidget(self.input_tolerance)

        # Botón para calcular
        self.calculate_button = QPushButton("Calcular Solución")
        self.calculate_button.clicked.connect(self.calculate_gauss_seidel)
        self.layout.addWidget(self.calculate_button)

        # Salida de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def generate_table(self):
        """Generar una tabla basada en el número de ecuaciones"""
        num_equations = self.input_num_equations.value()
        self.table.setRowCount(num_equations)
        self.table.setColumnCount(num_equations + 1)  # Coeficientes + término independiente
        self.table.setHorizontalHeaderLabels(
            [f"x{i+1}" for i in range(num_equations)] + ["Término independiente"]
        )

    def calculate_gauss_seidel(self):
        """Calcular la solución usando el método de Gauss-Seidel"""
        try:
            # Obtener datos de la tabla
            num_equations = self.input_num_equations.value()
            A = np.zeros((num_equations, num_equations))
            b = np.zeros(num_equations)

            for i in range(num_equations):
                for j in range(num_equations):
                    A[i, j] = float(self.table.item(i, j).text() or 0)
                b[i] = float(self.table.item(i, num_equations).text() or 0)

            # Configuración inicial
            max_iterations = self.input_iterations.value()
            tolerance = self.input_tolerance.value()
            x = np.zeros(num_equations)

            # Método de Gauss-Seidel
            results = []
            for iteration in range(max_iterations):
                x_old = x.copy()
                for i in range(num_equations):
                    sum_ax = sum(A[i, j] * x[j] for j in range(num_equations) if j != i)
                    x[i] = (b[i] - sum_ax) / A[i, i]

                # Verificar convergencia
                error = max(abs(x[i] - x_old[i]) for i in range(num_equations))
                results.append(f"Iteración {iteration + 1}: {x}")
                if error < tolerance:
                    results.append(f"Convergencia alcanzada en la iteración {iteration + 1}. Solución: {x}")
                    self.result_area.setText("\n".join(results))
                    return

            results.append("No se alcanzó la convergencia en el número máximo de iteraciones.")
            self.result_area.setText("\n".join(results))

        except Exception as e:
            self.result_area.setText(f"Error: {e}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CalculadoraGaussSeidel()
    window.show()
    sys.exit(app.exec_())
