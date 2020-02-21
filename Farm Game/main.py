from PyQt5.QtWidgets import QApplication
from FrontEnd import (VentanaInicio, VentanaJuego,
                      VentanaMapa)
from ventana_inv_tienda import VentanaTienda, VentanaInventario
from stats import VentanaStats
from BackEnd import Juego
import sys
from time import sleep

def hook(type, value, traceback):
    print(type)
    print(traceback)
sys.__excepthook__ = hook

app = QApplication(sys.argv)

mapa = VentanaMapa()
inventario = VentanaInventario()
tienda = VentanaTienda()
stats = VentanaStats()
ventana_juego = VentanaJuego(inventario, tienda, stats, mapa)
ventana_inicio = VentanaInicio(ventana_juego)
ventana_inicio.show()

back_end = Juego()

# Se conectan las señales de front-end con el back-end.
ventana_inicio.enviar_mapa_signal.connect(back_end.mapa_juego.map_edit)
ventana_inicio.enviar_mapa_signal.connect(back_end.clock.start_timer)
back_end.mapa_juego.respuesta_mapa_signal.connect(ventana_juego.mapa.actualizar_mapa)
back_end.jugador.update_character_signal.connect(ventana_juego.mapa.actualizar_personaje)
ventana_juego.mapa.senal_tienda.connect(ventana_juego.abrir_tienda)
ventana_juego.mapa.info_mapa_signal.connect(back_end.jugador.info_mapa)
ventana_juego.enviar_char_signal.connect(back_end.jugador.mover_personaje)
ventana_juego.tienda.senal_compra_venta.connect(back_end.jugador.tienda)
back_end.jugador.update_inventario_signal.connect(ventana_juego.tienda.update_tienda)
back_end.jugador.update_inventario_signal.connect(ventana_juego.inventario.update_inventario)
ventana_juego.mapa.senal_fruto_recogido.connect(back_end.jugador.update_inventario)
back_end.clock.tiempo_signal.connect(ventana_juego.stats.actualizar_hora_fecha)
back_end.clock.tiempo_signal.connect(ventana_juego.mapa.celda_ocupada)
back_end.jugador.update_dinero_signal.connect(ventana_juego.stats.actualizar_dinero)
back_end.clock.aparicion_esp_signal.connect(ventana_juego.mapa.arbol_o_oro)
back_end.jugador.tiene_azada_signal.connect(ventana_juego.mapa.has_azada)
back_end.jugador.tiene_hacha_signal.connect(ventana_juego.mapa.has_hacha)
ventana_juego.mapa.energy_signal.connect(back_end.jugador.energy)
#back_end.clock.tiempo_signal.connect(ventana_juego.mapa.revisar_arado)
back_end.jugador.energia_update.connect(ventana_juego.stats.actualizar_energia)
ventana_juego.mapa.nuevo_dia_signal.connect(back_end.clock.nuevo_dia)
ventana_juego.dinero_trampa_signal.connect(back_end.jugador.dinero_trampa)
ventana_juego.energia_trampa_signal.connect(back_end.jugador.energia_trampa)
ventana_juego.stats.pausa_signal.connect(back_end.clock.pausa)
ventana_juego.stats.pausa_signal.connect(ventana_juego.pausa)
back_end.jugador.termino.connect(ventana_juego.fin)



sys.exit(app.exec())
