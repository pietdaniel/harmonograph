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
			loop=1
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

def hEquation2(amplitude, frequency, phase, damping, sample_rate):
	def hFunc(time):
		val = amplitude*math.sin(2*math.pi*frequency*time/sample_rate + float(phase))*math.pow(math.e,(-1*damping*time/sample_rate))
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

def harmonicXatT(sample_rate):
	freqX = 261.63
	ratio1 = 0.0
	freqS1 = ratio1 * freqX
	ampS1 = 10000
	ampS2 = 10000
	ampX = 10000
	damping = .9
	phase = 0 
	baseFuncS1 = hEquation2(ampS1,freqS1, phase,damping,sample_rate)
	baseFuncX = hEquation2(ampS2,freqX, phase,damping,sample_rate)
	xOft=makeXYofT(baseFuncS1,baseFuncX)
	return xOft

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

def makeNoteFactory(duration_in_samples, sample_rate,amplitude,damping):
	def makeNote(frequency):
		return np.int16(np.array([amplitude*math.sin(2.0 * math.pi * frequency * t / sample_rate)*math.pow(math.e,(-1*damping*(t/sample_rate))) for t in xrange(0, duration_in_samples)]))
	return makeNote

def makeHarmonicNoteFromFunc(sample_rate,duration_in_samples):
	func = harmonicXatT(sample_rate)
	a=[]
	for t in xrange(0, duration_in_samples):
		a.append(func(t))
	return np.int16(np.array(a))



def harmonograph():
	hFunc = harmonicXYatT()

	duration_in_samples = 100000
	sample_rate = 44100
	amplitude = 10000
	damping = .9

	pygame.mixer.pre_init(sample_rate, -16, 1, 4096)
	pygame.mixer.init()

	makeNote = makeNoteFactory(duration_in_samples,sample_rate,amplitude,damping)
	a4 = makeNote(436.05)
	print a4

	hNote = makeHarmonicNoteFromFunc(sample_rate,duration_in_samples)
	print hNote

	s2 = pygame.sndarray.make_sound(a4)
	sound2 = pygame.mixer.Sound(s2)
	s = pygame.sndarray.make_sound(hNote)
	sound = pygame.mixer.Sound(s)
	
	pygame.mixer.Sound.play(sound)
	pygame.mixer.Sound.play(sound2)

	
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
