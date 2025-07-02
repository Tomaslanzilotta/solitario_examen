import pygame
import random
import time
import sys
from paquete.funciones import repartir_juego
from paquete.graficos  import *
from paquete.audio     import *
from paquete.logica    import *

pygame.init()
pantalla = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Solitario Klondike")
inicializar_audio("recursos/Balatro Main Theme.mp3", 0.5)
random.seed(time.time())

while True:
    musica_activada = mostrar_menu(pantalla, True)

    # ——————————————
    # Configurar nueva partida
    # ——————————————
    mi_mazo = repartir_juego()
    img_reverso = pygame.image.load(ruta_reverso)
    img_reverso = pygame.transform.scale(img_reverso, (70, 120))

    # Íconos de sonido en juego
    icono_on  = pygame.image.load(RUTA_ON)
    icono_off = pygame.image.load(RUTA_OFF)
    icono_on  = pygame.transform.scale(icono_on,  (40, 40))
    icono_off = pygame.transform.scale(icono_off, (40, 40))
    rect_sonido = pygame.Rect(20, 640, 40, 40)

    # Rects de interacción
    rect_monton   = pygame.Rect(50,  30, 70, 120)
    rect_descarte = pygame.Rect(140, 30, 70, 120)

    rects_fundacion = []
    for k in range(4):
        x_f = 400 + k * 90
        y_f = 30
        rects_fundacion.append(pygame.Rect(x_f, y_f, 70, 120))

    # Estado de arrastre
    bloque_seleccionado = []
    indice_origen       = None
    drag_en_progreso    = False
    posicion_mouse      = (0, 0)

    ejecutando = True
    while ejecutando:
        # — Procesar eventos —
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mx, my = evento.pos

                # 1) Toggle sonido
                if rect_sonido.collidepoint(mx, my):
                    musica_activada = toggle_music(musica_activada)
                    continue

                # 2) Click en monton
                if rect_monton.collidepoint(mx, my):
                    click_en_mazo(mi_mazo)
                    continue

                # 3) Click en descarte
                if mi_mazo["descarte"] and rect_descarte.collidepoint(mx, my):
                    carta = mi_mazo["descarte"][-1]
                    if intentar_mover_a_fundacion(mi_mazo, carta):
                        mi_mazo["descarte"].pop()
                    else:
                        intentar_mover_descarte_a_pilas(mi_mazo)
                    continue

                # 4) Click en fundaciones
                moved = False
                for k, rect in enumerate(rects_fundacion):
                    if rect.collidepoint(mx, my):
                        mover_desde_fundacion_a_pila(mi_mazo, k)
                        moved = True
                        break
                if moved:
                    continue

                # 5) Selección de bloque en columnas
                bloque, origen = seleccionar_bloque(mi_mazo, mx, my)
                if bloque:
                    bloque_seleccionado = bloque
                    indice_origen      = origen
                    drag_en_progreso   = True
                    posicion_mouse     = (mx, my)

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and drag_en_progreso:
                mx, my = evento.pos

                # Si soltás 1 carta, primero intentá fundación
                if len(bloque_seleccionado) == 1:
                    carta = bloque_seleccionado[0]
                    if intentar_mover_a_fundacion(mi_mazo, carta):
                        mi_mazo["pilas_cuadro"][indice_origen].remove(carta)
                        destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], indice_origen)
                        bloque_seleccionado = []
                        indice_origen       = None
                        drag_en_progreso    = False
                        continue

                # Si no fue a fundación, mové el bloque entre columnas
                bloque_seleccionado, indice_origen = mover_bloque(
                    mi_mazo, bloque_seleccionado, indice_origen, mx, my
                )
                drag_en_progreso = False

            elif evento.type == pygame.MOUSEMOTION and drag_en_progreso:
                posicion_mouse = evento.pos

        # — Renderizado —
        pantalla.fill(VERDE_FONDO)

        # 1) Columnas
        for i, pila in enumerate(mi_mazo["pilas_cuadro"]):
            for j, carta in enumerate(pila):
                x = 50 + i * 120
                y = 200 + j * 25
                img = carta["superficie"] if carta["boca_arriba"] else img_reverso
                pantalla.blit(img, (x, y))

        # 2) Mazo
        if mi_mazo["monton"]:
            pantalla.blit(img_reverso, (50, 30))

        # 3) Descarte
        if mi_mazo["descarte"]:
            pantalla.blit(mi_mazo["descarte"][-1]["superficie"], (140, 30))

        # 4) Fundaciones
        for k in range(4):
            x_f, y_f = rects_fundacion[k].topleft
            if mi_mazo["pilas_cimientos"][k]:
                carta = mi_mazo["pilas_cimientos"][k][-1]
                pantalla.blit(carta["superficie"], (x_f, y_f))
            else:
                pygame.draw.rect(pantalla, BLANCO, (x_f, y_f, 70, 120), 2)

        # 5) Bloque en arrastre
        if drag_en_progreso and bloque_seleccionado:
            mx, my = posicion_mouse
            for idx, carta in enumerate(bloque_seleccionado):
                px = mx - 35
                py = my + idx * 25 - 60
                pantalla.blit(carta["superficie"], (px, py))
                pygame.draw.rect(pantalla, (0, 120, 255), (px, py, 70, 120), 2)

        # 6) Ícono de sonido
        if musica_activada:
            pantalla.blit(icono_on, rect_sonido.topleft)
        else:
            pantalla.blit(icono_off, rect_sonido.topleft)

        pygame.display.update()

