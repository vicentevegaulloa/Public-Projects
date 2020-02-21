from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect)
from PyQt5.QtGui import (QPixmap, QFont, QMovie)
import os
import DCColgado

class VentanaJuego(QWidget):

    enviar_letra_signal = pyqtSignal(dict)
    reiniciar_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Colgado")
        self.setGeometry(200, 200, 400, 400)

        #palabra
        self.palabra = QLabel("", self)
        #foto
        self.foto = QLabel(self)
        self.foto.setGeometry(50, 50, 50, 50)
        ruta_imagen = os.path.join('images', '1.png')
        pixeles = QPixmap(ruta_imagen)
        self.foto.setPixmap(pixeles)
        self.foto.setScaledContents(True)
        #Boton slect
        self.boton_select = QPushButton("&Seleccionar Letra",self)
        self.boton_select.clicked.connect(self.boton_select_clicked)
        self.boton_select.resize(self.boton_select.sizeHint())
        #boton_nuevo
        self.boton_nuevo = QPushButton("&Nuevo Juego",self)
        self.boton_nuevo.clicked.connect(self.boton_nuevo_clicked)
        self.boton_nuevo.resize(self.boton_nuevo.sizeHint())
        #usadas
        self.usadas = QLabel("", self)
        self.usadas_label = QLabel("Usadas:", self)
        #disponibles
        self.disponibles = QLabel("", self)
        self.disponibles_label = QLabel("Disponibles:", self)
        #letra
        self.letra = QLabel("", self)

        #layout
        contenedor = QVBoxLayout()
        contenedor.addWidget(self.palabra)
        contenedor.addWidget(self.foto)
        contenedor.addWidget(self.usadas_label)
        contenedor.addWidget(self.usadas)
        contenedor.addWidget(self.disponibles_label)
        contenedor.addWidget(self.disponibles)
        contenedor.addWidget(self.letra)
        contenedor.addWidget(self.boton_select)
        contenedor.addWidget(self.boton_nuevo)

        # Fijamos el Layout completo
        self.setLayout(contenedor)

        self.show()

    def keyPressEvent(self, event):
        """
        Este método maneja el evento que se produce al presionar las teclas.
        """
        self.letra.setText(f'{event.text()}')
        self.letra.resize(self.letra.sizeHint())

    def boton_select_clicked(self):
        envio = {"letra": self.letra.text(),
                 "usadas": self.usadas.text(),
                 "disponibles": self.disponibles.text(),
                 "palabra": self.palabra.text()}
        self.enviar_letra_signal.emit(envio)


    def boton_nuevo_clicked(self):
        self.reiniciar_signal.emit()

    def trabajar_diccionario(self, dict):
            self.palabra.setText(dict["palabra"])
            pixeles = QPixmap(dict["imagen"])
            self.foto.setPixmap(pixeles)
            self.foto.setScaledContents(True)
            self.usadas.setText(dict["usadas"])
            self.disponibles.setText(dict["disponibles"])
