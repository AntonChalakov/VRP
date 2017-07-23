import VR
from PresenceSensor import PresenceSensor

openLeft = {1:[1,0,0], -1:[-1,0,0], 100:[0,0,1], -100:[0,0,-1]}
openRight = {1:[-1,0,0], -1:[1,0,0], 100:[0,0,-1], -100:[0,0,1]}


class Door(object):
	""" Definiere eine Tuer fuer die VR-Umgebung.

	In dieser Klasse ist die "physische" Form der Tuer fuer die VR-Umgebung definiert. 
	
	@attr isClosed: Der oeffnungszustand er Tuer; geschlossen/offen (Boolean)
	@attr transform: Das Transform-Objekt der Tuer, welches die Geometrie der Tuer enthaelt und fuer die
	oeffnungs- und Schliess-Animation dieser benoetigt wird. (VR.Transform)
	@attr pos: Position der Tuer, relativ zu ihrem Elternobjekt in der VR-Umgebung ([float, float, float])
	@attr pathOpen: Animationspfad zum oeffnen der Tuer (VR.Path)
	@attr pathClose: Animationspfad zum Schliessen der Tuer (VR.Path)
	@attr direction: Richtungsvektor der Tuer,  relativ zu ihrem Elternobjekt in der VR-Umgebung ([float, float, float])
	"""

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

		self.pathOpen = VR.Path()
		self.pathClose = VR.Path()
		
		self.direction = self.transform.getDir()
		dirIndex = self.direction[0] * 100 + self.direction[2]
		
		if not sliding:
			if openSide == "left":
				openDir = openLeft[dirIndex]
			else:
				openDir = openRight[dirIndex]

			self.pathOpen.addPoint(self.pos, self.direction, [0,0,0], [0,1,0])
			self.pathOpen.addPoint(self.pos, openDir, [0,0,0], [0,1,0])
			self.pathOpen.compute(20)

			self.pathClose.addPoint(self.pos, openDir, [0,0,0], [0,1,0])
			self.pathClose.addPoint(self.pos, self.direction, [0,0,0], [0,1,0])
			self.pathClose.compute(20)
		
		else:
			
			closePos = self.pos
			
			openWidth = width - 0.02
			
			if openSide == "left":
				translation = [x*openWidth for x in openLeft[dirIndex]]
			else:
				translation = [x*openWidth for x in openRight[dirIndex]]
				
			openPos = [closePos[i] + translation[i] for i in range(3)]
			
			self.pathOpen.addPoint(closePos, self.direction, [0,0,0], [0,1,0])
			self.pathOpen.addPoint(openPos, self.direction, [0,0,0], [0,1,0])
			self.pathOpen.compute(2)

			self.pathClose.addPoint(openPos, self.direction, [0,0,0], [0,1,0])
			self.pathClose.addPoint(closePos, self.direction, [0,0,0], [0,1,0])
			self.pathClose.compute(2)

	def setOpen(self):
		""" oeffne die Tuer, falls sie geschlossen ist, und fuehre entsprechende Animation aus.
		"""
		if self.isClosed:
			self.transform.animate(self.pathOpen, 1, 0, True)
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

class MainDoor(Door):
	""" Subklasse von Door zur Definition einer "Haupttuer", dem Zugang zur Wohnung.

	Diese Klasse bietet zusaetzliche Funktionalitaet fuer die Eingangstuer zum Smart-Home, um das 
	automatische oeffnen und Schliessen der Tuer beim Betreten der Wohnung zu implementieren.

	@attr outsideSensor: Anwesenheitssensor fuer Personen im Bereich der Tuer, ausserhalb der Wohnung (PresenceSensor)
	@attr insideSensor: Anwesenheitssensor fuer Personen im Bereich der Tuer, innerhalb der Wohnung (PresenceSensor)
	@attr personEntering: Angabe, ob aktuell eine Person dabei ist die Wohnung zu betreten.
	Noetig fuer das automatisierte oeffnen und Schliessen der Tuer. (Boolean)
	@attr personExiting: analog zu personEntering (Boolean)
	"""
	def __init__(self, name, transform, openSide="left"):
		""" Instanziiere eine Eingangstuer.

		Die Eingangstuer wird mit einem importierten 3D-Modell erstellt und ist keine Schwingtuer.

		@param transform: Transform-Objekt des importierten Tuermodells. Enthaelt unnoetige Hierarchieebenen,
		die bei der Weitergabe in den Superkonstruktor entfernt werden.
		@param openSide: Angabe an welcher Seite der Tuer sich die Tuerangeln befinden.
		Relativ zur Richtung der Tuer; Moegliche Werte sind "left" und "right" (String) (default = "left")
		"""
		super(MainDoor, self).__init__(name, transform.getChild(0).getChild(0), False, openSide)
		
		
		oSensor = VR.Geometry("Outside Sensor")
		self.transform.addChild(oSensor)
		oSensor.setPose([0.43,0,0.5],[0,0,1],[0,1,0])
		oSensorPos = oSensor.getWorldFrom()
		oSensor.destroy()
		
		iSensor = VR.Geometry("Inside Sensor")
		self.transform.addChild(iSensor)
		iSensor.setPose([0.43,0,-0.5],[0,0,1],[0,1,0])
		iSensorPos = iSensor.getWorldFrom()
		iSensor.destroy()
				
		self.outsideSensor = PresenceSensor("Maindoor Outside", 1, 2.4, 1, oSensorPos[0], 1.2, oSensorPos[2], self.oSensorEvent)
		VR.presenceSensors.append(self.outsideSensor)
		self.insideSensor = PresenceSensor("Maindoor Inside", 1, 2.4, 1, iSensorPos[0], 1.2, iSensorPos[2], self.iSensorEvent)
		VR.presenceSensors.append(self.insideSensor)
		
		self.personEntering = False
		self.personExiting = False
		
	def oSensorEvent(self, personId, entering):
		""" Gebe ein Event vom aeusseren Anwesenheitssensor an den zentralen Hub weiter.

		@param personId: ID der Person im Sensorbereich
		"""
		VR.hub.eventMainDoorOutside(personId, entering)
		
	def iSensorEvent(self, personId, entering):
		""" Gebe ein Event vom inneren Anwesenheitssensor an den zentralen Hub weiter.
		"""
		VR.hub.eventMainDoorInside(personId, entering)
	
