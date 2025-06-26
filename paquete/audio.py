import pygame
from pygame import mixer

def inicializar_audio(musica_path: str, volumen: float = 0.5) -> None:
    """
    Inicializa el mixer, carga la pista de fondo y la reproduce en bucle.
    """
    mixer.init()
    mixer.music.load(musica_path)
    mixer.music.set_volume(volumen)
    mixer.music.play(-1)

def toggle_music(musica_activa: bool) -> bool:
    """
    Alterna el estado de la música (on/off).
    Recibe el estado actual y devuelve el nuevo.
    """
    nueva = not musica_activa
    if nueva:
        if mixer.music.get_busy():
            mixer.music.unpause()
        else:
            mixer.music.play(-1)
    else:
        mixer.music.pause()
    return nueva
