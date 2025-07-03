import pygame, random, time, sys
from paquete.funciones import repartir_juego
from paquete.graficos import*
from paquete.audio import *
from paquete.logica import *

# ——— Inicialización ———
pygame.init()
pantalla = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Solitario de Tomas")
inicializar_audio("recursos/Balatro Main Theme.mp3", 0.5)
random.seed(time.time())

while True:
    musica_activada = mostrar_menu(pantalla, True)
    nombre_jugador  = ingresar_nombre(pantalla)

    mi_mazo = repartir_juego()
    puntaje  = 0

    img_reverso = pygame.image.load(ruta_reverso)
    img_reverso = pygame.transform.scale(img_reverso, (70, 120))

    icono_on  = pygame.image.load(RUTA_ON)
    icono_off = pygame.image.load(RUTA_OFF)
    icono_on  = pygame.transform.scale(icono_on,  (40, 40))
    icono_off = pygame.transform.scale(icono_off, (40, 40))

    rect_sonido    = pygame.Rect(20, 640, 40, 40)
    rect_reiniciar = pygame.Rect(140, 640, 100, 40)

    rect_monton   = pygame.Rect(50, 30, 70, 120)
    rect_descarte = pygame.Rect(140, 30, 70, 120)

    # Sin list-comprehension
    rects_fundacion = []
    for k in range(4):
        x = 400 + k * 90
        rects_fundacion.append(pygame.Rect(x, 30, 70, 120))

    bloque_seleccionado = []
    indice_origen       = None
    drag_en_progreso    = False
    posicion_mouse      = (0, 0)

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mx, my = evento.pos

                if rect_sonido.collidepoint(mx, my):
                    musica_activada = toggle_music(musica_activada)
                    continue

                if rect_reiniciar.collidepoint(mx, my):
                    ejecutando = False
                    continue

                if rect_monton.collidepoint(mx, my):
                    click_en_mazo(mi_mazo)
                    puntaje -= 1
                    continue

                if mi_mazo["descarte"] and rect_descarte.collidepoint(mx, my):
                    carta = mi_mazo["descarte"][-1]
                    if intentar_mover_a_fundacion(mi_mazo, carta):
                        mi_mazo["descarte"].pop()
                        puntaje += 10
                    else:
                        intentar_mover_descarte_a_pilas(mi_mazo)
                        puntaje += 5
                    continue

                for idx, rect in enumerate(rects_fundacion):
                    if rect.collidepoint(mx, my):
                        mover_desde_fundacion_a_pila(mi_mazo, idx)
                        break

                bloque, origen = seleccionar_bloque(mi_mazo, mx, my)
                if bloque:
                    bloque_seleccionado = bloque
                    indice_origen       = origen
                    drag_en_progreso    = True
                    posicion_mouse      = (mx, my)

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 \
                and drag_en_progreso:
                mx, my = evento.pos

                if len(bloque_seleccionado) == 1:
                    carta = bloque_seleccionado[0]
                    if intentar_mover_a_fundacion(mi_mazo, carta):
                        mi_mazo["pilas_cuadro"][indice_origen].remove(carta)
                        destapar_tope_si_corresponde(mi_mazo["pilas_cuadro"], indice_origen)
                        puntaje += 10
                        bloque_seleccionado = []
                        indice_origen       = None
                        drag_en_progreso    = False
                        continue

                bloque_seleccionado, indice_origen = mover_bloque(mi_mazo, bloque_seleccionado, 
                                                    indice_origen, mx, my)
                drag_en_progreso = False

            elif evento.type == pygame.MOUSEMOTION and drag_en_progreso:
                posicion_mouse = evento.pos

        pantalla.fill(VERDE_FONDO)

        for i_pila, pila in enumerate(mi_mazo["pilas_cuadro"]):
            for j_carta, carta in enumerate(pila):
                x = 50 + i_pila * 120
                y = 200 + j_carta * 25
                img = carta["superficie"] if carta["boca_arriba"] else img_reverso
                pantalla.blit(img, (x, y))

        if mi_mazo["monton"]:
            pantalla.blit(img_reverso, (50, 30))
        if mi_mazo["descarte"]:
            pantalla.blit(mi_mazo["descarte"][-1]["superficie"], (140, 30))

        for k in range(4):
            x_f, y_f = rects_fundacion[k].topleft
            if mi_mazo["pilas_cimientos"][k]:
                carta = mi_mazo["pilas_cimientos"][k][-1]
                pantalla.blit(carta["superficie"], (x_f, y_f))
            else:
                pygame.draw.rect(pantalla, BLANCO, (x_f, y_f, 70, 120), 2)

        if drag_en_progreso and bloque_seleccionado:
            mx, my = posicion_mouse
            offset = 0
            for carta in bloque_seleccionado:
                px = mx - 35
                py = my + offset * 25 - 60
                pantalla.blit(carta["superficie"], (px, py))
                pygame.draw.rect(pantalla, (0, 120, 255), (px, py, 70, 120), 2)
                offset += 1

        pantalla.blit(icono_on if musica_activada else icono_off,
                    rect_sonido.topleft)

        pygame.draw.rect(pantalla, (0, 120, 200), rect_reiniciar,
                    border_radius=5)
        fuente_btn = pygame.font.SysFont(None, 28)
        pantalla.blit(
            fuente_btn.render("Reiniciar", True, (255, 255, 255)),
            rect_reiniciar.move(12, 8).topleft
        )

        fuente_puntaje = pygame.font.SysFont(None, 28)
        txt_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}",
                                            True, (255, 255, 255))
        pantalla.blit(txt_puntaje, (800, 650))

        pygame.display.update()

        if jugador_gano(mi_mazo):
            finalizar_partida(pantalla, nombre_jugador, puntaje)
            ejecutando = False