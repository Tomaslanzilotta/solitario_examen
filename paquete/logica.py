import pygame
from paquete.funciones import obtener_color_palo

def click_en_mazo(mi_mazo: dict) -> None:
    """
    Toma la carta superior del montón y la pone en el descarte.
    Si el montón está vacío, recarga las cartas del descarte al montón.

    Param mi_mazo: diccionario con llaves
        - "monton": lista de cartas boca abajo
        - "descarte": lista de cartas boca arriba
    Return: None
    """
    if mi_mazo["monton"]:
        carta = mi_mazo["monton"].pop()
        carta["boca_arriba"] = True
        mi_mazo["descarte"].append(carta)
    else:
        # Reciclar todas las cartas del descarte al montón
        while mi_mazo["descarte"]:
            c = mi_mazo["descarte"].pop()
            c["boca_arriba"] = False
            mi_mazo["monton"].append(c)

def intentar_mover_descarte_a_pilas(mi_mazo: dict) -> None:
    """
    Intenta colocar la carta del descarte en alguna de las columnas válidas.

    Param mi_mazo: diccionario con llaves
        - "descarte": lista de cartas boca arriba
        - "pilas_cuadro": lista de 7 columnas, cada una es lista de cartas
    Return: None (modifica mi_mazo directamente)
    """
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
            # Pila vacía sólo acepta un 10
            if carta["numero"] == 10:
                mi_mazo["descarte"].pop()
                pila.append(carta)
                return

def seleccionar_bloque(mi_mazo: dict, mx: int, my: int) -> tuple:
    """
    Dado un clic en (mx, my), encuentra la pila y sub-bloque arrastrable.

    Param mi_mazo: diccionario con "pilas_cuadro"
    Param mx: posición X del mouse
    Param my: posición Y del mouse
    Return: (bloque, índice_columna) donde bloque es lista de cartas,
            o (None, None) si no se clickeó nada válido.
    """
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
    """
    Si en la columna indicada la carta de tope está boca abajo, la voltea.

    Param pilas_cuadro: lista de columnas (listas de cartas)
    Param indice: índice de la columna a chequear
    Return: None
    """
    if not pilas_cuadro[indice]:
        return
    tope = pilas_cuadro[indice][-1]
    if not tope["boca_arriba"]:
        tope["boca_arriba"] = True

def mover_bloque(mi_mazo: dict, bloque: list, origen: int,
                mx: int, my: int) -> tuple:
    """
    Intenta soltar 'bloque' arrastrado en una columna válida.
    Si se mueve con éxito:
    - elimina el bloque de la columna de origen
    - lo añade a la columna destino
    - destapa la carta tope en la columna origen
    - devuelve ([], None)
    Si no, conserva (bloque, origen).

    Param mi_mazo: diccionario con "pilas_cuadro"
    Param bloque: lista de cartas arrastradas
    Param origen: índice de la columna origen
    Param mx, my: posición del mouse al soltar
    Return: tupla (nuevo_bloque, nuevo_origen)
    """
    for i, pila in enumerate(mi_mazo["pilas_cuadro"]):
        x = 50 + i * 120
        y = 200 + (len(pila) * 25 if pila else 0)
        rect = pygame.Rect(x, y, 70, 120)

        if rect.collidepoint(mx, my):
            carta_sup = bloque[0]
            # Pila no vacía: mismo control que en intentar_mover_descarte
            if pila:
                tope = pila[-1]
                if (tope["boca_arriba"]
                    and carta_sup["numero"] == tope["numero"] - 1
                    and obtener_color_palo(carta_sup["palo"]) != obtener_color_palo(tope["palo"])):
                    # Mover bloque
                    mi_mazo["pilas_cuadro"][origen] = mi_mazo["pilas_cuadro"][origen][:-len(bloque)]
                    pila.extend(bloque)
                    destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], origen)
                    return [], None
            else:
                # Pila vacía sólo acepta un 10
                if carta_sup["numero"] == 10:
                    mi_mazo["pilas_cuadro"][origen] = mi_mazo["pilas_cuadro"][origen][:-len(bloque)]
                    pila.extend(bloque)
                    destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], origen)
                    return [], None

    return bloque, origen

def intentar_mover_a_fundacion(mi_mazo: dict, carta: dict) -> bool:
    """
    Intenta colocar la carta en una de las 4 fundaciones según reglas:
    - As (1) en fundación vacía
    - Misma pinta y número consecutivo en fundación no vacía

    Param mi_mazo: diccionario con "pilas_cimientos"
    Param carta: carta a mover (dict con "palo" y "numero")
    Return: True si se movió, False de lo contrario
    """
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
    """
    Toma la carta superior de la fundación indicada y la mueve a 
    una columna si es un movimiento válido (igual que en columnas).

    Param mi_mazo: diccionario con "pilas_cimientos" y "pilas_cuadro"
    Param indice_fundacion: índice de la fundación (0–3)
    Return: None
    """
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

def finalizar_partida(pantalla: pygame.Surface,
                    nombre: str, puntaje: int) -> None:
    """
    Muestra un cartel de victoria, pausa 2.5s y guarda el puntaje.

    Param pantalla: superficie de Pygame para dibujar el mensaje.
    Param nombre: nombre del jugador
    Param puntaje: puntos obtenidos en la partida
    Return: None
    """
    fuente = pygame.font.SysFont(None, 60)
    texto = fuente.render("¡Victoria!", True, (255, 255, 0))
    subtxt = pygame.font.SysFont(None, 36).render(
        f"{nombre} obtuvo {puntaje} puntos", True, (200, 255, 200)
    )

    pantalla.fill((0, 100, 0))
    pantalla.blit(texto, (380, 280))
    pantalla.blit(subtxt, (340, 360))
    pygame.display.update()
    pygame.time.wait(2500)

    with open("ranking.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre}, {puntaje}\n")

def jugador_gano(mi_mazo: dict) -> bool:
    """
    Determina si las 4 fundaciones están completas (10 cartas cada una).

    Param mi_mazo: diccionario con "pilas_cimientos"
    Return: True si todas las fundaciones tienen 10 cartas.
    """
    # Reemplaza el generator expression por un bucle explícito
    for fund in mi_mazo["pilas_cimientos"]:
        if len(fund) != 10:
            return False
    return True