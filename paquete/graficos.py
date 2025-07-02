import pygame, os
from paquete.audio import toggle_music

# Colores y tamaño de pantalla
NEGRO       = (  0,   0,   0)
BLANCO      = (255, 255, 255)
VERDE_FONDO = (  0, 100,   0)
AZUL        = (  0,   0, 255)

ANCHO, ALTO = 1000, 700

# Rutas de íconos
RUTA_ON     = "recursos/sonido_on.jpg"
RUTA_OFF    = "recursos/sonido_off.jpg"
ruta_reverso = "recursos/img/reverso_carta.png"

def mostrar_menu(pantalla: pygame.Surface,
                musica_activada: bool) -> bool:
    """
    Dibuja el menú principal y gestiona interacciones.

    Presenta botones para:
    - Iniciar juego
    - Ver ranking
    - Activar/desactivar música

    Param pantalla: superficie de Pygame donde dibujar el menú.
    Param musica_activada: estado inicial de la música (True = encendida).
    Return: nuevo estado de musica_activada tras la interacción.
    """
    fuente_titulo = pygame.font.SysFont("arial", 64)
    fuente_boton  = pygame.font.SysFont("arial", 36)

    rect_jugar   = pygame.Rect(ANCHO//2 - 120, 260, 240, 60)
    rect_sonido  = pygame.Rect(ANCHO - 60, 20, 40, 40)

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
        txt_jugar = fuente_boton.render("Iniciar juego", True, NEGRO)
        pantalla.blit(txt_jugar, (rect_jugar.x + 30, rect_jugar.y + 15))

        # Botón "Ver ranking"
        rect_ranking = pygame.Rect(400, 420, 200, 50)
        pygame.draw.rect(pantalla, AZUL, rect_ranking)
        txt_rank = fuente_boton.render("Ver ranking", True, BLANCO)
        pantalla.blit(txt_rank, rect_ranking.move(20, 10).topleft)

        # Icono de sonido según estado
        ruta_icono = RUTA_ON if musica_activada else RUTA_OFF
        icono = pygame.image.load(ruta_icono)
        icono = pygame.transform.scale(icono, (40, 40))
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
                elif rect_ranking.collidepoint(mx, my):
                    mostrar_ranking(pantalla)
                elif rect_sonido.collidepoint(mx, my):
                    musica_activada = toggle_music(musica_activada)

    return musica_activada

def obtener_puntaje(par: tuple) -> int:
    """
    Extrae el segundo elemento de una tupla (nombre, puntaje).

    Param par: tupla con (str, int)
    Return: el puntaje (int)
    """
    return par[1]

def mostrar_ranking(pantalla: pygame.Surface) -> None:
    """
    Muestra los 10 mejores puntajes leyendo 'ranking.txt'.

    El archivo debe contener líneas en formato "nombre, puntaje".
    Si no existe, muestra una lista vacía.

    Param pantalla: superficie de Pygame donde dibujar el ranking.
    Return: None. Vuelve tras presionar ESC o hacer clic.
    """
    fuente_titulo = pygame.font.SysFont(None, 64)
    fuente_lista  = pygame.font.SysFont(None, 36)

    # Leer y parsear ranking
    ranking = []
    if os.path.exists("ranking.txt"):
        with open("ranking.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    nombre = partes[0].strip()
                    try:
                        puntaje = int(partes[1].strip())
                        ranking.append((nombre, puntaje))
                    except ValueError:
                        pass

    # Ordenar descendentemente por puntaje
    ranking.sort(key=obtener_puntaje, reverse=True)

    # Tomar top 10
    top = ranking[:10]

    esperando = True
    while esperando:
        pantalla.fill((25, 25, 60))

        titulo = fuente_titulo.render("Ranking", True, (255, 255, 255))
        pantalla.blit(titulo, (400, 80))

        # Dibujar lista
        for i, (nombre, puntaje) in enumerate(top):
            linea = f"{i+1}. {nombre} — {puntaje} pts"
            txt = fuente_lista.render(linea, True, (200, 255, 200))
            pantalla.blit(txt, (300, 180 + i * 40))

        instruccion = fuente_lista.render(
            "Presioná ESC o clic para volver", True, (180, 180, 180)
        )
        pantalla.blit(instruccion, (280, 600))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

def ingresar_nombre(pantalla: pygame.Surface) -> str:
    """
    Solicita al jugador que ingrese su nombre y presione ENTER.

    El nombre máximo permitido es de 12 caracteres.
    Param pantalla: superficie de Pygame donde dibujar la entrada.
    Return: cadena con el nombre ingresado.
    """
    fuente = pygame.font.SysFont(None, 48)
    nombre = ""
    esperando = True

    while esperando:
        pantalla.fill((20, 20, 20))
        prompt = fuente.render(
            "Ingresá tu nombre y presioná ENTER:", True, (255, 255, 255)
        )
        pantalla.blit(prompt, (220, 200))

        texto_nombre = fuente.render(nombre, True, (0, 255, 0))
        pantalla.blit(texto_nombre, (300, 300))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre:
                    return nombre
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 12:
                    nombre += evento.unicode