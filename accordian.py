
import pygame

pygame.mixer.init()
in_chord = pygame.mixer.Sound("accordian/chord0.wav")
out_chord = pygame.mixer.Sound("accordian/chord1.wav")

def play(chord):
    if chord == "in":
        in_chord.play()
    elif chord == "out":
        out_chord.play()

    #while pygame.mixer.get_busy():
    #    pygame.time.wait(20)


def stop():
    in_chord.fadeout(100)
    out_chord.fadeout(100)
