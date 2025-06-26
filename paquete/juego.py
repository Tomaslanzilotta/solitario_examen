import pygame
from paquete.funciones import repartir_juego
from paquete.logica import *
from paquete.graficos import ruta_reverso, VERDE_FONDO, BLANCO

def iniciar_juego(pantalla: pygame.Surface) -> None:
    mi_mazo = repartir_juego()

    # Rectángulos interactivos
    rect_monton   = pygame.Rect(50,  30, 70, 120)
    rect_descarte = pygame.Rect(140, 30, 70, 120)

    bloque_seleccionado = []
    indice_origen       = None
    drag_en_progreso    = False
    posicion_mouse      = (0, 0)

    # Precarga la imagen del reverso
    img_reverso = pygame.image.load(ruta_reverso)
    img_reverso = pygame.transform.scale(img_reverso, (70, 120))

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                break

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mx, my = evento.pos

                # 1) Clic en el montón
                if rect_monton.collidepoint(mx, my):
                    click_en_mazo(mi_mazo)

                # 2) Clic en el descarte
                elif mi_mazo["descarte"] and rect_descarte.collidepoint(mx, my):
                    intentar_mover_descarte_a_pilas(mi_mazo)

                # 3) Seleccionar bloque de la mesa
                else:
                    bloque, origen = seleccionar_bloque(mi_mazo, mx, my)
                    if bloque:
                        bloque_seleccionado = bloque
                        indice_origen      = origen
                        drag_en_progreso   = True
                        posicion_mouse     = (mx, my)

            elif (evento.type == pygame.MOUSEBUTTONUP and
                evento.button == 1 and
                drag_en_progreso):
                mx, my = evento.pos
                bloque_seleccionado, indice_origen = mover_bloque(
                    mi_mazo,
                    bloque_seleccionado,
                    indice_origen,
                    mx, my
                )
                drag_en_progreso = False

            elif evento.type == pygame.MOUSEMOTION and drag_en_progreso:
                posicion_mouse = evento.pos

        # ——— DIBUJADO ———
        pantalla.fill(VERDE_FONDO)

        # Tablero (pilas del cuadro)
        for i, pila in enumerate(mi_mazo["pilas_cuadro"]):
            for j, carta in enumerate(pila):
                x = 50 + i * 120
                y = 200 + j * 25
                if carta["boca_arriba"]:
                    pantalla.blit(carta["superficie"], (x, y))
                else:
                    pantalla.blit(img_reverso, (x, y))

        # Mazo
        if mi_mazo["monton"]:
            pantalla.blit(img_reverso, (50, 30))

        # Descarte
        if mi_mazo["descarte"]:
            ultima = mi_mazo["descarte"][-1]
            pantalla.blit(ultima["superficie"], (140, 30))

        # Fundaciones
        for k in range(4):
            x_f, y_f = 400 + k * 90, 30
            if mi_mazo["pilas_cimientos"][k]:
                top = mi_mazo["pilas_cimientos"][k][-1]
                pantalla.blit(top["superficie"], (x_f, y_f))
            else:
                pygame.draw.rect(pantalla, BLANCO, (x_f, y_f, 70, 120), 2)

        # Bloque arrastrado
        if drag_en_progreso and bloque_seleccionado:
            mx, my = posicion_mouse
            for idx, carta in enumerate(bloque_seleccionado):
                px = mx - 35
                py = my + idx * 25 - 60
                pantalla.blit(carta["superficie"], (px, py))
                pygame.draw.rect(
                    pantalla,
                    (0, 120, 255),
                    (px, py, 70, 120),
                    2
                )

        pygame.display.update()

    # Al cerrar la ventana, el control vuelve al menú
    return
