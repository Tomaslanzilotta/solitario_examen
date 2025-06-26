import pygame, random, time
from paquete.audio    import inicializar_audio
from paquete.graficos import mostrar_menu
from paquete.juego    import iniciar_juego

pygame.init()
pantalla = pygame.display.set_mode((1000,700))
pygame.display.set_caption("Solitario Klondike")

# Audio 
inicializar_audio("recursos/Balatro Main Theme.mp3", 0.5)
musica_activada = True

random.seed(time.time())

# Flujo: menú → juego → menú...
while True:
    musica_activada = mostrar_menu(pantalla, musica_activada)
    iniciar_juego(pantalla)
