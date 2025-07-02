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

def crear_carta(ruta_imagen: str, palo: str, numero: int) -> dict:
    """
    Crea una carta cargando y escalando su imagen para Pygame.

    Param ruta_imagen: ruta al archivo de imagen de la carta.
    Param palo: uno de los valores en PALOS ('basto','copa','espada','oro').
    Param numero: valor numérico de la carta (1–10).
    Return: diccionario con claves:
      - 'superficie': Surface de Pygame (70×120).
      - 'ruta_imagen': ruta original de la imagen.
    - 'palo': palo de la carta.
    - 'numero': número de la carta.
    - 'boca_arriba': False por defecto.
    """
    superficie = pygame.image.load(ruta_imagen)
    superficie = pygame.transform.scale(superficie, (70, 120))

    return {
        "superficie":   superficie,
        "ruta_imagen":  ruta_imagen,
        "palo":         palo,
        "numero":       numero,
        "boca_arriba":  False
    }

def barajar_mazo() -> list:
    """
    Genera y mezcla las 40 cartas de un mazo de Klondike.

    Crea cartas para cada combinación de palo y número,
    luego mezcla la lista al azar.

    Return: lista de diccionarios de cartas barajadas.
    """
    base = "recursos/img/cartas/"
    cartas = []
    for palo in PALOS:
        for num in range(1, 11):
            nombre = f"{num} de {palo}.jpg"
            cartas.append(crear_carta(base + nombre, palo, num))

    random.shuffle(cartas)
    return cartas

def repartir_juego() -> dict:
    """
    Distribuye las cartas para iniciar una partida de Klondike.

    - Crea 7 columnas en 'pilas_cuadro' con reparto escalonado.
    - Crea 4 pilas vacías en 'pilas_cimientos' (fundaciones).
    - Rellena 'monton' con las cartas restantes boca abajo.
    - Deja 'descarte' vacío para el uso del jugador.

    Return: diccionario con llaves
    - 'pilas_cuadro': lista de 7 listas de cartas.
    - 'pilas_cimientos': lista de 4 listas de cartas.
    - 'monton': lista de cartas boca abajo.
    - 'descarte': lista vacía para cartas boca arriba.
    """
    mazo = barajar_mazo()

    # Columnas del cuadro
    pilas_cuadro = []
    for _ in range(7):
        pilas_cuadro.append([])

    # Fundaciones
    pilas_cimientos = []
    for _ in range(4):
        pilas_cimientos.append([])

    idx = 0
    # Reparto escalonado para el cuadro
    for i in range(7):
        for j in range(i + 1):
            carta = mazo[idx]
            carta["boca_arriba"] = (j == i)
            pilas_cuadro[i].append(carta)
            idx += 1

    # Resto de cartas al montón
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
    """
    Devuelve el color asociado a un palo de cartas.

    Param palo: nombre del palo (clave en COLOR_PALOS).
    Return: 'rojo', 'negro' o 'desconocido' si no existe.
    """
    return COLOR_PALOS.get(palo, "desconocido")