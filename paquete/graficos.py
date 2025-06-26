import pygame
from paquete.audio import toggle_music  # <-- quitamos is_music_on

# Colores y tamaño
NEGRO       = (  0,   0,   0)
BLANCO      = (255, 255, 255)
VERDE_FONDO = (  0, 100,   0)
ANCHO, ALTO = 1000, 700

# Rutas de íconos
RUTA_ON  = "recursos/sonido_on.jpg"
RUTA_OFF = "recursos/sonido_off.jpg"

ruta_reverso  = "recursos/img/reverso_carta.png"


def mostrar_menu(pantalla: pygame.Surface,
                musica_activada: bool) -> bool:
    """
    Dibuja el menú hasta que clickees 'Iniciar juego' o cierres la ventana.
    Recibe y devuelve el estado de musica_activada.
    """
    fuente_titulo = pygame.font.SysFont("arial", 64)
    fuente_boton  = pygame.font.SysFont("arial", 36)

    rect_jugar  = pygame.Rect(ANCHO//2 - 120, 260, 240, 60)
    rect_sonido = pygame.Rect(ANCHO - 60, 20, 40, 40)

    titulo_surf = fuente_titulo.render("Solitario Klondike", True, BLANCO)
    en_menu = True

    while en_menu:
        pantalla.fill(VERDE_FONDO)
        pantalla.blit(
            titulo_surf,
            (ANCHO//2 - titulo_surf.get_width()//2, 100)
        )

        # Botón "Iniciar juego"
        pygame.draw.rect(pantalla, BLANCO, rect_jugar, border_radius=10)
        txt = fuente_boton.render("Iniciar juego", True, NEGRO)
        pantalla.blit(txt, (rect_jugar.x+30, rect_jugar.y+15))

        # Icono sonido (según la variable que recibimos)
        ruta = RUTA_ON if musica_activada else RUTA_OFF
        icono = pygame.image.load(ruta)
        icono = pygame.transform.scale(icono, (40,40))
        pantalla.blit(icono, rect_sonido.topleft)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos

                if rect_jugar.collidepoint(mx, my):
                    en_menu = False

                elif rect_sonido.collidepoint(mx, my):
                    # toggle_music devuelve el nuevo estado
                    musica_activada = toggle_music(musica_activada)

    return musica_activada

