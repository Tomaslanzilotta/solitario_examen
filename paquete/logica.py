import pygame
from paquete.funciones import obtener_color_palo

def click_en_mazo(mi_mazo: dict) -> None:
    if mi_mazo["monton"]:
        carta = mi_mazo["monton"].pop()
        carta["boca_arriba"] = True
        mi_mazo["descarte"].append(carta)
    else:
        nuevas = []
        for carta in reversed(mi_mazo["descarte"]):
            nuevas.append(carta)
        mi_mazo["monton"] = nuevas
        for carta in mi_mazo["monton"]:
            carta["boca_arriba"] = False
        mi_mazo["descarte"].clear()

def intentar_mover_descarte_a_pilas(mi_mazo: dict) -> None:
    if not mi_mazo["descarte"]:
        return
    carta_desc = mi_mazo["descarte"][-1]
    for pila in mi_mazo["pilas_cuadro"]:
        if pila:
            tope = pila[-1]
            if (carta_desc["numero"] == tope["numero"] - 1
                and obtener_color_palo(carta_desc["palo"]) != obtener_color_palo(tope["palo"])):
                pila.append(mi_mazo["descarte"].pop())
                return
        else:
            if carta_desc["numero"] == 10:
                pila.append(mi_mazo["descarte"].pop())
                return

def seleccionar_bloque(mi_mazo: dict, mouse_x: int, mouse_y: int) -> tuple[list[dict], int | None]:
    for idx_col, pila in enumerate(mi_mazo["pilas_cuadro"]):
        x_col = 50 + idx_col * 120
        for idx_carta, carta in enumerate(pila):
            y = 200 + idx_carta * 25
            rect = pygame.Rect(x_col, y, 70, 120)
            if carta.get("boca_arriba", False) and rect.collidepoint(mouse_x, mouse_y):
                return pila[idx_carta:], idx_col
    return [], None

def destapar_tope_si_corresponde(pilas_cuadro: list[list[dict]], indice: int) -> None:
    pila = pilas_cuadro[indice]
    if pila and not pila[-1].get("boca_arriba", False):
        pila[-1]["boca_arriba"] = True

def mover_bloque(mi_mazo: dict, bloque: list[dict], origen: int, mouse_x: int, mouse_y: int) -> tuple[list[dict], int | None]:
    if not bloque:
        return [], None
    carta_sup = bloque[0]
    columnas = mi_mazo["pilas_cuadro"]
    for i, pila_dest in enumerate(columnas):
        x_min = 50 + i * 120
        if x_min <= mouse_x <= x_min + 70 and mouse_y >= 200:
            if i == origen:
                break
            if pila_dest:
                tope = pila_dest[-1]
                if (tope.get("boca_arriba", False)
                    and carta_sup["numero"] == tope["numero"] - 1
                    and obtener_color_palo(carta_sup["palo"]) != obtener_color_palo(tope["palo"])):
                    for c in bloque:
                        columnas[origen].remove(c)
                        pila_dest.append(c)
                    destapar_tope_si_corresponde(columnas, origen)
                    return [], None
            else:
                if carta_sup["numero"] == 10:
                    for c in bloque:
                        columnas[origen].remove(c)
                        pila_dest.append(c)
                    destapar_tope_si_corresponde(columnas, origen)
                    return [], None
    return bloque, origen