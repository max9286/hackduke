
import pygame, os

pygame.mixer.init()

path = "sample_generator/instruments/violin/"
notes = []
for i in xrange(5):
    sound = pygame.mixer.Sound(os.path.join(path, 'note%d.wav'%i))
    notes.append(sound)
def play(index):
    notes[index].play()

def stop():
    for note in notes:
        note.fadeout(500)
