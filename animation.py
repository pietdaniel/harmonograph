import pygame
from pygame.locals import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

white = (255,255,255)
black = (0,0,0)

class animation():
	def __init__(self,onTickFunc):
		self.onTickFunc = onTickFunc
		self.width=1920
		self.height=1080
		self.scr = pygame.display.set_mode((self.width,self.height))
		self.screen=self.scr.copy()
		self.loop=0
		self.counter=0
		self.scaling=400

	def start(self):
		while not self.loop:
			self.scr.fill(black)
			if (self.screen):
				self.screen.set_alpha(50)
				self.scr.blit(self.screen,(0,0))	
			self.draw()

			self.counter+=1
			pygame.display.flip()
			self.screen=self.scr.copy()
			pygame.time.wait(2)
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
		for ctr in self.drange(0.0,0.25,0.0005):
			timeAtFrame = self.counter/4.0 + ctr
			(x1,y1) = self.getScreenPos(self.onTickFunc(timeAtFrame))
			(x,y) = (int(x1),int(y1))
			pygame.draw.circle(self.scr,white,(x,y),1,1)

	def getScreenPos(self,pos):
		(x,y) = pos
		xVal = x*self.scaling+self.width/2
		yVal = y*self.scaling+self.height/2
		return (xVal,yVal)


