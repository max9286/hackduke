#Import the library

from midiutil.MidiFile import MIDIFile
import pygame
# import midi
# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.

track = 0   
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

# Add a note. addNote expects the following information:
track = 0
channel = 0
pitch = 60
time = 0
duration = 50
volume = 100

# Now add the note.
MyMIDI.addNote(track,channel,pitch,time,duration,volume)
MyMIDI.addNote(track,channel,pitch+10,time+.1,duration,volume)
MyMIDI.addNote(track,channel,pitch+20,time+.2,duration,volume)
MyMIDI.addNote(track,channel,pitch+30,time,duration,volume)
MyMIDI.addNote(track,channel,pitch+40,time+.1,duration,volume)
MyMIDI.addNote(track,channel,pitch+50,time+.2,duration,volume)

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()


# midi.read_midifile("output.mid")

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

def stop_music(): # stop currently playing music, else do nothing
    
    
music_file = "output.mid"

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0

pygame.mixer.music.set_volume(1)
try:
    # use the midi file you just saved
    play_music(music_file)
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit