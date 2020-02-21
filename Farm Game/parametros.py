

DICT_SPRITES_MAP = {"H": "sprites/mapa/house.png",
                    "O": "sprites/mapa/tile006.png",
                    "C": "sprites/mapa/tile004.png",
                    "R": "sprites/mapa/tile087.png",
                    "T": "sprites/mapa/store.png",
                    "E": "E"}

DICT_SPRITES_PERSONAJE = {("left", 1): "sprites/personaje/left_1.png",
                          ("left", 2): "sprites/personaje/left_2.png",
                          ("left", 3): "sprites/personaje/left_3.png",
                          ("left", 4): "sprites/personaje/left_4.png",
                          ("right", 1): "sprites/personaje/right_1.png",
                          ("right", 2): "sprites/personaje/right_2.png",
                          ("right", 3): "sprites/personaje/right_3.png",
                          ("right", 4): "sprites/personaje/right_4.png",
                          ("up", 1): "sprites/personaje/up_1.png",
                          ("up", 2): "sprites/personaje/up_2.png",
                          ("up", 3): "sprites/personaje/up_3.png",
                          ("up", 4): "sprites/personaje/up_4.png",
                          ("down", 1): "sprites/personaje/down_1.png",
                          ("down", 2): "sprites/personaje/down_2.png",
                          ("down", 3): "sprites/personaje/down_3.png",
                          ("down", 4): "sprites/personaje/down_4.png",}
def calcular_N(w_width, w_height, col_map, fil_map):
    if (w_height / fil_map) < (w_width/col_map):
        N = (w_height / fil_map)
        return N
    else:
        N = (w_width/col_map)
        return N

VEL_MOVIMIENTO = 20

MONEDAS_INICIALES = 100

#minuto en milisegundos
MINUTO = 10

PROB_ARBOL = 0.5
PROB_ORO = 0.5

DURACION_LEÑA = 50
DURACION_ORO = 500
ENERGIA_INICIAL = 100
DINERO_TRAMPA = 200
