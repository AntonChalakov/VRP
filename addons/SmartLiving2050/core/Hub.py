import VR
import random
from datetime import datetime
from Clock import Clock, days
from AccessGroup import AccessGroup
from Person import Person
from TimedEvent import TimedEvent


class Hub:
	""" Diese Klasse repraesentiert den zentralen Hub des Smart Homes, der alle Geraete und Funktionalitaeten verwaltet.

	Der Hub enthaelt Referenzen auf saemtliche Smart-Objekte und zusaetzlich benoetigter Peripherie, um das Smart Home
	zu verwalten. Hier werden Zugangsberechtigungen geprueft und Reparaturtermine vereinbart. Er enthaelt zudem alle 
	statisch definierten Events (keine TimedEvents) der diversen Sensoren und Smart-Geraete.

	@attr clock: Uhr, welche den aktuellen Wochentag und die Uhrzeit der virtuellen Umgebung angibt (Clock)
	@attr mainDoor: Eingangstuer zur Wohnung. Kann vom Hub geoeffnet werden um Personen mit Zugangsberechtigung den 
	Zutritt zur Wohnung ermoeglichen. (Door)
	@attr rooms: Liste der Raeume des Smart Homes ([Room])
	@attr clocks: Liste der ID-Nummern saemtlicher "physischer" Uhr-Objekte im Smart-Home
	@attr doors: Liste saemtlicher Tueren in dem Smart Home ([Door])
	@attr lamps: Liste saemtlicher Lampen in dem Smart Home ([Lamp])
	@attr radiators: Liste saemtlicher Heizungen in dem Smart Home ([Radiator])
	@attr sensors: Liste saemtlicher Praesenzsensoren in dem Smart Home ([PresenceSensor])
	@attr accessGroups: Dictionary der verschiedenen Gruppen fuer Zugangsrechte zum Smart Home,	sortiert nach Namen
	({String : AccessGroup})
	@attr persons: Dictionary saemtlicher, dem Hub bekannter, Personen, sortiert nach ihren ID-Nummern ({int : Person})
	@attr presentIds: Liste der aktuell im Smart Home anwesenden Personen anhand ihrer IDs ([int])
	@attr presenceLog: Liste saemtlicher Log-Eintraege, die der Hub ueber die Wohnung betretenden und verlassenden Personen
	angefertigt hat. Besteht aus einem Stichwort ueber die getaetigte Aktion, "Arrival", "Departure", oder "Denial" bei einem 
	zurueckgewiesenem Zutrittsversuch, der ID der betreffenden Person und der Zeit des Eintrags ([String, int, [int, int, int, int]])
	"""
	def __init__(self):
		""" Erstellt eine Instanz des Hubs. Stellt die VR-Zeit initial auf reale/n Wochentag und Uhrzeit.
		"""
		now = datetime.today()
		self.clock = Clock(now.weekday(), now.hour, now.minute, now.second)
		
		self.mainDoor = None
		self.rooms = []
		self.clocks = []
		self.doors = []
		self.lamps = []
		self.radiators = []
		self.sensors = []
		self.bordcomputers = []
		
		self.accessGroups = {}
		self.persons = {}
		self.presentIds = []
		self.presenceLog = []
		
	def eventBordcomputerToggle(self,personId, bordcomputer):
		
		bordcomputer.toggle()
			

	def eventDoorToggle(self, personId, door):
		""" Oeffne / schliesse Tuer abhaengig von der Erlaubnis

		Wird aufgerufen wenn manuell versucht wird eine Tuer zu oeffnen / schliessen.
		Eine Tuer kann geoeffnet werden, wenn die entsprechende Berechtigung existiert.
		Eine Tuer kann immer geschlossen werden, und die Wohnungstuer kann immer von innen geoeffnet werden,
		um die Wohnung zu verlassen.
		Bei einem fehlgeschlagenen Versuch eine Tuer zu oeffnen wird diese ueber ein TimedEvent fuer 1.5 Sekunden
		roetlich eingefaerbt und weitestgehend undurchsichtig.

		@param personId: ID der Person, die eine Tuer betaetigen will (int)
		@param door: Tuer, die geoeffnet oder geschlossen werden soll (Door)
		"""
		if self.hasAccess(personId, door):
			# Person has access, all is well
			door.toggle()
			if door == self.mainDoor and door.insideSensor.personPresent:
				self.mainDoor.personExiting = True
		elif not door.isClosed:
			# Person has no access, but can close door.
			door.setClosed()
		elif door == self.mainDoor and door.insideSensor.personPresent: 
			# Person has no access, but is allowed to leave the apartment
			self.mainDoor.personExiting = True
			door.setOpen()
		elif door != self.mainDoor:
			# Person has no access, tries to open other door than main.
			door.transform.getChild(0).setMaterial(VR.materials["Glassdoor locked"])
			def event():
				door.transform.getChild(0).setMaterial(VR.materials["Glassdoor unlocked"])
			newEvent = TimedEvent(1.5, event)
			VR.timedEvents.append(newEvent)


	def eventMainDoorOutside(self, personId, entering):
		""" Definiere das Verhalten fuer eine Sensoraenderung auf der Aussenseite der Wohnungstuer.

		Kann die Wohnungstuer fuer eine ankommende Person mit Zugangsberechtigun automatisch oeffnen,
		oder die Tuer hinter einer gehenden Person schliessen.

		@param personId: ID der Person, die den Tuersensor ausgeloest hat (int)
		@param entering: Ob die Person den Sensorbereich betreten oder verlassen hat (Boolean)
		"""
		if self.mainDoor.isClosed:
			if entering:
				# Check for access right
				
				if self.hasAccess(personId, self.mainDoor):
					self.mainDoor.setOpen()
					self.mainDoor.personEntering = True
				else:
					self.presenceLog.append(("Denial", personId, self.clock.get()))
					
		else:
			if entering:
				if self.mainDoor.personExiting:
					self.presentIds.remove(personId)
					self.presenceLog.append(("Departure", personId, self.clock.get()))
					
			else:
				if self.mainDoor.personExiting:
					self.mainDoor.setClosed()
					self.mainDoor.personExiting = False
				else:
					# TODO: what if a person leaves sensor area after opening the door, without entering the apartment?
					pass
					
	def eventMainDoorInside(self, personId, entering):
		""" Definiere das Verhalten fuer eine Sensoraenderung auf der Innenseite der Wohnungstuer.

		Kann die Tuer hinter einer ankommenden Person schliessen.

		@param personId: ID der Person, die den Tuersensor ausgeloest hat (int)
		@param entering: Ob die Person den Sensorbereich betreten oder verlassen hat (Boolean)
		"""
		if self.mainDoor.isClosed:
			# Door does not open automatically from the inside.
			pass
		else:
			if entering:
				if self.mainDoor.personEntering:
					self.presentIds.append(personId)
					self.presenceLog.append(("Arrival", personId, self.clock.get()))
			else:
				if self.mainDoor.personEntering:
					self.mainDoor.setClosed()
					self.mainDoor.personEntering = False

	def eventPresenceChange(self, room, personId, entering):
		""" Definiere das Verhalten fuer eine Sensoraenderung eines Anwesenheitssensors in einem Raum.

		Schaltet die Lampen des Raums danach um, ob sich eine Person in diesem befindet.

		@param room: Der Raum, der die Aenderung meldet (Room)
		@param personId: Die ID, die die Aenderung ausgeloest hat (int)
		@param entering: Ob die Person den Raum betreten oder verlassen hat (Boolean)
		"""
		if entering:
			room.switchAllLamps(True)
			room.presentIds.append(personId)
			self.presentIds.append(personId)
		elif not entering:
			room.switchAllLamps(False)
			room.presentIds.remove(personId)

	def eventDevice(self, device):
		""" Definiere das Verhalten fuer eine Sensoraenderung eines Geraets

		Erstellt einen Reparaturtermin bei auftretendem Defekt.
		Gibt eine Meldung an die Middleware abhaengig vom Geraete-Zustand.

		@param device: Das Geraet, dessen Zustand sich geaendert hat (Device)
		"""
		# if device.type() == "RADIATOR" and not device.is_ok():   - jzehnter 2017-02-08 (nach Absprache mit Lars)
		if not device.is_ok():
			self.createAppointment(device)

		if device.is_ok():
			VR.mw.mw.pvr_repaired_device(device)
		else:
			VR.mw.mw.pvr_broken_device(device)


	def createAppointment(self, brokenDevice):
		""" Organisiere einen Termin zu einer zufaelligen Uhrzeit am naechsten moeglichen Werktag

		Simuliert eine Terminvereinbarung fuer einen Techniker zur Reparatur. Ein Defekt vor 13:00 resultiert
		in einem Termin am naechsten Werktag, ein Defekt spaeter am Tag fuehrt zu einem Termin am uebernaechsten.
		Eine Ausnahme bildet die Zeit von Donnerstag Nachmittag bis inkl. Sonntag Vormittag, welches immer zu 
		einem Termin am Montag fuehrt. Das Zeitfenster des Termins beginnt zu einer zufaelligen vollen Stunde
		zwischen 08:00 und 15:00 und hat eine fixe Dauer von drei Stunden.
		Fuer den reparierenden Techniker wird in diesem Zeitfenster automatisch eine Zugangsberechtigung zu den 
		Raeumen erstellt, die fuer die Reparatur zugaenglich sein muessen.
		Eine Meldung ueber den Vorfall und den Reparaturtermin wird auf die Konsole ausgegeben.

		@param brokenDevice: Das Geraet, fuer das ein Reparaturtermin vereinbart werden muss
		"""
		now = self.clock.get()
		day = now[0]
		hour = now[1]
		
		# Simulate arrangement of appointment timeframe
		if day < 4 and hour < 13:
			appointmentDay = day + 1
		elif day < 3 and hour >= 13:
			appointmentDay = day + 2
		elif day == 6 and hour >= 13:
			appointmentDay = 1
		else:
			appointmentDay = 0
			
		startTime = [int(random.random()*7 + 8),0]
		endTime = [startTime[0] + 3, 0]
		
		# Simulate recipience of personal identification of repairing engineer
		idFound = False
		engineerId = 100
		'''while not idFound:
			engineerId = int(random.random()*100000000)
			if engineerId not in self.persons:
				idFound = True'''
				
		engineerData = [engineerId, "Mario Klempnertyp"]
		
		# Create appropriate access group and appoint access right for appointment time frame
		groupName = "Repair Service " + brokenDevice.type() + " " + brokenDevice.id()
		engineerGroup = AccessGroup(groupName, False)
		engineerGroup.addAccessRight(appointmentDay, startTime, endTime, [brokenDevice.room()])
		self.accessGroups[engineerGroup.name] = engineerGroup
		
		engineer = Person(engineerData[0], engineerGroup, engineerData[1])
		self.persons[engineerId] = engineer
		

		print "Appointment for repair of " + brokenDevice.__class__.__name__ + " in the " + brokenDevice.room() + ": " \
			+ days[appointmentDay] + ", between " + str(startTime[0]) + ":00 and " + str(endTime[0]) + ":00."
		print "Your technician will be " + engineer.name + ", ID: " + str(engineer.idNumber) + "."
			
		brokenDevice.set_repairAppointment(appointmentDay, startTime, endTime)

	def hasAccess(self, personId, door):
		""" Pruefe ob die gegebene Person zum gegebenen Zeitpunkt Zugang zur gegebenen Tuer hat.

		@param personId: ID-Nummer der betreffenden Person (int)
		@param door: Listenindex der betreffenden Tuer (siehe class AccessGroup) (int)
		"""
		timeStamp = self.clock.getTimeStamp()
		return (personId in self.persons) and self.persons[personId].hasAccess(timeStamp, door)

	def addDoor(self, door, isMain=False):
		""" Setup zum hinzufuegen von Tueren zur Wohnung

		TODO: angrenzende Raeume uebergeben, damit generisch!

		@param door: Die Tuer, die hinzugefuegt werden soll (Door)
		@param isMain: Ob die gegebene Tuer die Wohnungstuer ist (Boolean)
		"""
		if not self.mainDoor and isMain: self.mainDoor = door
		self.doors.append(door)
	
	def addBordcomputer(self, bordcomputer):
		
		self.bordcomputers.append(bordcomputer)
	

	def addRoom(self, room):
		""" Setup zum hinzufuegen von Raeumen zur Wohnung

		@param room: Der Raum, der hinzugefuegt werden soll (Room)
		"""
		self.rooms.append(room)

	def devices(self):
		""" Gebe eine Liste von allen Geraeten in der Wohnung zurueck.

		@return: Liste von allen Geraeten in der Wohnung
		"""
		devices = []
		for r in self.rooms:
			for d in r.lamps:
				devices.append(d)
			for d in r.radiators:
				devices.append(d)
		return devices
	
	def get_time(self):
		""" Gebe die aktuelle Zeit zurueck

		@return: Aktuelle Zeit als dict mit keys 'day', 'hour' und 'minute'
		"""
		time = self.clock.get()
		return {'day':time[0], 'hour':time[1], 'minute':time[2]}
	
	def set_time(self, d, h, m):
		""" Aendere die aktuelle Zeit

		@param d: Der Tag auf den die Zeit gesetzt werden soll (int oder String)
		@param h: Die Stunde auf die die Zeit gesetzt werden soll (int)
		@param m: Die Minute auf die die Zeit gesetzt werden soll (int)
		@return: Aktuelle Zeit als dict mit keys 'day', 'hour' und 'minute'
		"""
		self.clock.set(d, h, m)
		return self.get_time()
	
	def printLog(self):
		""" Gebe eine formatierte Version des Anwesenheitslogs des Hubs auf die Konsole aus.
		"""
		print "Presence Log: "
		for entry in self.presenceLog:
			nameId = entry[1]
			if entry[1] in self.persons:
				nameId = self.persons[entry[1]].name
				
			print "  {0} {1}: {2}, {3}:{4}:{5}".format(entry[0], nameId, days[entry[2][0]], entry[2][1], entry[2][2], entry[2][3])
		print "End of Log"
