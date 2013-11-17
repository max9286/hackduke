from midiutil.MidiFile import MIDIFile
from subprocess import call
import os

print "instrument name?"
instrument_name = raw_input()

num_notes = 128

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
pitch = 0
time = 0
duration = 4
volume = 100

# add a single note for the midi file for each note
for i, note in enumerate(notes):
	note.addNote(track,channel,pitch+i,time,duration,volume)
	
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

