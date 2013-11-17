from midiutil.MidiFile import MIDIFile
from subprocess import call
import os

print "instrument name?"
instrument_name = raw_input()

print "number of chords?"
num_chords = int(raw_input())

print "delay between notes?"
delay = float(raw_input())

# generate midi files for each chord
chords = []
for i in range(0, num_chords):
	chords.append(MIDIFile(1))

track = 0   
time = 0

# Add track name and tempo
for chord in chords:
	chord.addTrackName(track,time,"Sample Track")
	chord.addTempo(track,time,120)


# some default parameters
track = 0
channel = 0
pitch = 60
time = 0
duration = 10
volume = 100

# a list of available notes using the pentatonic scale
# this (almost) guarantees that the notes will sound good
# together
pentatonic_notes = [0,2,5,7,9,12,14,17,19,21,24]

# add the notes needed for each chord
# and then write them to disk
for i, chord in enumerate(chords):
	notes = [pentatonic_notes[i], pentatonic_notes[i+2], pentatonic_notes[i+4]]
	for j, note in enumerate(notes):
		chord.addNote(track,channel,pitch+note,time+(delay*j),duration,volume)
	
	# create the directory if it doesn't exist
	dir_name = "instruments/%s" % instrument_name
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

	# create the file
	f_name = "%s/chord%d.mid" % (dir_name, i)
	f = open(f_name, 'w')
	chord.writeFile(f)
	f.close()

	# use fluidsynth to convert midi to wav
	font_name = "soundfonts/%s.sf2" % instrument_name
	output_name = "%s/chord%d.wav" % (dir_name, i)
	if not os.path.exists(font_name):
		raise Exception("could not find soundfont file for instrument! Looked in " + font_name)
	call(["fluidsynth", "-F", output_name, font_name, f_name])

	# remove the midi file
	os.remove(f_name)

