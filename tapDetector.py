import pyaudio
import struct
import math
import os 

class tapDetector():
	"""
		Simplified tap detection based upon stack overflow post
	"""
	def __init__(self):	
		self.FORMAT = pyaudio.paInt16 
		self.short_normalize = (1.0/32768.0)
		self.CHANNELS = 2
		self.RATE = 44100  
		self.INPUT_BLOCK_TIME = 0.05
		self.INPUT_FRAMES_PER_BLOCK = int(self.RATE*self.INPUT_BLOCK_TIME)
		self.pa = pyaudio.PyAudio()	
		self.stream = self.pa.open(format = self.FORMAT, channels = self.CHANNELS, rate = self.RATE, input = True, frames_per_buffer = self.INPUT_FRAMES_PER_BLOCK)
		self.tap_threshold = 0.0015
		self.errorcount = 0

	def get_rms(self, block):
		"""
			Root Mean Square amplitude
		"""
		count = len(block)/2
		format = "%dh"%(count)
		shorts = struct.unpack( format, block )
		# iterate over the block.
		sum_squares = 0.0
		for sample in shorts:
		# sample is a signed short in +/- 32768. 
		# normalize it to 1.0
			n = sample * self.short_normalize
			sum_squares += n*n
			return math.sqrt( sum_squares / count )

	def run(self):
		print 'Running'
		for i in range(250):
			try:
				block = self.stream.read(self.INPUT_FRAMES_PER_BLOCK)
			except IOError, e:
				self.errorcount += 1
				print( "(%d) Error recording: %s"%(self.errorcount,e))
				self.noisycount = 1
			amplitude = self.get_rms(block)
			if amplitude > self.tap_threshold: # if its to loud...
				print amplitude
		print 'Done'

def main():
	td = tapDetector()
	td.run()
main()