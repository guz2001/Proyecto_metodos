from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QWidget, QTextEdit, QTableWidget, QTableWidgetItem
)
import numpy as np
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from decimal import Decimal, getcontext
getcontext().prec = 20
class GaussJacobiCalculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Gauss-Jacobi")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Número de ecuaciones
        self.label_equations = QLabel("Número de ecuaciones:")
        self.layout.addWidget(self.label_equations)
        self.num_equations_input = QSpinBox()
        self.num_equations_input.setRange(2, 10)
        self.num_equations_input.setValue(3)
        self.layout.addWidget(self.num_equations_input)

        # Botón para generar tabla de coeficientes
        self.generate_table_button = QPushButton("Generar tabla")
        self.generate_table_button.clicked.connect(self.generate_table)
        self.layout.addWidget(self.generate_table_button)

        # Tabla de coeficientes
        self.coefficient_table = QTableWidget()
        self.layout.addWidget(self.coefficient_table)

        # Configuración de iteraciones y tolerancia
        self.label_iterations = QLabel("Número máximo de iteraciones:")
        self.layout.addWidget(self.label_iterations)
        self.input_iterations = QSpinBox()
        self.input_iterations.setRange(1, 1000)
        self.input_iterations.setValue(3)
        self.layout.addWidget(self.input_iterations)

        self.label_tolerance = QLabel("Tolerancia:")
        self.layout.addWidget(self.label_tolerance)
        self.input_tolerance = QLineEdit("0.0001")
        self.layout.addWidget(self.input_tolerance)

        # Botón para calcular
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.clicked.connect(self.calculate_gauss_jacobi)
        self.layout.addWidget(self.calculate_button)

        # Área de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def generate_table(self):
        n = self.num_equations_input.value()
        self.coefficient_table.setRowCount(n)
        self.coefficient_table.setColumnCount(n + 1)
        self.coefficient_table.setHorizontalHeaderLabels(
            [f"x{i + 1}" for i in range(n)] + ["b"]
        )
        for i in range(n):
            for j in range(n + 1):
                self.coefficient_table.setItem(i, j, QTableWidgetItem("0"))

    def calculate_gauss_jacobi(self):
        try:
            n = self.num_equations_input.value()
            max_iterations = self.input_iterations.value()
            tolerance = float(self.input_tolerance.text())

            # Extraer los valores de la tabla
            A = np.zeros((n, n))
            b = np.zeros(n)
            for i in range(n):
                for j in range(n):
                    A[i, j] = float(self.coefficient_table.item(i, j).text())
                b[i] = float(self.coefficient_table.item(i, n).text())

            # Comprobación de diagonal dominante
            if not self.is_diagonally_dominant(A):
                self.result_area.setText(
                    "La matriz no es diagonal dominante. El método podría no converger."
                )
                return

            # Inicializar las soluciones
            x = np.zeros(n)
            results = []

            # Iteraciones de Gauss-Jacobi
            for iteration in range(1, max_iterations + 1):
                x_new = np.copy(x)
                for i in range(n):
                    sum_ = sum(A[i, j] * x[j] for j in range(n) if j != i)
                    x_new[i] = (b[i] - sum_) / A[i, i]

                # Verificar convergencia
                diff = np.linalg.norm(x_new - x, ord=np.inf)
                results.append(f"Iteración {iteration}: x = {x_new}, Error = {diff:.6f}")
                if diff < tolerance:
                    results.append("Convergencia alcanzada.")
                    self.result_area.setText("\n".join(results))
                    return

                x = x_new

            results.append("No se alcanzó la convergencia en el número máximo de iteraciones.")
            self.result_area.setText("\n".join(results))

        except Exception as e:
            self.result_area.setText(f"Error en el cálculo: {e}")

    def is_diagonally_dominant(self, A):
        """Verifica si una matriz es diagonalmente dominante."""
        for i in range(len(A)):
            diag = abs(A[i, i])
            off_diag_sum = sum(abs(A[i, j]) for j in range(len(A)) if i != j)
            if diag <= off_diag_sum:
                return False
        return True


if   __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # Estilo CSS
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2E3440;
        }
        QLabel {
            font-size: 14px;
            color: #D8DEE9;
        }
        QLineEdit, QDoubleSpinBox, QSpinBox {
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            background-color: #5E81AC;
            color: white;
            border: dark;
            padding: 10px;
            border-radius: 5px;
        } 
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QTextEdit {
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
            border-radius: 5px;
            padding: 10px;
        }
    """)
    window = GaussJacobiCalculadora()
    window.show()
    sys.exit(app.exec_())