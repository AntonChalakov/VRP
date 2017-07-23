import VR

class Person:
	""" Diese Klasse definiert eine Person in der VR-Umgebung.

	Eine Person wird aktuell rein im Kontext ihrer Zugangsberechtigung angewendet.

	@attr idNumber: Eindeutige Identifikationnummer fuer die Erkennung durch die Sensoren (int)
	@attr name: Name der Person, zur leichteren Identifikation durch den Nutzer (String)
	@attr accessGroup: Gruppe mit Zugangsberechtigungen, zu der diese Person gehoert (AccessGroup)
	"""
	def __init__(self, idNumber, accessGroup, name="Unknown"):
		""" Erstelle ein Objekt der Klasse Person

		@attr idNumber: Eindeutige Identifikationnummer fuer die Erkennung durch die Sensoren (int)
		@attr accessGroup: Gruppe mit Zugangsberechtigungen, zu der diese Person gehoert (AccessGroup)
		@attr name: Name der Person, zur leichteren Identifikation durch den Nutzer (String) (default = "Unknown")
		"""
		self.idNumber = idNumber
		self.name = name
		self.accessGroup = accessGroup

	def hasAccess(self, timestamp, door):
		""" Prueft, ob diese Person zur gegebenen Zeit eine Berechtigung fuer die gegebene Tuer hat.

		@param timestamp: Zeitstempel des aktuellen Zeitpunkts (int)
		@param door: Tuer, zu der der Zugang geprueft werden soll (Door)

		@return: Wahrheitswert, ob eine Zugangsberechtigung existiert (Boolean)
		"""
		return self.accessGroup.hasAccess(timestamp, door)

	

