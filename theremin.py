import math
import numpy
import pyaudio
import time
import threading

class Theremin:

	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
		self.freq = 550
		self.volume = 0
		self.thread = None
		self.is_playing = False
		self.event = None

	# start playing a tone
	def start(self):
		if not self.is_playing:
			self.is_playing = True
			self.event = threading.Event()
			self.thread = threading.Thread(name="play_tone", target=play_tone, args=(self.stream,self.event,self))
			self.thread.start()
		
	# stop playing the tone
	def stop(self):
		self.event.set()
		self.is_playing = False

	# set the frequency of the tone
	# works whether the tone is currently playing or not
	def set_freq(self,freq):
		self.freq = freq

	# must call this before your application exits
	def close(self):
		self.stream.close()
		self.p.terminate()


def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, end, ther, length=0.5, rate=44100):
	while not end.is_set():
		chunks = []
		chunks.append(sine(ther.freq, length, rate))
		chunk = numpy.concatenate(chunks) * 0.25
		stream.write(chunk.astype(numpy.float32).tostring())

if __name__ == '__main__':
	t = Theremin()
	t.start()
	time.sleep(0.5)
	t.set_freq(440)
	time.sleep(1)
	t.set_freq(470)
	time.sleep(0.3)
	t.set_freq(440)
	time.sleep(1)
	t.stop()
	time.sleep(1)
	t.start()
	t.start()
	time.sleep(1)
	t.stop()
	t.close()
