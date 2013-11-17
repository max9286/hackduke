from midiutil.MidiFile import MIDIFile
from subprocess import call
import os

print "instrument name?"
instrument_name = raw_input()

print "starting pitch?"
start_pitch = int(raw_input())

print "number of notes?"
num_notes = int(raw_input())



# generate midi files for each note
notes = []
for i in range(0, num_notes):
	notes.append(MIDIFile(1))

track = 0   
time = 0

# Add track name and tempo
for note in notes:
	note.addTrackName(track,time,"Sample Track")
	note.addTempo(track,time,120)


# some default parameters
track = 0
channel = 0
pitch = start_pitch
time = 0
duration = 10
volume = 100

# a list of available notes using the pentatonic scale
# this (almost) guarantees that the notes will sound good
# together
pentatonic_notes = [0,2,5,7,9,12,14,17,19,21,24,26,29,31,33,36]

# add the notes needed for each note
# and then write them to disk
for i, note in enumerate(notes):
	penta_pitch = pentatonic_notes[i]
	note.addNote(track,channel,pitch+penta_pitch,time,duration,volume)
	
	# create the directory if it doesn't exist
	dir_name = "instruments/%s" % instrument_name
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

	# create the file
	f_name = "%s/note%d.mid" % (dir_name, i)
	f = open(f_name, 'w')
	note.writeFile(f)
	f.close()

	# use fluidsynth to convert midi to wav
	font_name = "soundfonts/%s.sf2" % instrument_name
	output_name = "%s/note%d.wav" % (dir_name, i)
	if not os.path.exists(font_name):
		raise Exception("could not find soundfont file for instrument! Looked in " + font_name)
	call(["fluidsynth", "-F", output_name, font_name, f_name])

	# remove the midi file
	os.remove(f_name)

