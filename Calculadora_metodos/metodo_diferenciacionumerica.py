import numpy as np
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox, QWidget, QTextEdit, QSpinBox,QComboBox
from decimal import Decimal, getcontext
getcontext().prec = 20
class CalculadoraDiferenciacionNumerica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Diferenciación Numérica")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Entrada de la función
        self.label_function = QLabel("Ingrese la función (en x):")
        self.layout.addWidget(self.label_function)
        self.input_function = QLineEdit()
        self.layout.addWidget(self.input_function)

        # Entrada del punto donde evaluar la derivada
        self.label_point = QLabel(r"Punto (x_0) donde calcular la derivada:")
        self.layout.addWidget(self.label_point)
        self.input_point = QDoubleSpinBox()
        self.input_point.setRange(-1e6, 1e6)
        self.input_point.setDecimals(6)
        self.input_point.setValue(0.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_point)
        

        # Selección del orden de la derivada
        self.label_order = QLabel("Orden de la derivada:")
        self.layout.addWidget(self.label_order)
        self.input_order = QSpinBox()
        self.input_order.setRange(1, 5)  # Hasta quinta derivada
        self.input_order.setValue(1)  # Primera derivada por defecto
        self.layout.addWidget(self.input_order)

        # Entrada del tamaño del paso h
        self.label_step = QLabel(r"Tamaño del paso (h):")
        self.layout.addWidget(self.label_step)
        self.input_step = QDoubleSpinBox()
        self.input_step.setRange(1e-6, 50)
        self.input_step.setDecimals(6)
        self.input_step.setValue(1)  # Paso predeterminado
        self.layout.addWidget(self.input_step)

        # Método de diferencias finitas
        self.label_method = QLabel("Seleccione el método de diferencias finitas:")
        self.layout.addWidget(self.label_method)
        self.method_selector = QComboBox()
        self.method_selector.addItems(["Hacia Adelante", "Hacia Atrás", "Centrado"])
        self.layout.addWidget(self.method_selector)

        # Botón de calcular
        self.calculate_button = QPushButton("Calcular Derivada")
        self.calculate_button.clicked.connect(self.calculate_derivative)
        self.layout.addWidget(self.calculate_button)

        # Salida de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def calculate_derivative(self):
        # Obtener la función ingresada
        function_text = self.input_function.text()
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(function_text, transformations=transformations)
        except Exception as e:
            self.result_area.setText(f"Error en la función: {e}")
            return

        # Obtener los datos de entrada
        x0 = self.input_point.value()
        h = self.input_step.value()
        order = self.input_order.value()
        method = self.method_selector.currentText()

        # Calcular la derivada
        x = symbols('x')
        try:
            if method == "Hacia Adelante":
                result = self.forward_difference(expr, x, x0, h, order)
            elif method == "Hacia Atrás":
                result = self.backward_difference(expr, x, x0, h, order)
            elif method == "Centrado":
                result = self.centered_difference(expr, x, x0, h, order)
            else:
                raise ValueError("Método no reconocido.")

            self.result_area.setText(f"Resultado de la derivada de orden {order} en x = {x0} usando el método '{method}':\n{result:.6f}")
        except Exception as e:
            self.result_area.setText(f"Error en el cálculo: {e}")

    def forward_difference(self, expr, x, x0, h, order):
        """Diferencias finitas hacia adelante"""
        if order == 1:
            return (expr.subs(x, x0 + h) - expr.subs(x, x0)) / h
        elif order == 2:
            return (expr.subs(x, x0 + 2*h) - 2*expr.subs(x, x0 + h) + expr.subs(x, x0)) / (h**2)
        elif order == 3:
            return (expr.subs(x, x0 + 3*h) - 3*expr.subs(x, x0 + 2*h) + 3*expr.subs(x, x0 + h) - expr.subs(x, x0)) / (h**3)
        else:
            raise ValueError("Orden no soportado para diferencias hacia adelante.")

    def backward_difference(self, expr, x, x0, h, order):
        """Diferencias finitas hacia atrás"""
        if order == 1:
            return (expr.subs(x, x0) - expr.subs(x, x0 - h)) / h
        elif order == 2:
            return (expr.subs(x, x0) - 2*expr.subs(x, x0 - h) + expr.subs(x, x0 - 2*h)) / (h**2)
        elif order == 3:
            return (expr.subs(x, x0) - 3*expr.subs(x, x0 - h) + 3*expr.subs(x, x0 - 2*h) - expr.subs(x, x0 - 3*h)) / (h**3)
        else:
            raise ValueError("Orden no soportado para diferencias hacia atrás.")

    def centered_difference(self, expr, x, x0, h, order):
        """Diferencias finitas centradas"""
        if order == 1:
            return (expr.subs(x, x0 + h) - expr.subs(x, x0 - h)) / (2 * h)
        elif order == 2:
            return (expr.subs(x, x0 + h) - 2*expr.subs(x, x0) + expr.subs(x, x0 - h)) / (h**2)
        elif order == 3:
            return (expr.subs(x, x0 + 2*h) - 2*expr.subs(x, x0 + h) + 2*expr.subs(x, x0 - h) - expr.subs(x, x0 - 2*h)) / (2 * h**3)
        else:
            raise ValueError("Orden no soportado para diferencias centradas.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CalculadoraDiferenciacionNumerica()
    window.show()
    sys.exit(app.exec_())
    

