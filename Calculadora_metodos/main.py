from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from metodo_newton_raphson import NewtonRaphsonCalculadora  # Importamos la ventana de Newton-Raphson
from metodo_biseccion import BiseeccionCalculadora  # Suponiendo que ya tengas otro método implementado
from metodo_puntofijo import PuntoFijoCalculadora  #
from metodo_gaussjacobi import GaussJacobiCalculadora
from metodo_integracionumerica import CalculadoraIntegracionNumerica
from metodo_diferenciacionumerica import CalculadoraDiferenciacionNumerica
from metodo_GaussSeider import CalculadoraGaussSeidel
from metodo_PolinomioLagrange import CalculadoraLagrangeInterpolator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Métodos Numéricos")
        self.setGeometry(120, 120, 700, 500)

        # Crear un layout para la ventana principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Botones para acceder a los diferentes métodos
        self.newton_button = QPushButton("Método Newton-Raphson")
        self.layout.addWidget(self.newton_button)
        self.newton_button.clicked.connect(self.open_newton_raphson)

        self.bisection_button = QPushButton("Método de Bisección")  # Este botón es solo un ejemplo
        self.layout.addWidget(self.bisection_button)
        self.bisection_button.clicked.connect(self.open_bisection)

        self.puntofijo_button = QPushButton("Método Punto Fijo")
        self.layout.addWidget(self.puntofijo_button)
        self.puntofijo_button.clicked.connect(self.open_puntofijo)    

        self.gaussjacobi_button = QPushButton("Metodo Gauss-Jacobi")
        self.layout.addWidget(self.gaussjacobi_button)
        self.gaussjacobi_button.clicked.connect(self.open_gaussjacobi)

        self.integracionumerica_button =QPushButton("Metodo de Integracion Numerica")
        self.layout.addWidget(self.integracionumerica_button)
        self.integracionumerica_button.clicked.connect(self.open_integracionumerica)

        self.diferenciacionumerica_button =QPushButton("Metodo de Diferenciacion numerica")
        self.layout.addWidget(self.diferenciacionumerica_button)
        self.diferenciacionumerica_button.clicked.connect(self.open_diferenciacionumerica)
        
        self.GaussSeider_button =QPushButton("Metodo de GaussSeider")
        self.layout.addWidget(self.GaussSeider_button)
        self.GaussSeider_button.clicked.connect(self.open_gauss_seider)

        self.polinomiolagrange_button = QPushButton("Metodo Polinomio de Lagrange ")
        self.layout.addWidget (self.polinomiolagrange_button)
        self.polinomiolagrange_button.clicked.connect(self.open_polinomiolagrange)


    def open_newton_raphson(self):
        self.newton_window = NewtonRaphsonCalculadora()  # Crear la ventana de Newton-Raphson
        self.newton_window.show()

    def open_bisection(self):
        self.bisection_window = BiseeccionCalculadora()  # Crear la ventana del método de bisección
        self.bisection_window.show()

    def open_puntofijo(self):
        self.puntofijo_window = PuntoFijoCalculadora ()
        self.puntofijo_window.show()

    def open_gaussjacobi(self):
        self.gaussjacobi_window = GaussJacobiCalculadora ()
        self.gaussjacobi_window.show()

    def open_integracionumerica(self):
        self.integracionumerica_window = CalculadoraIntegracionNumerica()
        self.integracionumerica_window.show()

    def open_diferenciacionumerica(self):
        self.diferenciacionumerica_window = CalculadoraDiferenciacionNumerica()
        self.diferenciacionumerica_window.show()
    
    def open_gauss_seider(self):
        self.gauss_seider_window = CalculadoraGaussSeidel()
        self.gauss_seider_window.show()

    def open_polinomiolagrange(self):
        self.polinomiolagrange_window = CalculadoraLagrangeInterpolator()
        self.polinomiolagrange_window.show()
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Estilo CSS para la ventana principal
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2E3440;
        }
        QLabel {
            font-size: 16px;
            color: #D8DEE9;
        }
        QPushButton {
            background-color: #5E81AC;
            color: white;
            border: none;
            padding: 10px;
            font-size: 14px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QPushButton:pressed {
            background-color: #4C566A;
        }
    """)

    from main import MainWindow  
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())