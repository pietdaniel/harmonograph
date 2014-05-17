import pygame
from pygame.locals import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

white = (255,255,255)
black = (0,0,0)

class animation():
	"""
		onTickFunc takes time and returns
		a screen position.
	"""
	def __init__(self,onTickFunc):
		self.onTickFunc = onTickFunc
		self.width=1920
		self.height=1080
		self.scr = pygame.display.set_mode((self.width,self.height))
		self.screen=self.scr.copy()
		self.loop=0
		self.counter=0
		self.scaling=.4
		self.fps = 60.0
		self.sample_rate = .5 #44100.0
		self.mouse_visibility = 1
		self.ms_per_frame = 1000.0/self.fps
		self.ms_per_sample = 1000.0/self.sample_rate
		self.ms_per_sample_frame = self.ms_per_sample * self.ms_per_frame
		self.dot_resolution = 500.0

	def start(self):
		pygame.mouse.set_visible(self.mouse_visibility)
		while not self.loop:
			self.scr.fill(black)
			if (self.screen):
				self.screen.set_alpha(50)
				self.scr.blit(self.screen,(0,0))	
			self.draw()

			self.counter+=1
			pygame.display.flip()
			self.screen=self.scr.copy()
			pygame.time.wait(int(self.ms_per_frame))
			self.loop = self.keyQuit()

	def stop(self):
		self.loop=1

	def keyQuit(self):
		for e in pygame.event.get():
			if e.type == KEYDOWN and e.key == K_w:
				x=1/0
			if e.type == KEYDOWN and e.key == K_q:
				return 1

	def drange(self,start, stop, step):
		r = start
		while r < stop:
			yield r
			r += step

	def draw(self):
		timeOffset = self.counter * self.ms_per_sample_frame
		timeIncrement = self.ms_per_sample_frame / self.dot_resolution
		for timeInc in self.drange(0.0, self.ms_per_sample_frame, timeIncrement):
			timesAtFrame = timeOffset + timeInc
			(x1,y1) = self.getScreenPos(self.onTickFunc(timesAtFrame))
			(x,y) = (int(x1),int(y1))
			pygame.draw.circle(self.scr,white,(x,y),1,1)

	def getScreenPos(self,pos):
		(x,y) = pos
		xVal = x*self.scaling+self.width/2
		yVal = y*self.scaling+self.height/2
		return (xVal,yVal)


