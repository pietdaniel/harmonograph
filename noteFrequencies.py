class noteFrequencies():
	def __init__(self):
		self.notes = \
						 {'C4' : {'just':261.63, 'equal':261.63},\
						 'C4#': {'just':272.54, 'equal':277.18},\
						 'D4' : {'just':294.33, 'equal':293.66},\
						 'E4B': {'just':313.96, 'equal':311.13},\
						 'E4' : {'just':327.03, 'equal':329.63},\
						 'F4' : {'just':348.83, 'equal':349.23},\
						 'F4#': {'just':367.92, 'equal':369.99},\
						 'G4' : {'just':392.44, 'equal':392.00},\
						 'A4B': {'just':418.60, 'equal':415.30},\
						 'A4' : {'just':436.05, 'equal':440.00},\
						 'B4B': {'just':470.93, 'equal':466.16},\
						 'B4' : {'just':490.55, 'equal':493.88},\
						 'C5' : {'just':523.25, 'equal':523.25}}

	def get(self,note,tuning='equal'):
		return self.notes[note.upper()][tuning.lower()]	