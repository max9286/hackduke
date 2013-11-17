
import pygame, os

pygame.mixer.init()

path = "sample_generator/instruments/guitar/"
chords = []
for i in xrange(5):
    sound = pygame.mixer.Sound(os.path.join(path, 'chord%d.wav'%i))
    chords.append(sound)
def play(index):
    chords[index].play()

def stop():
    for chord in chords:
        chord.fadeout(100)
