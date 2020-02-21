from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
from os.path import join
import random
from parametros import (DICT_SPRITES_MAP, VEL_MOVIMIENTO, DICT_SPRITES_PERSONAJE,
                              MONEDAS_INICIALES, MINUTO, PROB_ORO, PROB_ARBOL,
                              DURACION_ORO, DURACION_LEÑA, ENERGIA_INICIAL, DINERO_TRAMPA)
from formulas import evento_ocurre
import parametros_precios
import parametros_plantas

class Juego(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapa_juego = Mapa()
        self.clock = Clock()
        self.jugador = Jugador()

class Mapa(QObject):
    respuesta_mapa_signal = pyqtSignal(tuple)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapa = None
        self.O = None
        self.mapa_sprites = None

    def map_edit(self, mapa_recibido):
        with open(f"{mapa_recibido}", "r", encoding="utf-8") as file:
            self.mapa = [line.strip().split(" ") for line in file.readlines()]
            count_H = 0
            count_T = 0
            for f in range(len(self.mapa)):
                for c in range(len(self.mapa[0])):
                    if self.mapa[f][c] == "H" and count_H == 0:
                        count_H += 1
                        continue
                    elif self.mapa[f][c] == "H" and count_H > 0:
                        self.mapa[f][c] = "E"
                    elif self.mapa[f][c] == "T" and count_T == 0:
                        count_T += 1
                        continue
                    elif self.mapa[f][c] == "T" and count_T > 0:
                        self.mapa[f][c] = "E"
            self.O = [[DICT_SPRITES_MAP["O"] for i in line] for line in self.mapa]
            self.mapa_sprites = [[DICT_SPRITES_MAP[i] for i in line] for line in self.mapa]
            self.respuesta_mapa_signal.emit((self.O, self.mapa_sprites))

class Jugador(QObject):
    enzo_muerto_signal = pyqtSignal()
    energia_update = pyqtSignal(int)
    tiene_hacha_signal = pyqtSignal(bool)
    tiene_azada_signal = pyqtSignal(bool)
    update_inventario_signal = pyqtSignal(tuple)
    update_character_signal = pyqtSignal(tuple)
    update_dinero_signal= pyqtSignal(int)
    termino = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._etapa = 1
        self.direccion = "left"
        self.sprite = DICT_SPRITES_PERSONAJE[(self.direccion, self._etapa)]
        self._x = 0
        self._y = 0
        self.limit_x = 0
        self.limit_y = 0
        self._energia = ENERGIA_INICIAL
        self.blocked = None
        self.dinero = MONEDAS_INICIALES
        self.inventario = {"ALCACHOFA": 0,
                           "CHOCLO": 0,
                           "LEÑA": 0,
                           "ORO": 0,
                           "AZADA": 0,
                           "HACHA": 0,
                           "SEMILLAS ALCACHOFA": 0,
                           "SEMILLAS CHOCLO": 0}

    @property
    def energia(self):
        return self._energia
    @energia.setter
    def energia(self, p):
        if p < 0:
            self._energia = 0
            self.enzo_muerto_signal.emit()
        elif p > ENERGIA_INICIAL:
            self._energia = ENERGIA_INICIAL
            self.energia_update.emit(ENERGIA_INICIAL)
        else:
            self._energia = p
            self.energia_update.emit(p)

    @property
    def etapa(self):
        return self._etapa
    @etapa.setter
    def etapa(self, p):
        if p > 4:
            self._etapa = 1
        else:
            self._etapa = p
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, p):
        if p > self.limit_x:
            self._x = self.limit_x
        elif p < 0:
            self._x = 0
        else:
            self._x = p
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, p):
        if p > self.limit_y:
            self._y = self.limit_y
        elif p < 0:
            self._y = 0
        else:
            self._y = p

    def tienda(self, data):
        if "Vender" in data:
            mensaje = ""
            data = data.replace("Vender","")
            data = data.strip().replace(" ","_")
            if data == "ALCACHOFAS" and self.inventario["ALCACHOFA"] > 0:
                self.dinero += parametros_precios.PRECIO_ALACACHOFAS
                self.inventario["ALCACHOFA"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "CHOCLOS" and self.inventario["CHOCLO"] > 0:
                self.dinero += parametros_precios.PRECIO_CHOCLOS
                self.inventario["CHOCLO"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "LEÑA" and self.inventario["LEÑA"] > 0:
                self.dinero += parametros_precios.PRECIO_LEÑA
                self.inventario["LEÑA"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "ORO" and self.inventario["ORO"] > 0:
                self.dinero += parametros_precios.PRECIO_ORO
                self.inventario["ORO"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "SEMILLA_ALCACHOFA" and self.inventario["SEMILLAS ALCACHOFA"] > 0:
                self.dinero += parametros_precios.PRECIO_SEMILLA_ALCACHOFAS
                self.inventario["SEMILLAS ALCACHOFA"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "SEMILLA_CHOCLO" and self.inventario["SEMILLAS CHOCLO"] > 0:
                self.dinero += parametros_precios.PRECIO_SEMILLA_CHOCLOS
                self.inventario["SEMILLAS CHOCLO"] -= 1
                mensaje = "Articulo vendido!"
            elif data == "HACHA" and self.inventario["HACHA"] > 0:
                self.dinero += parametros_precios.PRECIO_HACHA
                self.inventario["HACHA"] -= 1
                self.tiene_hacha_signal.emit(False)
                mensaje = "Articulo vendido!"
            elif data == "AZADA" and self.inventario["AZADA"] > 0:
                self.dinero += parametros_precios.PRECIO_AZADA
                self.inventario["AZADA"] -= 1
                self.tiene_azada_signal.emit(False)
                mensaje = "Articulo vendido!"
            else:
                mensaje = "No puedes vender un elemento que no tienes"
        elif "Comprar" in data:
            data = data.replace("Comprar","")
            data = data.strip().replace(" ","_")
            if data == "SEMILLA_ALCACHOFA" and self.dinero >= parametros_precios.PRECIO_SEMILLA_ALCACHOFAS:
                self.dinero -= parametros_precios.PRECIO_SEMILLA_ALCACHOFAS
                self.inventario["SEMILLAS ALCACHOFA"] += 1
                mensaje = "Articulo comprado!"
            elif data == "SEMILLA_CHOCLO" and self.dinero >= parametros_precios.PRECIO_SEMILLA_CHOCLOS:
                self.dinero -= parametros_precios.PRECIO_SEMILLA_CHOCLOS
                self.inventario["SEMILLAS CHOCLO"] += 1
                mensaje = "Articulo comprado!"
            elif data == "HACHA" and self.dinero >= parametros_precios.PRECIO_HACHA and self.inventario["HACHA"] < 1:
                self.dinero -= parametros_precios.PRECIO_HACHA
                self.inventario["HACHA"] += 1
                self.tiene_hacha_signal.emit(True)
                mensaje = "Articulo comprado!"
            elif data == "AZADA" and self.dinero >= parametros_precios.PRECIO_AZADA and self.inventario["AZADA"] < 1:
                self.dinero -= parametros_precios.PRECIO_AZADA
                self.inventario["AZADA"] += 1
                self.tiene_azada_signal.emit(True)
                mensaje = "Articulo comprado!"
            elif data == "TICKET" and self.dinero >= parametros_precios.PRECIO_TICKET:
                self.dinero -= parametros_precios.PRECIO_TICKET
                mensaje = "Articulo comprado!"
                self.termino.emit(True)
            else:
                mensaje = "No puedes comprar este articulo"
        self.update_inventario_signal.emit((mensaje, self.inventario))
        self.update_dinero_signal.emit(self.dinero)
    def info_mapa(self, data):
        self.limit_x = data[0]
        self.limit_y = data[1]

    def energy(self, data):
        self.energia += data

    def mover_personaje(self, tuple):
        if len(tuple) == 1:
            accion = tuple[0]
        self.etapa += 1
        self.direccion = accion
        self.sprite = DICT_SPRITES_PERSONAJE[(self.direccion, self.etapa)]
        if self.direccion == "left":
            self.x -= VEL_MOVIMIENTO
        elif self.direccion == "right":
            self.x += VEL_MOVIMIENTO
        elif self.direccion == "up":
            self.y -= VEL_MOVIMIENTO
        elif self.direccion == "down":
            self.y += VEL_MOVIMIENTO
        self.update_character_signal.emit((self.x,
                                           self.y,
                                           self.sprite,
                                           self.direccion))

    def update_inventario(self, item):
        if item == "choclo":
            self.inventario["CHOCLO"] += parametros_plantas.COSECHA_CHOCLOS
        elif item == "alcachofa":
            self.inventario["ALCACHOFA"] += parametros_plantas.COSECHA_ALCACHOFAS
        elif item == "s_choclo":
            self.inventario["SEMILLAS CHOCLO"] -= 1
        elif item == "s_alcachofa":
            self.inventario["SEMILLAS ALCACHOFA"] -= 1
        elif item == "arbol":
            self.inventario["LEÑA"] += 1
        elif item == "oro":
            self.inventario["ORO"] += 1
        self.update_inventario_signal.emit(("", self.inventario))

    def dinero_trampa(self):
        self.dinero += DINERO_TRAMPA
        self.update_dinero_signal.emit(self.dinero)

    def energia_trampa(self):
        self.energia += ENERGIA_INICIAL

class Choclo(QThread):
    stage_up_signal = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intervalo = parametros_plantas.TIEMPO_CHOCLOS * 1000
        self.timer = QTimer(self)
        self.timer.setInterval(self.intervalo)
        self.timer.timeout.connect(self.stage_up)
        self.timer.start()
        self._stage = 1
    @property
    def stage(self):
        return self._stage
    @stage.setter
    def stage(self, p):
        if p > parametros_plantas.FASES_CHOCLOS:
            self.stage_up_signal.emit(0)
            self.timer.stop()
        else:
            self._stage = p
            self.stage_up_signal.emit(p)

    def stage_up(self):
        self.stage += 1

class Alcachofa(QThread):
    stage_up_signal = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intervalo = parametros_plantas.TIEMPO_ALCACHOFAS * 1000
        self.timer = QTimer(self)
        self.timer.setInterval(self.intervalo)
        self.timer.timeout.connect(self.stage_up)
        self.timer.start()
        self._stage = 1
    @property
    def stage(self):
        return self._stage
    @stage.setter
    def stage(self, p):
        if p > parametros_plantas.FASES_ALCACHOFAS:
            self.stage_up_signal.emit(0)
            self.timer.stop()
        else:
            self._stage = p
            self.stage_up_signal.emit(p)

    def stage_up(self):
        self.stage += 1

class AparicionEspontanea(QObject):
    timer_signal = pyqtSignal()
    def __init__(self, tipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = tipo
        self.timer = QTimer(self)
        if self.tipo == "arbol":
            self.timer.setInterval(DURACION_LEÑA * MINUTO)
        elif self.tipo == "oro":
            self.timer.setInterval(DURACION_ORO * MINUTO)
        self.timer.timeout.connect(self.tiempo)
    def timer_accion(self, event):
        if event:
            self.timer.start()
        else:
            self.timer.stop()
    def tiempo(self):
        self.timer_signal.emit()

class Clock(QObject):
    tiempo_signal = pyqtSignal(tuple)
    aparicion_esp_signal = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.timer.setInterval(MINUTO)
        self.timer.timeout.connect(self.tiempo)
        self._minuto = 0
        self._hora = 0
        self.dia = 0
    def start_timer(self, data):
        self.timer.start()
    @property
    def minuto(self):
        return self._minuto
    @minuto.setter
    def minuto(self, p):
        if p >= 60:
            self._minuto = 0
            self.hora += 1
        else:
            self._minuto = p
    @property
    def hora(self):
        return self._hora
    @hora.setter
    def hora(self, p):
        if p >= 24:
            self._hora = 0
            self.dia += 1
            self.aparicion_espontanea()
        else:
            self._hora = p

    def aparicion_espontanea(self):
        self.aparicion_esp_signal.emit(evento_ocurre(PROB_ARBOL, PROB_ORO))

    def tiempo(self):
        self.minuto += 1
        self.tiempo_signal.emit((self.dia, self.hora, self.minuto))

    def nuevo_dia(self):
        self.hora = 23
        self.minuto = 59
        self.tiempo_signal.emit((self.dia, self.hora, self.minuto))

    def pausa(self, event):
        if event:
            self.timer.stop()
        else:
            self.timer = QTimer(self)
            self.timer.setInterval(MINUTO)
            self.timer.timeout.connect(self.tiempo)
            self.timer.start()
