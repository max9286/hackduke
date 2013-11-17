from midiutil.MidiFile import MIDIFile

# Create the MIDIFile Object with 1 track
chord1 = MIDIFile(1)
chord2 = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.

track = 0   
time = 0

# Add track name and tempo.
chord1.addTrackName(track,time,"Sample Track")
chord1.addTempo(track,time,120)

# Add a note. addNote expects the following information:
track = 0
channel = 0
pitch = 60
time = 0
duration = 10
volume = 100

# Now add the note.
chord1.addNote(track,channel,pitch+2,time,duration,volume)
chord1.addNote(track,channel,pitch+7,time,duration,volume)
chord1.addNote(track,channel,pitch+12,time,duration,volume)

chord2.addNote(track,channel,pitch,time,duration,volume)
chord2.addNote(track,channel,pitch+5,time,duration,volume)
chord2.addNote(track,channel,pitch+9,time,duration,volume)

# And write it to disk.
file1 = open("instruments/accordian/chord1.mid", 'wb')
file2 = open("instruments/accordian/chord2.mid", 'wb')
chord1.writeFile(file1)
file1.close()
chord2.writeFile(file2)
file2.close()