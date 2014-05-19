import pygame
from pygame.locals import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
from time import time


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
		self.counter=1
		self.scaling=.4
		self.mouse_visibility = 1

		self.fps = 30.0
		self.dot_resolution = 800.0
		self.ms_per_frame = 1000.0/self.fps

		self.timeIncrement = self.ms_per_frame / self.dot_resolution
		self.start_time_ms = 0.0
		self.ms_drawn_counter = 0.0
		
		self.mark_time = 0.0
		self.delta_time = 0.0


	def start(self):
		pygame.mouse.set_visible(self.mouse_visibility)
		self.mark_time = time()
		self.start_time_ms = time() * 1000.0
		while not self.loop:
			self.draw()
			self.regulate_time()	
			self.loop = self.keyQuit()
			self.counter+=1

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

	def regulate_time(self):
		self.delta_time = self.ms_per_frame - (1000*(time() - self.mark_time))
		pygame.time.delay(int(self.delta_time))
		self.mark_time = time()

	def draw(self):
		self.scr.fill(black)
		if (self.screen):
			self.screen.set_alpha(50)
			self.scr.blit(self.screen,(0,0))	
		self.plotGraph()
		pygame.display.flip()
		self.screen=self.scr.copy()


	def plotGraph(self):
		for timeInc in self.drange(0.0, self.ms_per_frame, self.timeIncrement):
			timeAtFrame = self.ms_drawn_counter + timeInc
			(x1,y1) = self.getScreenPos(self.onTickFunc(timeAtFrame/1000.0))
			(x,y) = (int(x1),int(y1))
			pygame.draw.circle(self.scr,white,(x,y),1,1)
		self.ms_drawn_counter = ((time() * 1000.0) - self.start_time_ms)

	def getScreenPos(self,pos):
		(x,y) = pos
		xVal = x*self.scaling+self.width/2
		yVal = y*self.scaling+self.height/2
		return (xVal,yVal)