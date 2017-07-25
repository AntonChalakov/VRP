import VR

class Device(object):
	""" Allgemeine Klasse fuer Smart-Geraete.

	Klasse kann direkt instanziiert werden fuer nicht naeher spezifizierte Geraete
	oder als Superklasse fuer spezifischer definierte Geraete fungieren.

	@attr _id: eindeutige Identifikationsnummer des Geraets (int)
	@attr _type: Typ des Geraets (String)
	@attr _ok: Zustand des Geraets; funktionierend/defekt (Boolean)
	@attr _room: Raum, in dem sich das Geraet befindet (String)
	@attr _repairAppointment: Enthaelt den Termin zur Reparatur, 
	falls das Geraet einen aktuellen, oder vergangenen Defekt hat/hatte in der Form 
	[Tag, Zeitpunkt Beginn, ZeitpunktEnde] ([int, [int,int], [int,int]])
	"""

	def __init__(self, item_id, item_type, is_ok, room_name, geometry):
		""" Instanziiere ein Objekt der Klasse Geraet.

		@param item_id: Die Identifikationsnummer des Geraets (int)
		@param item_type: Der Typ des Geraets (String)
		@param is_ok: Der Zustand des Geraets; funktionierend/defekt (Boolean)
		@param room_name: Der Raum in dem sich das Geraet befindet (String)
		@param geometry: Das Objekt, das zum reparieren angeklickt wird (VR.Geometry)
		"""
		self._id   = item_id
		self._type = item_type
		self._ok   = is_ok
		self._room = room_name
		self._geometry = geometry
		self._repairAppointment = []

	def id(self):
		""" Gebe die ID des Geraets aus.

		@return: ID des Geraets
		"""
		return self._id

	def type(self):
		""" Gebe den Typ des Geraets aus.

		@return: Der Typ des Geraets (String)
		"""
		return self._type

	def is_ok(self):
		""" Gebe den Zustand des Geraets aus.

		@return: Der Zustand der Geraets (Boolean)
		"""
		return self._ok

	def room(self):
		""" Gebe den Raum aus, in dem sich das Geraet befindet.

		@return: Der Raum in dem sich das Geraet befindet (String)
		"""
		return self._room

	def set_broken(self):
		""" Verursache einen Defekt an dem Geraet.

		Der Zustand des Geraets wird auf False (=defekt) gesetzt. Eine Meldung hierzu wird auf der Debug-Konsole ausgegeben
		und ein entsprechendes Event wird auf dem zentralen Hub aufgerufen.
		"""
		if not self._ok:
			print("{0} {1} in {2} is already broken.".format(self._type, self._id, self._room))
		else:
			print("{0} {1} in {2} broke down.".format(self._type, self._id, self._room))
			self._ok = False
			self.sendEvent()

	def set_repaired(self):
		""" Repariere das Geraet.

		Der Zustand des Geraets wird auf True (=funktionstuechtig) gesetzt. Eine Meldung hierzu wird auf der Debug-Konsole ausgegeben
		und ein entsprechendes Event wird auf dem zentralen Hub aufgerufen.
		"""
		if self._ok:
			print("{0} {1} in {2} is already repaired.".format(self._type, self._id, self._room))
		else:
			print("{0} {1} in {2} has been repaired.".format(self._type, self._id, self._room))
			self._ok = True
			self.sendEvent()

	def toggle_ok(self):
		""" Aendere den Zustand des Geraets.

		Abhaengig vom vorherigen Zustand wird das Geraet defekt / funktionstuechtig
		"""
		if not self._ok:
			self.set_repaired()
		else:
			self.set_broken()

	def set_dirty(self):
		if not self._ok:
			print("{0} {1} in {2} is already dirty.".format(self._type, self._id, self._room))
		else:
			print("{0} {1} in {2} is dirty.".format(self._type, self._id, self._room))
			self._ok = False
			self.sendEvent()
		

	def set_geometry(self, geometry):
		""" Setter fuer _geometry

		Setzt _geometry auf das uebergebene Objekt. Notwendig falls verschiedene Modelle
		fuer ein funktionstuechtiges / defektes Geraet angezeigt werden.
		@param geometry: Das neue Klick-Target (VR.Geometry)
		"""
		self._geometry = geometry

	def sendEvent(self):
		""" Rufe das zugehoerige Event auf dem zentralen Hub auf.
		"""
		VR.hub.eventDevice(self)
	
	def get_repairAppointment(self):
		""" Gebe den bestehenden Eintrag fuer den Reparaturtermin des Geraets aus.

		Wenn kein aktueller oder vergangener Termin besteht wird eine leere Liste ausgegeben.
		
		@return: Liste mit dem Reparturtermin [Tag, Beginn, Ende], oder leere Liste ([int, [int,int], [int,int]])
		"""
		return self._repairAppointment
	
	def set_repairAppointment(self, day, startTime, endTime):
		""" Erstelle einen Reparaturtermin fuer das Geraet zur gegebenen Zeit

		@param day: Tag des Termins (int)
		@param startTime: Beginn des Termins in Stunde, Minute ([int, int])
		@param endTime: Ende des Termins in Stunde, Minute ([int, int])
		"""
		self._repairAppointment = [day, startTime, endTime]
		
