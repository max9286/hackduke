import math
import numpy
import pyaudio
import time
import threading

class Tone:

	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
		self.freq = 550
		self.volume = 0
		self.thread = None
		self.event = None

	def start(self):
		self.event = threading.Event()
		self.thread = threading.Thread(name="play_tone", target=play_tone, args=(self.stream,self.event,))
		self.thread.start()
		self.event.wait()

	def stop(self):
		self.event.set()

	def close(self):
		self.stream.close()
		self.p.terminate()


def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, end, frequency=440, length=1, rate=44100):
	print "playing tone"
	chunks = []
	chunks.append(sine(frequency, length, rate))

	chunk = numpy.concatenate(chunks) * 0.25

	stream.write(chunk.astype(numpy.float32).tostring())


if __name__ == '__main__':
	t = Tone()
	t.start()
	time.sleep(1)
	t.stop()
	t.close()
