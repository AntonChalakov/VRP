import VR

class PresenceSensor:
	""" Definiert einen Anwesenheitssensor, der Personen in seinem Gueltigkeitsbereich erkennen kann.

	Der Geltungsbereich eines Anwesenheitssensors ist ein axial ausgerichteter Quader.

	@attr name: Name dieses Sensors. Entspricht oft dem Raum, den er abdeckt. (String)
	@attr bounds: Grenzpositionen des Geltungsbereichs in alle drei Richtungen ([(int, int)])
	@attr event: Verknuepftes Event. Dieses wird aufgerufen, wenn sich eine Zustandsaenderung bzgl. Anwesenheit
	von einer Person am Sensor ergibt. (function)
	@attr personPresent: Gibt an, ob in der letzten Sensorpruefung eine Person im Geltungsbereich des Sensors
	anwesend war. (Boolean)
	"""
	def __init__(self, name, sizex, sizey, sizez, posx, posy, posz, event):
		""" Erstellt ein Objekt der Klasse PresenceSensor

		@attr name: Name des Sensors (String)
		@attr sizex: Groesse des Geltungsbereichs in x-Richtung
		@attr sizey: Groesse des Geltungsbereichs in y-Richtung
		@attr sizez: Groesse des Geltungsbereichs in z-Richtung
		@attr posx: Mittelpunkt des Geltungsbereichs in x-Richtung
		@attr posy: Mittelpunkt des Geltungsbereichs in y-Richtung
		@attr posz: Mittelpunkt des Geltungsbereichs in z-Richtung
		@attr event: Verknuepftes Event
		"""
		self.name = name

		# Calculate the bounding box
		self.bounds = [[0 for x in range(2)] for y in range(3)]
		self.bounds[0] = [posx-sizex/2.0, posx+sizex/2.0]
		self.bounds[1] = [posy-sizey/2.0, posy+sizey/2.0]
		self.bounds[2] = [posz-sizez/2.0, posz+sizez/2.0]
		
		self.event = event
		
		self.personPresent = False
		
	def test(self, person):
		""" ueberpruefe die Anwesenheit der gegebenen Person und rufe gegebenenfalls das Sensorevent aus.

		Prueft ob sich die gegebene Person im Sensorbereich befindet und rufe das Sensorevent aus, wenn sich seit der letzten
		Pruefung eine aenderung ergeben hat. Dies ist der Fall, wenn die Person in dem Zeitraum seit der letzten Pruefung
		den Sensorbereich betreten oder verlassen hat. Weiterhin wird bei einer aenderung eine entsprechene Meldung an die
		Konsole ausgegeben.

		@person: Person, bzw. Kamera deren Position geprueft werden soll (VR.Camera)
		"""
		personFrom = person.getWorldFrom()
		
		isInBox = True
		for i in [0,1,2]:
			if personFrom[i] < self.bounds[i][0] or personFrom[i] > self.bounds[i][1]:
				isInBox = False
				break

		if self.personPresent != isInBox:
			print self.name + ": " + str(isInBox)
			self.event(VR.CameraId, isInBox)
			self.personPresent = isInBox