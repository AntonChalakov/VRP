import VR

class Room:
	""" Definiert einen logischen Raum in dem Smart-Home.

	Der Raum erhaelt fuer die VR-Funktionalitaet eine Referenz auf sein VR.Transform-Objekt,
	entspricht sonst aber aber einer logischen Repraesentation eines Raums in einem
	Smart Home.

	@attr name: Der Name des Raums; eindeutig (String)
	@attr transform: Das Transform-Objekt in PolyVR, das alle Elemente des Raums enthaelt (VR.Transform)
	@attr presentIds: ID-Nummern saemtlicher, in diesem Raum anwesender Personen ([int])
	@attr lamps: Liste der vorhandenen Lampen in diesem Raum ([Lamp])
	@attr radiators: Liste der vorhandenen Heizkoerper in diesem Raum ([Radiator])
	"""
	def __init__(self, name, transform):
		""" Erstelle ein Objekt der Klasse Room.

		@param name: Der Name des Raums (String)
		@param transform: Referenz auf das Transform-Objekt dieses Raums in PolyVR (VR.Transform)
		"""
		self.name = name
		self.transform = transform
		self.presentIds = []
		self.lamps = []		# physical lamp meshes
		self.radiators = []

	def switchAllLamps(self, on):
		""" Schalte alle Lampen in diesem Raum um.

		@param on: Gibt an, ob die Lampen an- oder ausgeschaltet werden sollen; an/aus (Boolean)
		"""
		for l in self.lamps:
			l.switch(on)

	def eventPresenceChange(self, personId, entering):
		""" Melde eine Aenderung in der Anwesenheit von Personen an den Hub.

		@param personId: ID-Nummer der Person, die den Raum betreten oder verlassen hat (int)
		@param entering: Gibt an, ob die Person den Raum soeben verlassen oder betreten hat; betreten/verlassen (Boolean)
		"""
		VR.hub.eventPresenceChange(self, personId, entering)
		
	def addLamp(self, lamp):
		""" Fuege dem Raum eine Lampe hinzu.

		@param lamp: Dem Raum hinzuzufuegende Lampe (Lamp)
		"""
		self.lamps.append(lamp)
