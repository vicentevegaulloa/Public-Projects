from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QFrame,
                             QGraphicsScene, QGraphicsItem, QGraphicsView,
                             QGraphicsPixmapItem)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QThread, QTimer)
from PyQt5.QtGui import (QPixmap, QFont, QMovie)
import os
import sys
from parametros import (DICT_SPRITES_MAP, calcular_N, DICT_SPRITES_PERSONAJE,
                              ENERGIA_INICIAL)
from time import sleep
import BackEnd
import parametros_precios
import parametros_plantas
from ventana_inv_tienda import VentanaTienda, VentanaInventario
from stats import VentanaStats
import random
from parametros_acciones import (ENERGIA_RECOGER, ENERGIA_COSECHAR,
                                 ENERGIA_HERRAMIENTA)

class AparicionLabel(QLabel):
    pressed_signal = pyqtSignal()
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
    def mousePressEvent(self, event):
        self.pressed_signal.emit()

class DropLabel(QLabel):
    plantar_signal = pyqtSignal(tuple)
    descontar_inventario = pyqtSignal(str)
    arado_signal = pyqtSignal()
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.tipo = None
        self.sembrado = False
        self.arable = False
    def dragEnterEvent(self, event):
        if self.tipo == DICT_SPRITES_MAP["C"]:
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.plantar_signal.emit((text,
                                  self.x(),
                                  self.y(),
                                  self.width(),
                                  self.height()))
        self.descontar_inventario.emit(text)

        event.acceptProposedAction()

    def mousePressEvent(self, event):
        if self.arable and self.tipo == DICT_SPRITES_MAP["O"]:
            pixeles = QPixmap(DICT_SPRITES_MAP["C"]).scaled(self.width(),
                                                            self.height(),
                                                            Qt.IgnoreAspectRatio)
            self.tipo = DICT_SPRITES_MAP["C"]
            #self.setFrameShape(QFrame.Panel)
            self.setPixmap(pixeles)
            self.setScaledContents(True)
            self.setVisible(True)
            self.arable = False
            self.arado_signal.emit()

