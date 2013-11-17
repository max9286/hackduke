
import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound('sample_generator/instruments/dj/scratch.wav')

def play():
    sound.play()

def stop():
    sound.stop()
