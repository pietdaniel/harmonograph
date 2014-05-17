
# def hEquation2(amplitude, frequency, phase, damping, sample_rate):
# 	def hFunc(time):
# 		val = amplitude*math.sin(2*math.pi*frequency*time/sample_rate + float(phase))*math.pow(math.e,(-1*damping*time/sample_rate))
# 		return val
# 	return hFunc


# def harmonicXatT(sample_rate):
# 	freqX = 261.63
# 	ratio1 = 0.0
# 	freqS1 = ratio1 * freqX
# 	ampS1 = 10000
# 	ampS2 = 10000
# 	ampX = 10000
# 	damping = .9
# 	phase = 0 
# 	baseFuncS1 = hEquation2(ampS1,freqS1, phase,damping,sample_rate)
# 	baseFuncX = hEquation2(ampS2,freqX, phase,damping,sample_rate)
# 	xOft=makeXYofT(baseFuncS1,baseFuncX)
# 	return xOft

# def makeHarmonicNoteFromFunc(sample_rate,duration_in_samples):
# 	func = harmonicXatT(sample_rate)
# 	a=[]
# 	for t in xrange(0, duration_in_samples):
# 		a.append(func(t))
# 	return np.int16(np.array(a))


	# hNote = makeHarmonicNoteFromFunc(sample_rate,duration_in_samples)
	# s = pygame.sndarray.make_sound(hNote)
	# sound = pygame.mixer.Sound(s)
	# pygame.mixer.Sound.play(sound)