import pygame
from pygame import mixer

def inicializar_audio(musica_path: str, volumen: float = 0.5) -> None:
    """
    Inicializa el mixer de Pygame, carga la pista de fondo y la reproduce en bucle.

    Param musica_path: ruta al archivo de audio (mp3, wav, etc.).
    Param volumen: nivel de volumen entre 0.0 y 1.0 (por defecto, 0.5).
    Return: None
    """
    mixer.init()
    mixer.music.load(musica_path)
    mixer.music.set_volume(volumen)
    mixer.music.play(-1)

def toggle_music(musica_activa: bool) -> bool:
    """
    Alterna el estado de la música de fondo entre pausa y reproducción.

    Param musica_activa: estado actual de la música (True = sonando).
    Return: nuevo estado de la música después de alternar.
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
