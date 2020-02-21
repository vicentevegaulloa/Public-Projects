from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QFrame,
                             QGraphicsScene, QGraphicsItem, QGraphicsView,
                             QGraphicsPixmapItem)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QThread, QTimer, QMutex)
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
from front_end_2 import (AparicionLabel, DropLabel, AparicionEspontanea,
                         ActMapa, Choclo, Alcachofa, Jugador)

class VentanaInicio(QWidget):

    enviar_mapa_signal = pyqtSignal(str)

    def __init__(self, ventana_juego = None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.juego = ventana_juego
        self.init_gui()

    def init_gui(self):
        self.setGeometry(500, 200, 700, 500)
        self.setFixedSize(700, 500)
        self.setWindowTitle('Inicio')
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        #Imagen
        self.foto = QLabel(self)
        self.foto.setGeometry(0,0, 600, 400)
        ruta_imagen = os.path.join('sprites_propias', 'DCCampo.png')
        pixeles = QPixmap(ruta_imagen).scaled(600, 400, Qt.KeepAspectRatio)
        self.foto.setPixmap(pixeles)
        self.foto.setScaledContents(False)
        #label ingresar mapa
        self.label = QLabel("Ingresa el mapa a cargar:",self)
        # edit
        self.edit = QLineEdit('', self)
        self.edit.setGeometry(45, 15, 100, 20)
        # boton
        self.boton_jugar = QPushButton("&Jugar",self)
        self.boton_jugar.clicked.connect(self.boton_jugar_clicked)
        self.boton_jugar.resize(self.boton_jugar.sizeHint())
        #layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.foto)
        vbox.addWidget(self.label)
        vbox.addWidget(self.edit)
        vbox.addWidget(self.boton_jugar)
        self.setLayout(vbox)

    def boton_jugar_clicked(self):
        mapa = self.edit.text()
        if os.path.exists(f"mapas/{mapa}") and mapa:
            hide = self.hide()
            self.juego.show()
            self.enviar_mapa_signal.emit(f"mapas/{mapa}")
        else:
            self.label.setText("Error al ingresar mapa. Prueba otra vez:")

class VentanaMapa(QWidget):
    energy_signal = pyqtSignal(int)
    info_mapa_signal = pyqtSignal(tuple)
    senal_collision = pyqtSignal(tuple)
    senal_tienda = pyqtSignal(bool)
    senal_fruto_recogido = pyqtSignal(str)
    tiene_axe = pyqtSignal(bool)
    tiene_hoe = pyqtSignal(bool)
    nuevo_dia_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.init_gui()
        self.map_threads = []
        self.mapa_base = []
        self.N = 30
        self.player = Jugador(self)
        self.player.setGeometry(20, 20, self.N, self.N)
        self.player.setVisible(True)
        self.tuplita = None
        self.cultivo = []
        self.apariciones = []
        self.mapa_espacio_libre = []
        self.tiene_hacha = False
        self.tiene_azada = False
        #self.lock = QMutex(self)

    def init_gui(self):
        self.resize(1150, 870)

    def arbol_o_oro(self, event):
        for celda in self.map_threads:
            if celda.tipo == DICT_SPRITES_MAP["O"] and not celda.aparicion:
                self.mapa_espacio_libre.append(celda)
        random_cell = random.choice(self.mapa_espacio_libre)
        self.mapa_espacio_libre = []
        ap_esp = AparicionEspontanea(self,
                                     event,
                                     random_cell.label.x(),
                                     random_cell.label.y(),
                                     random_cell.label.width(),
                                     random_cell.label.height())
        ap_esp.hacha_signal.connect(random_cell.hacha)
        random_cell.clicked_recurso_signal.connect(ap_esp.update_aparicion)
        random_cell.clicked_recurso_signal.connect(self.actualizar_energia)
        random_cell.aparicion = True
        self.apariciones.append(ap_esp)
    def has_hacha(self, data):
        self.tiene_hacha = data
        self.tiene_axe.emit(data)
    def has_azada(self, data):
        self.tiene_azada = data
        self.tiene_hoe.emit(data)

    def revisar_arado(self, data):
        if data[1]:
            for celda in self.map_threads:
                if celda.tipo == DICT_SPRITES_MAP["C"]:
                    self.lock()
                    celda.label.plantar_signal.connect(self.sembrar)
                    celda.label.descontar_inventario.connect(self.semilla_gastada)
                    self.unlock()
    def celda_ocupada(self, data):
        for celda in self.map_threads:
            for fruto in self.cultivo:
                if celda.label.box.intersects(fruto.box):
                    celda.label.sembrado = True

    def sembrar(self, data):
        tipo, x, y, w, h = data
        if tipo == "choclo":
            choclo = Choclo(self, x, y, w, h)
            choclo.resembrar_signal.connect(self.sembrar)
            self.cultivo.append(choclo)
            self.energy_signal.emit(-ENERGIA_COSECHAR)
        elif tipo == "alcachofa":
            alcachofa = Alcachofa(self, x, y, w, h)
            self.cultivo.append(alcachofa)
            self.energy_signal.emit(-ENERGIA_COSECHAR)
    def semilla_gastada(self, data):
        self.senal_fruto_recogido.emit(f"s_{data}")
    def actualizar_mapa(self, maps):
        H = DICT_SPRITES_MAP["H"]
        T = DICT_SPRITES_MAP["T"]
        for map in maps:

            self.N = calcular_N(self.width(), self.height(),
                       len(map[0]), len(map))
            for fila in range(len(map)):
                for columna in range(len(map[0])):
                    if map[fila][columna] == "E":
                        continue
                    elif map[fila][columna] == DICT_SPRITES_MAP["R"]:
                        self.map_threads.append(ActMapa(self, self.N, columna, fila,
                                                        map, solid=True,
                                                        tipo=map[fila][columna]))
                    elif map[fila][columna] == DICT_SPRITES_MAP["H"]:
                        self.map_threads.append(ActMapa(self, 2 * self.N, columna,
                                                        fila, map, H_o_T=True,
                                                        tipo=map[fila][columna]))
                    elif map[fila][columna] == DICT_SPRITES_MAP["T"]:
                        self.map_threads.append(ActMapa(self, 2 * self.N, columna,
                                                        fila, map, H_o_T=True,
                                                        tipo=map[fila][columna]))
                    elif map[fila][columna] == DICT_SPRITES_MAP["C"]:
                        celda = ActMapa(self, self.N, columna, fila, map,
                                        tipo=map[fila][columna])
                        self.map_threads.append(celda)
                    else:
                        if map == maps[0]:
                            celda = ActMapa(self, self.N, columna, fila, map, tipo="nada")
                            self.mapa_base.append(celda)
                            continue
                        celda = ActMapa(self, self.N, columna, fila, map, tipo=map[fila][columna])
                        self.tiene_axe.connect(celda.has_hacha)
                        self.tiene_hoe.connect(celda.has_azada)
                        celda.perder_energia_signal.connect(self.actualizar_energia)
                        celda.perder_energia_signal.connect(self.revisar_arado)
                        self.map_threads.append(celda)
        self.info_mapa_signal.emit((self.N * len(maps[1][0]), self.N * len(maps[1])))
        self.actualizar_personaje((0,0,  DICT_SPRITES_PERSONAJE[("right", 1)], "right"))

    def actualizar_personaje(self, data):
        #self.revisar_arado(("nada", True))
        self.player.resize(self.N * 0.5, self.N - 5)
        x, y, sprite, dir = data
        self.player.move(x, y)
        self.player.feet.setSize(QSize(self.player.width(), 1))
        self.player.feet.moveTo(x, y + self.player.height() - 1)
        pixmap = QPixmap(sprite).scaled(self.player.size(), Qt.IgnoreAspectRatio)
        self.player.setPixmap(pixmap)
        #self.player.setFrameShape(QFrame.Panel)
        #colision
        colision = False
        for item in self.map_threads:
            if item.solid == True and self.player.feet.intersects(item.label.box):
                colision = True
            elif (item.tipo == DICT_SPRITES_MAP["T"] and
                  self.player.feet.intersects(item.label.box)):
                self.senal_tienda.emit(True)
            elif (item.tipo == DICT_SPRITES_MAP["H"] and
                  self.player.feet.intersects(item.label.box)):
                self.energy_signal.emit(ENERGIA_INICIAL)
                self.nuevo_dia_signal.emit()

        self.tuplita = (dir, colision)
        #recoger fruto
        for fruto in self.cultivo:
            if fruto.fruto_box.intersects(self.player.feet):
                self.senal_fruto_recogido.emit(fruto.tipo)
                fruto.img.hide()
                fruto.fruto_box = QRect()
                self.energy_signal.emit(-ENERGIA_RECOGER)
        #recoger oro o leña
        for recurso in self.apariciones:
            if recurso.recurso_box.intersects(self.player.feet):
                self.senal_fruto_recogido.emit(recurso.tipo)
                recurso.img.hide()
                recurso.recurso_box = QRect()
                self.energy_signal.emit(-ENERGIA_RECOGER)
        self.senal_collision.emit(self.tuplita)
        self.player.raise_()
        self.player.show()

    def actualizar_energia(self, data):
        energia, bool = data
        self.energy_signal.emit(energia)

class VentanaJuego(QWidget):
    enviar_char_signal = pyqtSignal(tuple)
    dinero_trampa_signal = pyqtSignal()
    energia_trampa_signal = pyqtSignal()
    def __init__(self, inventario=None, tienda=None, stats=None,
                 mapa=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventario = VentanaInventario(self)
        self.stats = VentanaStats(self)
        self.mapa = VentanaMapa(self)
        self.tienda = VentanaTienda()
        self.tecla_bloqueada = None
        self.mapa.senal_collision.connect(self.bloquear_tecla)
        self.short_cut = set()
        self.stop = False
        self.init_gui()

    def init_gui(self):
        # Ajustamos la geometría de la ventana y su título
        self.setGeometry(0, 0, 1400, 1000)
        self.setFixedSize(1400, 1000)
        self.setWindowTitle('DCCampo')
        hbox0 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.inventario)
        vbox1.addWidget(self.mapa)
        hbox0.addLayout(vbox1)
        hbox0.addWidget(self.stats)
        self.setLayout(hbox0)

    def abrir_tienda(self):
        self.tienda.show()

    def bloquear_tecla(self, data):
        dir, colision = data
        if colision == True:
            if dir == "right":
                self.tecla_bloqueada = "d"
            elif dir == "left":
                self.tecla_bloqueada = "a"
            elif dir == "up":
                self.tecla_bloqueada = "w"
            elif dir == "down":
                self.tecla_bloqueada = "s"
        else:
            self.tecla_bloqueada = None

    def keyPressEvent(self, event):
        #print("press")
        if self.stop:
            return
        if event.text() in ["m", "n", "y", "k", "i", "p"]:
            self.short_cut.add(event.text())
        if self.short_cut == {"m", "n", "y"}:
            self.dinero_trampa_signal.emit()
        elif self.short_cut == {"k", "i", "p"}:
            self.energia_trampa_signal.emit()
        if event.text() == "d" and event.text() != self.tecla_bloqueada:
            self.enviar_char_signal.emit(("right",))
        elif event.text() == "a" and event.text() != self.tecla_bloqueada:
            self.enviar_char_signal.emit(("left",))
        elif event.text() == "w" and event.text() != self.tecla_bloqueada:
            self.enviar_char_signal.emit(("up",))
        elif event.text() == "s" and event.text() != self.tecla_bloqueada:
            self.enviar_char_signal.emit(("down",))
    def keyReleaseEvent(self, event):
        #print("realease")
        if event.text() in ["m", "n", "y", "k", "i", "p"]:
            self.short_cut.remove(event.text())

    def pausa(self, event):
        self.stop = event

    def fin(self, event):
        if event:
            FinJuego(text ="GANASTE")
            self.close()
        else:
            FinJuego(text ="Perdiste :c")
            self.close()

class FinJuego(QWidget):
    def __init__(self, text = None ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.text = text
    def init_gui(self):

        self.setGeometry(200, 100, 200, 300)
        self.setWindowTitle('Ventana con botón')

        self.label = QLabel("FIN DELJUEGO", self)

        # Una vez que fueron agregados todos los elementos a la ventana la
        # desplegamos en pantalla
        self.show()
