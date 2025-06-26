import pygame
import random

# ——————————————
# Constantes de cartas
# ——————————————
PALOS = ("basto", "copa", "espada", "oro")
COLOR_PALOS = {
    "espada": "negro",
    "basto":  "negro",
    "copa":   "rojo",
    "oro":    "rojo"
}
RUTA_REVERSO = "recursos/img/reverso.jpg"

# ——————————————
# Funciones de mazo
# ——————————————
def crear_carta(ruta_imagen: str, palo: str, numero: int) -> dict:
    """
    Crea la ficha de datos de una carta *y* su superficie Pygame escalada.
    """
    # 1) cargo y escalo la imagen
    superficie = pygame.image.load(ruta_imagen)
    superficie = pygame.transform.scale(superficie, (70, 120))

    # 2) devuelvo el dict con la superficie incluida
    return {
        "superficie":   superficie,
        "ruta_imagen":  ruta_imagen,
        "palo":         palo,
        "numero":       numero,
        "boca_arriba":  False,
    }

def barajar_mazo() -> list[dict]:
    base = "recursos/img/cartas/"
    cartas = []
    for palo in PALOS:
        for num in range(1, 11):
            nombre = f"{num} de {palo}.jpg"
            cartas.append(crear_carta(base + nombre, palo, num))
    random.shuffle(cartas)
    return cartas


def repartir_juego() -> dict:
    mazo = barajar_mazo()
    pilas_cuadro = []
    for _ in range(7):
        pilas_cuadro.append([])
    pilas_cimientos = []
    for _ in range(4):
        pilas_cimientos.append([])

    idx = 0
    for i in range(7):
        for j in range(i + 1):
            carta = mazo[idx]
            carta["boca_arriba"] = (j == i)
            pilas_cuadro[i].append(carta)
            idx += 1

    monton = []
    for k in range(idx, len(mazo)):
        monton.append(mazo[k])

    return {
        "pilas_cuadro":    pilas_cuadro,
        "pilas_cimientos": pilas_cimientos,
        "monton":          monton,
        "descarte":        []
    }

def obtener_color_palo(palo: str) -> str:
    return COLOR_PALOS.get(palo, "desconocido")