class AparicionEspontanea(QThread):
    celda_ocupada_signal = pyqtSignal(str)
    hacha_signal = pyqtSignal()
    timer_action = pyqtSignal(bool)
    def __init__(self, parent, tipo, x, y, w, h):
        super().__init__()
        self.tipo = tipo
        self.be_aparicion = BackEnd.AparicionEspontanea(self.tipo)
        self.be_aparicion.timer_signal.connect(self.kill_aparicion)
        self.timer_action.connect(self.be_aparicion.timer_accion)
        self.parent = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = AparicionLabel(self.parent)
        self.img.pressed_signal.connect(self.aparicion_clickeada)
        if self.tipo == "arbol":
            pixmap = QPixmap("sprites/otros/tree.png")
            pixmap.scaled(self.w, self.h, Qt.IgnoreAspectRatio)
            self.img.setGeometry(self.x + 5, self.y - self.h + 5,
                                 pixmap.width(), pixmap.height())
        elif self.tipo == "oro":
            pixmap = QPixmap("sprites/recursos/gold.png")
            pixmap.scaledToWidth(self.w)
            self.img.setGeometry(self.x + 5, self.y - self.h + 5,
                                 pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(False)
        self.recurso = False
        self.ocupado_box = QRect(self.img.x(), self.img.y() + self.img.height(),
                                 self.img.width(), 1)
        self.recurso_box = QRect()
        #self.img.setFrameShape(QFrame.Panel)
        self.start()

    def kill_aparicion(self):
        self.img.hide()
        self.recurso_box = QRect()
        self.timer_action.emit(False)
    def aparicion_clickeada(self):
        if self.tipo == "arbol":
            self.hacha_signal.emit()
    def update_aparicion(self, data):
        if self.tipo == "arbol":
            pixmap = QPixmap(f"sprites/recursos/wood.png")
            pixmap.scaledToWidth(self.w)
            self.img.resize(pixmap.width(), pixmap.height())
            self.img.setPixmap(pixmap)
            self.img.setScaledContents(False)
        self.recurso = True
        self.ocupado_box = QRect()
        self.recurso_box = QRect(self.img.x(), self.img.y(), self.img.width(), self.img.height())
        self.timer_action.emit(True)
    def run(self):
        self.img.show()
        if self.tipo == "oro":
            self.update_aparicion(None)

class ActMapa(QThread):
    clicked_recurso_signal = pyqtSignal(int)
    perder_energia_signal = pyqtSignal(tuple)
    def __init__(self,parent, N, columna, fila, maplist, H_o_T = False, solid=False, tipo=None):
        super().__init__()
        self.arable = False
        self.hachable = False
        self.aparicion = False
        self.recurso = False
        self.tipo = tipo
        self.solid = solid
        self.maplist = maplist
        self.fila = fila
        self.columna = columna
        self.N = N
        self.parent = parent
        self.H_o_T = H_o_T
        pixeles = QPixmap(self.maplist[self.fila][self.columna])
        pixeles = pixeles.scaled(self.N, self.N, Qt.IgnoreAspectRatio)
        self.label = DropLabel(self.parent)
        self.label.arado_signal.connect(self.arar)
        self.label.tipo = self.tipo
        if self.H_o_T == True:
            self.label.setGeometry(((self.N/2)-1) * self.columna,
                              ((self.N/2)-1) * self.fila,
                              self.N, self.N)
        else:
            self.label.setGeometry((self.N-1) * self.columna,
                              (self.N-1) * self.fila,
                              self.N, self.N)
        #self.label.setFrameShape(QFrame.Panel)
        self.label.setPixmap(pixeles)
        self.label.setScaledContents(True)
        self.label.setVisible(True)
        self.label.box = QRect(self.label.x(), self.label.y(),
                               self.label.width(), self.label.height())

        self.start()
    def cansarse(self, event):
        self.perder_energia_signal.emit(event)
    def arar(self):
        self.tipo = DICT_SPRITES_MAP["C"]
        self.cansarse((-ENERGIA_HERRAMIENTA, True))
    def has_hacha(self, event):
        self.hachable = event
    def has_azada(self, event):
        self.arable = event
        self.label.arable = event
    def apariciones(self, data):
        self.aparicion = data

    def hacha(self):
        if self.hachable:
            self.clicked_recurso_signal.emit(-ENERGIA_HERRAMIENTA)

    def run(self):
        self.label.show()

class Choclo(QThread):
    resembrar_signal = pyqtSignal(tuple)
    def __init__(self, parent, x, y, w, h):
        super().__init__()
        self.tipo = "choclo"
        self.be_choclo = BackEnd.Choclo()
        self.be_choclo.stage_up_signal.connect(self.update_choclo)
        self.parent = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = QLabel(self.parent)
        pixmap = QPixmap("sprites/cultivos/choclo/stage_1.png")
        pixmap.scaledToWidth(self.w)
        self.img.setGeometry(self.x + 5, self.y - self.h + 5, pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(False)
        self.recurso = False
        self.box = QRect(self.img.x(), self.img.y() + self.img.height(), self.img.width(), 1)
        self.fruto_box = QRect()
        #self.img.setFrameShape(QFrame.Panel)
        self.start()

    def update_choclo(self, stage):
        if stage == 0:
            self.resembrar_signal.emit(("choclo", self.x, self.y, self.w, self.h))
            pixmap = QPixmap(f"sprites/cultivos/choclo/icon.png")
            pixmap.scaledToWidth(self.w)
            self.img.resize(pixmap.width(), pixmap.height())
            self.img.setPixmap(pixmap)
            self.img.setScaledContents(False)
            self.recurso = True
            self.box = QRect()
            self.fruto_box = QRect(self.img.x(), self.img.y(), self.img.width(), self.img.height())
        else:
            pixmap = QPixmap(f"sprites/cultivos/choclo/stage_{stage}.png")
            pixmap.scaledToWidth(self.w)
            self.img.resize(pixmap.width(), pixmap.height())
            self.img.setPixmap(pixmap)
            self.img.setScaledContents(False)
            self.img.raise_()
    def run(self):
        self.img.show()
        self.img.raise_()

class Alcachofa(QThread):
    def __init__(self, parent, x, y, w, h):
        super().__init__()
        self.tipo = "alcachofa"
        self.be_alcachofa = BackEnd.Alcachofa()
        self.be_alcachofa.stage_up_signal.connect(self.update_alcachofa)
        self.parent = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = QLabel(self.parent)
        pixmap = QPixmap("sprites/cultivos/alcachofa/stage_1.png")
        pixmap.scaledToWidth(self.w)
        self.img.setGeometry(self.x + 5, self.y - self.h + 20, pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(False)
        self.box = QRect(self.img.x(), self.img.y() + self.img.height(), self.img.width(), 1)
        self.fruto_box = QRect()
        self.recurso = False
        #self.img.setFrameShape(QFrame.Panel)
        self.start()

    def update_alcachofa(self, stage):
        if stage == 0:
            pixmap = QPixmap(f"sprites/cultivos/alcachofa/icon.png")
            pixmap.scaledToWidth(self.w)
            self.img.resize(pixmap.width(), pixmap.height())
            self.img.setPixmap(pixmap)
            self.img.setScaledContents(False)
            self.recurso = True
            self.box = QRect()
            self.fruto_box = QRect(self.img.x(), self.img.y(), self.img.width(), self.img.height())

        else:
            pixmap = QPixmap(f"sprites/cultivos/alcachofa/stage_{stage}.png")
            pixmap.scaledToWidth(self.w)
            self.img.resize(pixmap.width(), pixmap.height())
            self.img.setPixmap(pixmap)
            self.img.setScaledContents(False)
            self.img.raise_()
    def run(self):
        self.img.show()

class Jugador(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feet = QRect()
