import math
import wave
import sys
import operator
import functools
import struct
from itertools import *

# Returns an infinite generator that samples the wave at the specified bitrate
def sine_wave(freq=500.0, bitrate=44100, amplitude=1.0):
	return(float(amplitude)*math.sin(2.0*math.pi*float(freq)*(float(i)/float(bitrate))) for i in count(0))

# Returns the product of every element in a tuple
def mult(tup):
	return functools.reduce(operator.mul, tup)

# Computes the modulated signal by multiplying each sample in the input generators
def modulate_samples(channels, n_samples=None):
	return islice(zip(*(map(mult, zip(*channel)) for channel in channels)), n_samples)

#def compute_samples(channels, n_samples=None):
	#return islice(zip(*(map(sum, zip(*channel)) for channel in channels)), n_samples)

# Writes computed samples to a .wav file in an uncompressed format
def write_wavefile(filename, samples, n_frames=None, n_channels=2, sampwidth=2, bitrate=44100):
	if n_frames is None:
		n_frames = -1

	w = wave.open(filename, 'w')
	w.setparams((n_channels, sampwidth, bitrate, n_frames, 'NONE', 'not compressed'))

	max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
	
	for sample in samples:
		for channel in sample:			
			w.writeframesraw(struct.pack('h', int(max_amplitude * channel)))
	w.close

	return filename

if __name__ == "__main__":
	carrier_freq = float(input("Please enter the Carrier Frequency: "))
	mod_freq = float(input("Please enter the Modulating Frequency: "))
	length = float(input("Please enter the desired length in seconds: "))
	n_channels = 2
	bitrate = 44100 #frames per second
	n_frames = int(bitrate * length)
	print(n_frames)
	filename = str(int(carrier_freq)) + "Hz_mod" + str(int(mod_freq)) + "Hz_" + str(int(length * 1000)) + "ms.wav"

	carrier_wave = sine_wave(carrier_freq, bitrate)
	mod_wave = sine_wave(mod_freq, bitrate)
	right_channel = sine_wave(carrier_freq, bitrate, 0.0)
	channels = ((carrier_wave, mod_wave), (right_channel,))
	samples = modulate_samples(channels, n_frames)
	write_wavefile(filename, samples, n_frames)