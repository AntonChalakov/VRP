import VR
import Clock

doors = ["Main", "HW1_LR", "LR_Ki", "LR_HW2", "HW2_BaR", "HW2_GBR", "HW2_BeR", "HW2_KR", "Balcony"]
roomAccess = {
	"Hallway1": [0],
	"Hallway2": [0,1,3,8],
	"Livingroom": [0,1,8],
	"Kitchen": [0,1,2,8],
	"Bathroom": [0,1,3,4,8],
	"GuestBathR": [0,1,3,5,8],
	"Bedroom": [0,1,3,6,8],
	"KidsRoom": [0,1,3,7,8],
	"Complete": [0,1,2,3,4,5,6,7,8]}


class AccessGroup:
	""" Definiere eine Gruppe zur Verwaltung von Zugangsberechtigungen zum Smart Home.

	Eine Gruppe kann 0 bis n Personen zugeordnet sein.
	Eine Zugangsberechtigung bei zugangsbeschraenkten Gruppen besteht aus Zeitstempeln fuer Beginn und Ende der Berechtigung 
	und einer Liste von Tueren, die in dieser Berechtigung enthalten sind.

	@attr name: Name der Gruppe (String)
	@attr isUnlimited: Gibt an, ob die Gruppe unbeschraenkten Zutritt hat (Boolean)
	@attr accessRights: Einzelne Berechtigungszeitraeume bei zugangsbeschraenkten Gruppen 
	inklusive Zugangsberechtigungen nach Raeumen ([(Integer, Integer, [int])]
	"""

	def __init__(self, name, isUnlimited=False):
		""" Instanziiere ein Objekt der Klasse AccessGroup.

		@param name: Name der Gruppe (String)
		@param isUnlimited: Gibt an, ob die Gruppe unbeschraenkten Zutritt hat (Boolean) (default = False)
		"""
		self.name = name
		self.isUnlimited = isUnlimited
		self.accessRights = []
		
	def hasAccess(self, timestamp, door):
		""" Pruefe ob die Gruppe zu gegebenem Zeitpunkt und Tuer Zugang hat.

		@param timestamp: Zeitstempel fuer Tag und Uhrzeit (int)
		@param door: Die zu oeffnende Tuer (Door)

		@return: Gibt an ob Zugang gewaehrt wird. (Boolean)
		"""
		if self.isUnlimited:
			return True
		
		for access in self.accessRights:
			if access[0] <= timestamp and timestamp < access[1]:
				return door.name in access[2]
			
		return False

	
	def addAccessRight(self, weekday, startTime=[0,0], endTime=[0,0], openRooms=["Complete"]):
		""" Fuege eine neue Zugangsberechtigung hinzu.

		Wenn diese sich ganz oder teilweise mit einer bestehenden Zugangsberechtigung ueberschneidet,
		wird die alte Berechtigung im Zeitraum der neuen Berechtigung ueberschrieben.

		@param weekday: Wochentag fuer die Zugangsberechtigung (String)
		@param startTime: Beginn des Berechtigungszeitraums in Stunde und Minute [int, int]
		@param endTime: Ende des Berechtigungszeitraums in Stunde und Minute [int, int]
		@param openRooms: Liste der Raeume, fuer die diese Berechtigung gelten soll

		@return: Wahrheitswert, der angibt ob die neue Berechtigung erfolgreich erstellt wurde 
		"""

		if weekday not in Clock.days or \
			startTime[0] not in range(24) or startTime[1] not in range(60) or \
			endTime[0] not in range(24) or endTime[1] not in range(60):
				
			print "Invalid input. Please try again."
			return False


		startTimeStamp = Clock.timeStamp(weekday, startTime[0], startTime[1])
		endTimeStamp = Clock.timeStamp(weekday, endTime[0], endTime[1])
		
		
		if startTimeStamp >= endTimeStamp:
			print "Start time after end time. Please try again."
			return False


		openDoorList = []
		for door in openRooms:
			accessList = roomAccess[door]
			for item in accessList:
				if doors[item] not in openDoorList:
					openDoorList.append(doors[item])
		
		# Check if another accessRight already exists in the given timeframe
		# if so, overwrite it
		for i in reversed(range(len(self.accessRights)-1)):
			access = self.accessRights[i]
			if startTimeStamp <= access[0] and endTimeStamp >= access[1]:
				# new access right STARTS BEFORE start of old one and ENDS AFTER end of old one
				self.accessRights.pop(i)
			elif startTimeStamp <= access[0] and endTimeStamp > access[0]:
				# new access right STARTS BEFORE start of old one and ENDS BEFORE end of old one
				self.accessRights[i][0] = endTimeStamp
			elif startTimeStamp < access[1] and endTimeStamp >= access[1]:
				# new access right STARTS AFTER start of old one and ENDS AFTER end of old one
				self.accessRights[i][1] = startTimeStamp
			elif startTime > access[0] and endTimeStamp < access[1]:
				# new access right STARTS AFTER start of old one and ENDS BEFORE end of old one
				self.accessRights.append([endTimeStamp, access[1], access[2]])
				self.accessRights[i][1] = startTimeStamp
		
		self.accessRights.append([startTimeStamp, endTimeStamp, openDoorList])
		return True
		
