from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QFrame,
                             QGraphicsScene, QGraphicsItem, QGraphicsView,
                             QGraphicsPixmapItem)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QThread,
                          QMimeData, QTimer)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QDrag, QPainter)
import os
import sys
from parametros import DICT_SPRITES_MAP, calcular_N, DICT_SPRITES_PERSONAJE
from time import sleep
import BackEnd
import parametros_precios
import parametros_plantas
#la siguiente clase la saque de
#https://stackoverflow.com/questions/55636860/drag-and-drop-qlabels-with-pyqt5-pixmap-and-text
class DraggableLabel(QLabel):
    def __init__(self, tipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = tipo
        self.cant = 0
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        if self.cant < 1:
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        if self.tipo == "choclo":
            mimedata.setText("choclo")
            pixmap = QPixmap("sprites/cultivos/choclo/seeds.png")
        elif self.tipo == "alcachofa":
            mimedata.setText("alcachofa")
            pixmap = QPixmap("sprites/cultivos/alcachofa/seeds.png")
        drag.setMimeData(mimedata)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

class VentanaInventario(QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setFixedHeight(100)
        self.nombre = QLabel("Inventario",self)

        #hoe
        pixmap_hoe = QPixmap("sprites/otros/hoe.png")
        self.img_hoe = QLabel(self)
        self.img_hoe.setPixmap(pixmap_hoe)
        self.cant_hoe = QLabel(f"0", self)
        hoe_layout = QVBoxLayout()
        hoe_layout.addWidget(self.img_hoe)
        hoe_layout.addWidget(self.cant_hoe)
        #axe
        pixmap_axe = QPixmap("sprites/otros/axe.png")
        self.img_axe = QLabel(self)
        self.img_axe.setPixmap(pixmap_axe)
        self.cant_axe = QLabel(f"0", self)
        axe_layout = QVBoxLayout()
        axe_layout.addWidget(self.img_axe)
        axe_layout.addWidget(self.cant_axe)
        #choclo seeds
        pixmap_choclo_seeds = QPixmap("sprites/cultivos/choclo/seeds.png")
        self.img_choclo_seeds = DraggableLabel("choclo",self)
        self.img_choclo_seeds.setPixmap(pixmap_choclo_seeds)
        self.cant_choclo_seeds = QLabel(f"0", self)
        choclo_seeds_layout = QVBoxLayout()
        choclo_seeds_layout.addWidget(self.img_choclo_seeds)
        choclo_seeds_layout.addWidget(self.cant_choclo_seeds)
        #alcachofa seeds
        pixmap_alcachofa_seeds = QPixmap("sprites/cultivos/alcachofa/seeds.png")
        self.img_alcachofa_seeds = DraggableLabel("alcachofa", self)
        self.img_alcachofa_seeds.setPixmap(pixmap_alcachofa_seeds)
        self.cant_alcachofa_seeds = QLabel(f"0", self)
        alcachofa_seeds_layout = QVBoxLayout()
        alcachofa_seeds_layout.addWidget(self.img_alcachofa_seeds)
        alcachofa_seeds_layout.addWidget(self.cant_alcachofa_seeds)
        #alcachofa
        pixmap_alcachofa = QPixmap("sprites/cultivos/alcachofa/icon.png")
        self.img_alcachofa = QLabel(self)
        self.img_alcachofa.setPixmap(pixmap_alcachofa)
        self.cant_alcachofa = QLabel(f"0", self)
        alcachofa_layout = QVBoxLayout()
        alcachofa_layout.addWidget(self.img_alcachofa)
        alcachofa_layout.addWidget(self.cant_alcachofa)
        #choclo
        pixmap_choclo = QPixmap("sprites/cultivos/choclo/icon.png")
        self.img_choclo = QLabel(self)
        self.img_choclo.setPixmap(pixmap_choclo)
        self.cant_choclo = QLabel(f"0", self)
        choclo_layout = QVBoxLayout()
        choclo_layout.addWidget(self.img_choclo)
        choclo_layout.addWidget(self.cant_choclo)
        #madera
        pixmap_madera = QPixmap("sprites/recursos/wood.png")
        self.img_madera = QLabel(self)
        self.img_madera.setPixmap(pixmap_madera)
        self.cant_madera = QLabel(f"0", self)
        madera_layout = QVBoxLayout()
        madera_layout.addWidget(self.img_madera)
        madera_layout.addWidget(self.cant_madera)
        #Oro
        pixmap_oro = QPixmap("sprites/recursos/gold.png")
        self.img_oro = QLabel(self)
        self.img_oro.setPixmap(pixmap_oro)
        self.cant_oro = QLabel(f"0", self)
        oro_layout = QVBoxLayout()
        oro_layout.addWidget(self.img_oro)
        oro_layout.addWidget(self.cant_oro)

        items_layout = QHBoxLayout()
        items_layout.addLayout(hoe_layout)
        items_layout.addLayout(axe_layout)
        items_layout.addLayout(choclo_seeds_layout)
        items_layout.addLayout(alcachofa_seeds_layout)
        items_layout.addLayout(alcachofa_layout)
        items_layout.addLayout(choclo_layout)
        items_layout.addLayout(madera_layout)
        items_layout.addLayout(oro_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.nombre)
        main_layout.addLayout(items_layout)
        self.setLayout(main_layout)


    def update_inventario(self, data):
        mensaje, dict = data
        self.cant_alcachofa.setText(str(dict["ALCACHOFA"]))
        self.cant_choclo.setText(str(dict["CHOCLO"]))
        self.cant_madera.setText(str(dict["LEÑA"]))
        self.cant_oro.setText(str(dict["ORO"]))
        self.cant_hoe.setText(str(dict["AZADA"]))
        self.cant_axe.setText(str(dict["HACHA"]))
        self.cant_alcachofa_seeds.setText(str(dict["SEMILLAS ALCACHOFA"]))
        self.cant_choclo_seeds.setText(str(dict["SEMILLAS CHOCLO"]))
        self.img_choclo_seeds.cant = dict["SEMILLAS CHOCLO"]
        self.img_alcachofa_seeds.cant = dict["SEMILLAS ALCACHOFA"]

class VentanaTienda(QWidget):

    senal_compra_venta = pyqtSignal(str)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):

        self.setGeometry(500, 200, 700, 500)
        self.setFixedSize(700, 500)
        self.setWindowTitle('Tienda')
        #status
        self.status = QLabel("", self)
        #labels
        self.item = QLabel("ITEM", self)
        self.precio = QLabel("PRECIO", self)
        self.accion = QLabel("ACCION", self)
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(self.item)
        labels_layout.addWidget(self.precio)
        labels_layout.addWidget(self.accion)
        #hoe
        pixmap_hoe = QPixmap("sprites/otros/hoe.png")
        self.img_hoe = QLabel(self)
        self.img_hoe.setPixmap(pixmap_hoe)
        self.precio_hoe = QLabel(f"${parametros_precios.PRECIO_AZADA}", self)
        self.vender_hoe = QPushButton("Vender AZADA", self)
        self.comprar_hoe = QPushButton("Comprar AZADA", self)
        hoe_buttons = QVBoxLayout()
        hoe_buttons.addWidget(self.comprar_hoe)
        hoe_buttons.addWidget(self.vender_hoe)
        hoe_layout = QHBoxLayout()
        hoe_layout.addWidget(self.img_hoe)
        hoe_layout.addWidget(self.precio_hoe)
        hoe_layout.addLayout(hoe_buttons)
        #axe
        pixmap_axe = QPixmap("sprites/otros/axe.png")
        self.img_axe = QLabel(self)
        self.img_axe.setPixmap(pixmap_axe)
        self.precio_axe = QLabel(f"${parametros_precios.PRECIO_HACHA}", self)
        self.vender_axe = QPushButton("Vender HACHA", self)
        self.comprar_axe = QPushButton("Comprar HACHA", self)
        axe_buttons = QVBoxLayout()
        axe_buttons.addWidget(self.comprar_axe)
        axe_buttons.addWidget(self.vender_axe)
        axe_layout = QHBoxLayout()
        axe_layout.addWidget(self.img_axe)
        axe_layout.addWidget(self.precio_axe)
        axe_layout.addLayout(axe_buttons)
        #choclo seeds
        pixmap_choclo_seeds = QPixmap("sprites/cultivos/choclo/seeds.png")
        self.img_choclo_seeds = QLabel(self)
        self.img_choclo_seeds.setPixmap(pixmap_choclo_seeds)
        self.precio_choclo_seeds = QLabel(f"${parametros_precios.PRECIO_SEMILLA_CHOCLOS}", self)
        self.vender_choclo_seeds = QPushButton("Vender SEMILLA CHOCLO", self)
        self.comprar_choclo_seeds = QPushButton("Comprar SEMILLA CHOCLO", self)
        choclo_seeds_buttons = QVBoxLayout()
        choclo_seeds_buttons.addWidget(self.comprar_choclo_seeds)
        choclo_seeds_buttons.addWidget(self.vender_choclo_seeds)
        choclo_seeds_layout = QHBoxLayout()
        choclo_seeds_layout.addWidget(self.img_choclo_seeds)
        choclo_seeds_layout.addWidget(self.precio_choclo_seeds)
        choclo_seeds_layout.addLayout(choclo_seeds_buttons)
        #alcachofa seeds
        pixmap_alcachofa_seeds = QPixmap("sprites/cultivos/alcachofa/seeds.png")
        self.img_alcachofa_seeds = QLabel(self)
        self.img_alcachofa_seeds.setPixmap(pixmap_alcachofa_seeds)
        self.precio_alcachofa_seeds = QLabel(f"${parametros_precios.PRECIO_SEMILLA_ALCACHOFAS}", self)
        self.vender_alcachofa_seeds = QPushButton("Vender SEMILLA ALCACHOFA", self)
        self.comprar_alcachofa_seeds = QPushButton("Comprar SEMILLA ALCACHOFA", self)
        alcachofa_seeds_buttons = QVBoxLayout()
        alcachofa_seeds_buttons.addWidget(self.comprar_alcachofa_seeds)
        alcachofa_seeds_buttons.addWidget(self.vender_alcachofa_seeds)
        alcachofa_seeds_layout = QHBoxLayout()
        alcachofa_seeds_layout.addWidget(self.img_alcachofa_seeds)
        alcachofa_seeds_layout.addWidget(self.precio_alcachofa_seeds)
        alcachofa_seeds_layout.addLayout(alcachofa_seeds_buttons)
        #alcachofa
        pixmap_alcachofa = QPixmap("sprites/cultivos/alcachofa/icon.png")
        self.img_alcachofa = QLabel(self)
        self.img_alcachofa.setPixmap(pixmap_alcachofa)
        self.precio_alcachofa = QLabel(f"${parametros_precios.PRECIO_ALACACHOFAS}", self)
        self.vender_alcachofa = QPushButton("Vender ALCACHOFAS", self)
        alcachofa_buttons = QVBoxLayout()
        alcachofa_buttons.addWidget(self.vender_alcachofa)
        alcachofa_layout = QHBoxLayout()
        alcachofa_layout.addWidget(self.img_alcachofa)
        alcachofa_layout.addWidget(self.precio_alcachofa)
        alcachofa_layout.addLayout(alcachofa_buttons)
        #choclo
        pixmap_choclo = QPixmap("sprites/cultivos/choclo/icon.png")
        self.img_choclo = QLabel(self)
        self.img_choclo.setPixmap(pixmap_choclo)
        self.precio_choclo = QLabel(f"${parametros_precios.PRECIO_CHOCLOS}", self)
        self.vender_choclo = QPushButton("Vender CHOCLOS", self)
        choclo_buttons = QVBoxLayout()
        choclo_buttons.addWidget(self.vender_choclo)
        choclo_layout = QHBoxLayout()
        choclo_layout.addWidget(self.img_choclo)
        choclo_layout.addWidget(self.precio_choclo)
        choclo_layout.addLayout(choclo_buttons)
        #madera
        pixmap_madera = QPixmap("sprites/recursos/wood.png")
        self.img_madera = QLabel(self)
        self.img_madera.setPixmap(pixmap_madera)
        self.precio_madera = QLabel(f"${parametros_precios.PRECIO_LEÑA}", self)
        self.vender_madera = QPushButton("Vender LEÑA", self)
        madera_buttons = QVBoxLayout()
        madera_buttons.addWidget(self.vender_madera)
        madera_layout = QHBoxLayout()
        madera_layout.addWidget(self.img_madera)
        madera_layout.addWidget(self.precio_madera)
        madera_layout.addLayout(madera_buttons)
        #Oro
        pixmap_oro = QPixmap("sprites/recursos/gold.png")
        self.img_oro = QLabel(self)
        self.img_oro.setPixmap(pixmap_oro)
        self.precio_oro = QLabel(f"${parametros_precios.PRECIO_ORO}", self)
        self.vender_oro = QPushButton("Vender ORO", self)
        oro_buttons = QVBoxLayout()
        oro_buttons.addWidget(self.vender_oro)
        oro_layout = QHBoxLayout()
        oro_layout.addWidget(self.img_oro)
        oro_layout.addWidget(self.precio_oro)
        oro_layout.addLayout(oro_buttons)
        #ticket
        pixmap_ticket = QPixmap("sprites/otros/ticket.png")
        self.img_ticket = QLabel(self)
        self.img_ticket.setPixmap(pixmap_ticket)
        self.precio_ticket = QLabel(f"${parametros_precios.PRECIO_TICKET}", self)
        self.vender_ticket = QPushButton("Comprar TICKET", self)
        ticket_buttons = QVBoxLayout()
        ticket_buttons.addWidget(self.vender_ticket)
        ticket_layout = QHBoxLayout()
        ticket_layout.addWidget(self.img_ticket)
        ticket_layout.addWidget(self.precio_ticket)
        ticket_layout.addLayout(ticket_buttons)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.status)
        self.layout.addLayout(labels_layout)
        self.layout.addLayout(hoe_layout)
        self.layout.addLayout(axe_layout)
        self.layout.addLayout(choclo_seeds_layout)
        self.layout.addLayout(alcachofa_seeds_layout)
        self.layout.addLayout(alcachofa_layout)
        self.layout.addLayout(choclo_layout)
        self.layout.addLayout(madera_layout)
        self.layout.addLayout(oro_layout)
        self.layout.addLayout(ticket_layout)
        self.setLayout(self.layout)

        self.comprar_hoe.clicked.connect(self.compra_venta)
        self.vender_hoe.clicked.connect(self.compra_venta)
        self.comprar_axe.clicked.connect(self.compra_venta)
        self.vender_axe.clicked.connect(self.compra_venta)
        self.comprar_choclo_seeds.clicked.connect(self.compra_venta)
        self.vender_choclo_seeds.clicked.connect(self.compra_venta)
        self.comprar_alcachofa_seeds.clicked.connect(self.compra_venta)
        self.vender_alcachofa_seeds.clicked.connect(self.compra_venta)
        self.vender_alcachofa.clicked.connect(self.compra_venta)
        self.vender_choclo.clicked.connect(self.compra_venta)
        self.vender_madera.clicked.connect(self.compra_venta)
        self.vender_oro.clicked.connect(self.compra_venta)
        self.vender_ticket.clicked.connect(self.compra_venta)

    def compra_venta(self):
        self.senal_compra_venta.emit(self.sender().text())

    def update_tienda(self, data):
        mensaje, dict = data
        self.status.setText(mensaje)
