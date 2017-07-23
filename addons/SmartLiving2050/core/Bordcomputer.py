import VR
from PresenceSensor import PresenceSensor

openLeft = {1:[0,1,0], -1:[0,-1,0], 100:[0,1,0], -100:[0,-1,0]}
openRight = {1:[-1,0,0], -1:[1,0,0], 100:[0,0,-1], -100:[0,0,1]}


class Bordcomputer(object):
	

	def __init__(self, name, transform, sliding=True, openSide="left", width = 0.84):
		""" Instanziiere ein Objekt der Klasse Door.

		Abhaengig der Parameter werden die Animationspfade zum oeffnen und Schliessen der Tuer berechnet.

		@param name: Der Name der Tuer um sie zu identifizieren; Sollte eindeutig sein, wird aber nicht geprueft
		@param transform: Transform-Objekt der Tuer (VR.Transform)
		@param sliding: Angabe um welche Art Tuer es sich handelt; Schiebetuer/Schwingtuer (Boolean) (default = True)
		@param openSide: Angabe in welche Richtung sich die Schiebetuer oeffnet, bzw. an welcher Seite der Tuer  sich die
		Tuerangeln befinden. Relativ zur Richtung der Tuer; Moegliche Werte sind "left" und "right" (String) (default = "left")
		@param width: Breite der Tuer in Metern. Notwendig fuer die Animation von Schiebetueren (float) (default = 0.84)
		"""
		self.isClosed = True
		self.name = name
		self.transform = transform
		self.pos = transform.getFrom()
		self.setSize = transform.setSize
		self.xSize = 0.5
		self.ySize = 0.5
		self.pathOpen = VR.Path()
		self.pathClose = VR.Path()
		
		self.direction = self.transform.getDir()
		dirIndex = self.direction[0] * 100 + self.direction[1]
		
		if not sliding:
			if openSide == "left":
				openDir = openLeft[dirIndex]
			else:
				openDir = openRight[dirIndex]

			self.pathOpen.addPoint(self.pos, self.direction, [0,0,0], [0,1,0])
			self.pathOpen.addPoint(self.pos, openDir, [0,0,0], [0,1,0])
			self.pathOpen.compute(2)

			self.pathClose.addPoint(self.pos, openDir, [0,0,0], [0,1,0])
			self.pathClose.addPoint(self.pos, self.direction, [0,0,0], [0,1,0])
			self.pathClose.compute(2)
		
		else:
			
			closePos = self.pos
			
			openWidth = width - 0.02
			
			if openSide == "left":
				translation = [x*openWidth for x in openLeft[dirIndex]]
			else:
				translation = [x*openWidth for x in openRight[dirIndex]]
				
			openPos = [closePos[i] + translation[i] for i in range(3)]
			self.openPos = openPos
			self.closePos = closePos
			
			self.pathOpen.addPoint(closePos, self.direction, [0,0,0], [0,0,1])
			self.pathOpen.addPoint(openPos, self.direction, [0,0,0], [0,-1,1])
			self.pathOpen.addPoint(openPos, [0,0,1], [0,0,0], [0,-1,1])
			self.pathOpen.compute(3)

			self.pathClose.addPoint(openPos, [0,0,1], [0,0,0], [0,-1,1])
			self.pathClose.addPoint(openPos, self.direction, [0,0,0], [0,-1,1])
			self.pathClose.addPoint(closePos, self.direction, [0,0,0], [0,0,1])
			self.pathClose.compute(3)

	def setOpen(self):
		""" oeffne die Tuer, falls sie geschlossen ist, und fuehre entsprechende Animation aus.
		"""
		if self.isClosed:
			self.transform.animate(self.pathOpen, 1, 0, True)
			
			self.transform.setSize(1.5,1.5)
			self.isClosed = False
		

	def setClosed(self):
		""" Schliesse die Tuer, falls sie geoeffnet ist, und fuehre die entsprechende Animation aus.
		"""
		if not self.isClosed:
			self.transform.animate(self.pathClose, 1, 0, True)
			
			self.isClosed = True
		
	
	def toggle(self):
		""" oeffne, oder schliesse, die Tuer abhaengig von ihrem oeffnungszustand.
		"""
		if self.isClosed:
			self.setOpen()
		else:
			self.setClosed()
