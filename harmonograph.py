import pygame, math, types
import pygame.midi # dep?
from pygame.locals import *
from random import randint,choice,randrange
from math import pi, sin, asin, tan, cos
import os
from pprint import pprint
import midi
import numpy as np

width=1920
height=1080
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
scr = pygame.display.set_mode((width,height))
white = (255,255,255)
black = (0,0,0)


def keyQuit(loop):
	for e in pygame.event.get():
		if e.type == KEYDOWN and e.key == K_q:
			x=1/0 # lol
	return loop

def makeXYofT(func1,func2):
	def xYofT(t):
		return func1(t) + func2(t)
	return xYofT

def hEquation(amplitude, frequency, phase, damping):
	def hFunc(time):
		val = amplitude*math.sin(2*math.pi*time*frequency + float(phase))*math.pow(math.e,(-1*damping*time))
		return val
	return hFunc

def makeXYatT(func1,func2):
	def XYatT(t):
		return (func1(t),func2(t))
	return XYatT

def harmonicXYatT():
	freqX = 261.63
	freqY = 392.44
	ratio1 = 0.0
	ratio2 = 0.0
	freqS1 = ratio1 * freqX
	freqS2 = ratio2 * freqY
	ampS1 = .5
	ampS2 = .5
	ampX = .5
	ampY = .5
	baseFuncS1 = hEquation(ampS1,freqS1, 0,.1)
	baseFuncX = hEquation(ampS2,freqX, 0,.1)
	baseFuncS2 = hEquation(ampX,freqS1, 0,.1)
	baseFuncY = hEquation(ampY,freqY, 0,.1)
	xOft=makeXYofT(baseFuncS1,baseFuncX)
	yOft=makeXYofT(baseFuncS2,baseFuncY)
	return makeXYatT(xOft,yOft)

def genericXYatT():
	baseFunc = hEquation(100.0,100,0,.1)
	baseFunc2 = hEquation(100.0,150,0,.1)
	baseFunc3 = hEquation(100.0,20,0,.1)
	xOft=makeXYofT(baseFunc,baseFunc2)
	yOft=makeXYofT(baseFunc,baseFunc3)
	return makeXYatT(xOft,yOft)

def getScreenPos(pos):
	(x,y) = pos
	w2 = width/2
	h2 = height/2
	scaling=400
	return (x*scaling+w2,y*scaling+h2)

def mirrorX(pos):
	(x,y) = pos
	w2 = width/2
	h2 = height/2
	return ((w2-x)+w2,y)

def mirrorY(pos):
	(x,y) = pos
	w2 = width/2
	h2 = height/2
	return (x,(h2-y)+h2)

def invert(pos):
	(x,y) = pos
	w2 = width/2
	h2 = height/2
	return ((w2-x)+w2,(h2-y)+h2)

def makeA():
	frequency = 436.05
	duration_in_samples = 40000
	sample_rate = 44100
	sarray = np.array([10000*math.sin(2.0 * math.pi * frequency * t / sample_rate) for t in xrange(0, duration_in_samples)])
	# print sarray
	return np.int16(sarray)


def harmonograph():
	hFunc = harmonicXYatT()
	print pygame.sndarray.get_arraytype()
	print pygame.version.ver
	pygame.mixer.pre_init(22050, -16, 1, 4096)
	pygame.mixer.init()
	print makeA()
	s = pygame.sndarray.make_sound(makeA())
	sound = pygame.mixer.Sound(s)
	pygame.mixer.Sound.play(sound)

	
	loop=0

	# pygame.display.flip()
	hTime = 0
	dotResolution =  1/ 10000.0
	dotsPerFrame = 2500

	def draw(i):
		maxZ = 2500
		for z in range(0,maxZ):
			q =  (i/4.0) + (z / 10000.0)
			(x1,y1) = getScreenPos(hFunc(q))
			(x,y) = (int(x1),int(y1))
			print (q,x1,y1,x,y)
			pygame.draw.circle(scr,(255,255,255),(x,y),1,1)
	def draw2(i):
		maxZ = 500
		for z in range(0,maxZ):
			q =  (i/4.0) + (z / 2000.0)
			(x1,y1) = getScreenPos(hFunc(q))
			(x,y) = (int(x1),int(y1))
			# print (i,x1,y1,x,y)
			pygame.draw.circle(scr,(255,255,255),(x,y),1,1)

	i=0
	screen=scr.copy()
	while not loop:
		scr.fill((0,0,0))
		if (screen):
			screen.set_alpha(50)
			scr.blit(screen,(0,0))	
		draw2(i)
		
		i+=1
		pygame.display.flip()
		screen=scr.copy()
		pygame.time.wait(2)
		loop = keyQuit(loop)

	





def main():
	#used in all
	# pygame.mouse.set_visible(0)

	harmonograph()

	
	
main()
