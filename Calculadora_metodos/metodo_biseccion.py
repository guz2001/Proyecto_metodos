from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QWidget, QTextEdit, QDoubleSpinBox
)
from decimal import Decimal, getcontext
getcontext().prec = 20
class BiseeccionCalculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Bisección")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Entrada de función
        self.label_function = QLabel("Ingrese la función (en x):")
        self.layout.addWidget(self.label_function)
        self.input_function = QLineEdit()
        self.layout.addWidget(self.input_function)

        # Entrada de intervalo
        self.label_interval = QLabel("Intervalo (a, b):")
        self.layout.addWidget(self.label_interval)
        self.input_a = QDoubleSpinBox()
        self.input_a.setRange(-1e6, 1e6)
        self.input_a.setDecimals(6)
        self.input_a.setValue(-1.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_a)
        
        self.input_b = QDoubleSpinBox()
        self.input_b.setRange(-1e6, 1e6)
        self.input_b.setDecimals(6)
        self.input_b.setValue(1.0)  # Valor inicial predeterminado
        self.layout.addWidget(self.input_b)

        # Entrada de iteraciones
        self.label_iterations = QLabel("Número máximo de iteraciones:")
        self.layout.addWidget(self.label_iterations)
        self.input_iterations = QSpinBox()
        self.input_iterations.setRange(1, 1000)
        self.layout.addWidget(self.input_iterations)

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
        self.calculate_button.clicked.connect(self.calculate_bisection)
        self.layout.addWidget(self.calculate_button)

        # Salida de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def calculate_bisection(self):
        # Obtener la función ingresada
        function_text = self.input_function.text()
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(function_text, transformations=transformations)
        except Exception as e:
            self.result_area.setText(f"Error en la función: {e}")
            return

        # Obtener los límites del intervalo, el número de iteraciones y la tolerancia
        a = self.input_a.value()
        b = self.input_b.value()
        max_iterations = self.input_iterations.value()
        tolerance = self.input_tolerance.value()

        # Definir el símbolo
        x = symbols('x')
        
        # Comprobar si la función tiene signos opuestos en los extremos del intervalo
        f_a = expr.subs(x, a)
        f_b = expr.subs(x, b)
        
        if f_a * f_b > 0:
            self.result_area.setText("Error: La función no cambia de signo en el intervalo dado.")
            return

        # Método de Bisección
        results = []
        try:
            for i in range(max_iterations):
                # Calcular el punto medio
                c = (a + b) / 2
                f_c = expr.subs(x, c)
                
                results.append(f"Iteración {i + 1}: c = {c:.6f}, f(c) = {f_c:.6f}")
                
                # Verificar convergencia
                if abs(f_c) < tolerance:
                    results.append(f"Convergencia alcanzada en la iteración {i + 1}.")
                    break

                # Actualizar el intervalo
                if f_a * f_c < 0:
                    b = c
                    f_b = f_c
                else:
                    a = c
                    f_a = f_c
            else:
                results.append("No se alcanzó la convergencia en el número máximo de iteraciones.")
                
            self.result_area.setText("\n".join(results))
        
        except Exception as e:
            self.result_area.setText(f"Error en el cálculo: {e}")



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
    window = BiseeccionCalculadora()
    window.show()
    sys.exit(app.exec_())

