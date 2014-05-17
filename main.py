import pygame, math, types
import pygame.midi # dep?
from pygame.locals import *
from random import randint,choice,randrange
from math import pi, sin, asin, tan, cos
import os
from pprint import pprint
import midi
import numpy as np
import animation
import noteFrequencies

def hEquation(amplitude, frequency, phase, damping, sample_rate):
	def hFunc(time):
		val = amplitude*math.sin(2*math.pi*frequency*time/sample_rate + float(phase))*math.pow(math.e,(-1*damping*time/sample_rate))
		return val
	return hFunc

def makeXYofT(func1,func2):
	def xYofT(t):
		return func1(t) + func2(t)
	return xYofT

def makeXYatT(func1,func2):
	def XYatT(t):
		return (func1(t),func2(t))
	return XYatT

def harmonicXYatT(freqX,freqY, amplitude, damping, sample_rate):
	ratio1 = 0.0
	ratio2 = 0.0
	freqS1 = ratio1 * freqX
	freqS2 = ratio2 * freqY
	ampS1 = amplitude
	ampS2 = amplitude
	ampX = amplitude
	ampY = amplitude
	baseFuncS1 = hEquation(ampS1,freqS1, 0,damping, sample_rate)
	baseFuncX = hEquation(ampS2,freqX, 0,damping, sample_rate)
	baseFuncS2 = hEquation(ampX,freqS1, 0,damping, sample_rate)
	baseFuncY = hEquation(ampY,freqY, 0,damping, sample_rate)
	xOft=makeXYofT(baseFuncS1,baseFuncX)
	yOft=makeXYofT(baseFuncS2,baseFuncY)
	return makeXYatT(xOft,yOft)

#----------------------------------------


def makeNoteFactory(duration_in_samples, sample_rate,amplitude,damping):
	def makeNote(frequency):
		return np.int16(np.array([amplitude*math.sin(2.0 * math.pi * frequency * t / sample_rate)*math.pow(math.e,(-1*damping*(t/sample_rate))) for t in xrange(0, duration_in_samples)]))
	return makeNote


def harmonograph():
	notes = noteFrequencies.noteFrequencies()
	
	freqX=notes.get('c4','just')
	freqY=notes.get('g4','just')

	duration_in_samples = 400000
	sample_rate = 44100.0
	amplitude = 1000
	damping = 0.01

	hFunc = harmonicXYatT(freqX,freqY,amplitude, damping, sample_rate)

	pygame.mixer.pre_init(int(sample_rate), -16, 1, 4096)
	pygame.mixer.init()

	makeNote = makeNoteFactory(duration_in_samples,sample_rate,amplitude,damping)
	noteA = makeNote(freqX)
	noteAsndarray = pygame.sndarray.make_sound(noteA)
	noteAsound = pygame.mixer.Sound(noteAsndarray)

	noteB = makeNote(freqX)
	noteBsndarray = pygame.sndarray.make_sound(noteB)
	noteBsound = pygame.mixer.Sound(noteBsndarray)
	
	pygame.mixer.Sound.play(noteAsound)
	pygame.mixer.Sound.play(noteBsound)

	
	my_animation = animation.animation(hFunc)
	my_animation.start()

	


def main():
	harmonograph()
main()
