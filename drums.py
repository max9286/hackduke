
import pygame, os

class Drum:
    snare = 0
    shake = 1
    hi_hat = 2
    cymbal = 3
    bass = 4

pygame.mixer.init()

path = "sample_generator/instruments/drums/"
drums = []
drums.append(pygame.mixer.Sound(os.path.join(path, 'snare.wav')))
drums.append(pygame.mixer.Sound(os.path.join(path, 'shake.wav')))
drums.append(pygame.mixer.Sound(os.path.join(path, 'hi_hat.wav')))
drums.append(pygame.mixer.Sound(os.path.join(path, 'cymbal.wav')))
drums.append(pygame.mixer.Sound(os.path.join(path, 'bass.wav')))

def play(drum):
    	drums[drum].play()
	pygame.time.wait(10)
	drums[drum].play()
def stop():
    for drum in drums:
        drum.fadeout(100)
