from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QFrame,
                             QGraphicsScene, QGraphicsItem, QGraphicsView,
                             QGraphicsPixmapItem, QProgressBar)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QThread,
                          QMimeData, QTimer)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QDrag, QPainter)
import os
import sys
from parametros import (DICT_SPRITES_MAP, calcular_N, DICT_SPRITES_PERSONAJE,
                        ENERGIA_INICIAL, MONEDAS_INICIALES)
from time import sleep
import BackEnd
import parametros_precios
import parametros_plantas

class VentanaStats(QFrame):
    pausa_signal = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.init_gui()
        self.pausar = False
    def init_gui(self):
        self.setFixedWidth(200)
        self.nombre = QLabel("Estadisticas",self)
        self.dia = QLabel("Dia", self)
        self.hora = QLabel("Hora", self)
        self.dinero = QLabel(f"Dinero: ${MONEDAS_INICIALES}", self)
        self.energia_label = QLabel("Energia:", self)
        self.energia_pbar = QProgressBar(self)
        self.energia_pbar.setMinimum(0)
        self.energia_pbar.setMaximum(ENERGIA_INICIAL)
        self.energia_pbar.setValue(ENERGIA_INICIAL)
        self.pausa = QPushButton("Pausa", self)
        self.pausa.clicked.connect(self.pausar_juego)
        self.setFrameShape(QFrame.Panel)
        vbox = QVBoxLayout()
        vbox.addWidget(self.nombre)
        vbox.addWidget(self.dia)
        vbox.addWidget(self.hora)
        vbox.addWidget(self.dinero)
        vbox.addWidget(self.energia_label)
        vbox.addWidget(self.energia_pbar)
        vbox.addWidget(self.pausa)
        self.setLayout(vbox)

    def pausar_juego(self, event):
        if self.pausar:
            self.pausa.setText("Pausa")
            self.pausar = False
            self.pausa_signal.emit(False)
        else:
            self.pausa.setText("Reanudar")
            self.pausar = True
            self.pausa_signal.emit(True)

    def actualizar_hora_fecha(self, data):
        dia, hora, minuto = data
        self.dia.setText(f"Dia: {dia}")
        self.hora.setText(f"Hora: {hora}:{minuto}")

    def actualizar_dinero(self, dinero):
        self.dinero.setText(f"Dinero: ${dinero}")

    def actualizar_energia(self, data):
        self.energia_pbar.setValue(data)
