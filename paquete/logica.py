import pygame
from paquete.funciones import obtener_color_palo

# ——————————————
# Robar y reciclar
# ——————————————

def click_en_mazo(mi_mazo: dict) -> None:
    if mi_mazo["monton"]:
        carta = mi_mazo["monton"].pop()
        carta["boca_arriba"] = True
        mi_mazo["descarte"].append(carta)
    else:
        while mi_mazo["descarte"]:
            c = mi_mazo["descarte"].pop()
            c["boca_arriba"] = False
            mi_mazo["monton"].append(c)

# ——————————————
# Descarte → columnas
# ——————————————

def intentar_mover_descarte_a_pilas(mi_mazo: dict) -> None:
    if not mi_mazo["descarte"]:
        return

    carta = mi_mazo["descarte"][-1]
    for pila in mi_mazo["pilas_cuadro"]:
        if pila:
            tope = pila[-1]
            if (tope["boca_arriba"]
                and carta["numero"] == tope["numero"] - 1
                and obtener_color_palo(carta["palo"]) != obtener_color_palo(tope["palo"])):
                mi_mazo["descarte"].pop()
                pila.append(carta)
                return
        else:
            if carta["numero"] == 10:
                mi_mazo["descarte"].pop()
                pila.append(carta)
                return

# ——————————————
# Selección y arrastre
# ——————————————

def seleccionar_bloque(mi_mazo: dict, mx: int, my: int):
    for i, pila in enumerate(mi_mazo["pilas_cuadro"]):
        for j, carta in enumerate(pila):
            if not carta["boca_arriba"]:
                continue
            x = 50 + i * 120
            y = 200 + j * 25
            rect = pygame.Rect(x, y, 70, 120)
            if rect.collidepoint(mx, my):
                return pila[j:], i
    return None, None

def destapar_tope_si_corresponde(pilas_cuadro: list, indice: int) -> None:
    if not pilas_cuadro[indice]:
        return
    tope = pilas_cuadro[indice][-1]
    if not tope["boca_arriba"]:
        tope["boca_arriba"] = True

def mover_bloque(mi_mazo: dict, bloque: list, origen: int, mx: int, my: int):
    """
    Intenta mover 'bloque' a una columna válida. Si lo logra:
    - lo elimina de la columna de origen
    - lo añade a la nueva columna
    - destapa la nueva carta tope en la columna de origen, si estaba boca abajo

    Devuelve ([], None) si se movió correctamente, o (bloque, origen) si falló.
    """
    for i, pila in enumerate(mi_mazo["pilas_cuadro"]):
        x = 50 + i * 120
        y = 200 + (len(pila) * 25 if pila else 0)
        rect = pygame.Rect(x, y, 70, 120)

        if rect.collidepoint(mx, my):
            carta_sup = bloque[0]

            if pila:
                tope = pila[-1]
                if (tope["boca_arriba"]
                    and carta_sup["numero"] == tope["numero"] - 1
                    and obtener_color_palo(carta_sup["palo"]) != obtener_color_palo(tope["palo"])):
                    # mover y destapar
                    mi_mazo["pilas_cuadro"][origen] = mi_mazo["pilas_cuadro"][origen][:-len(bloque)]
                    pila.extend(bloque)
                    destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], origen)
                    return [], None

            else:
                if carta_sup["numero"] == 10:
                    mi_mazo["pilas_cuadro"][origen] = mi_mazo["pilas_cuadro"][origen][:-len(bloque)]
                    pila.extend(bloque)
                    destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], origen)
                    return [], None

    return bloque, origen

# ——————————————
# Fundaciones
# ——————————————

def intentar_mover_a_fundacion(mi_mazo: dict, carta: dict) -> bool:
    for fund in mi_mazo["pilas_cimientos"]:
        if not fund:
            if carta["numero"] == 1:
                fund.append(carta)
                return True
        else:
            tope = fund[-1]
            if carta["palo"] == tope["palo"] and carta["numero"] == tope["numero"] + 1:
                fund.append(carta)
                return True
    return False

def mover_desde_fundacion_a_pila(mi_mazo: dict, indice_fundacion: int) -> None:
    fund = mi_mazo["pilas_cimientos"][indice_fundacion]
    if not fund:
        return

    carta = fund[-1]
    for pila in mi_mazo["pilas_cuadro"]:
        if pila:
            tope = pila[-1]
            if (tope["boca_arriba"]
                and carta["numero"] == tope["numero"] - 1
                and obtener_color_palo(carta["palo"]) != obtener_color_palo(tope["palo"])):
                fund.pop()
                pila.append(carta)
                return
        else:
            if carta["numero"] == 10:
                fund.pop()
                pila.append(carta)
                return