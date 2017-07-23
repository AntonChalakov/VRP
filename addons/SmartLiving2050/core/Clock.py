days = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3,
"Friday":4, "Saturday":5, "Sunday":6, 0:"Monday", 1:"Tuesday",
2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}

def timeStamp(d="Monday", h=0, m=0, s=0):
	""" Erstelle aus der gegebenen Zeit einen Zeitstempel.

	@param d: Wochentag (String) (default = "Monday")
	@param h: Stunde (int) (default = 0)
	@param m: Minute (int) (default = 0)
	@param s: Sekunde (int) (default = 0)
	
	@return: Zeitstempel wischen 0 (Montag, 00:00:00) und 604799 (Sonntag, 23:59:59) (int)
	"""
	if type(d) is str:
		day = days[d]
	elif type(d) is int:
		day = d
	else:
		print "Bad input on weekday"
	
	return s + 60*(m + 60*(h + 24 * day))

class Clock:
	""" Definiere eine Uhr fuer die VR-Umgebung.

	Die implementierte Zeit ist auf Wochentage vereinfacht, ein vollstaendiger Kalender ist nicht enthalten

	@attr value: Zeitstempelwert zwischen 0 (Montag, 00:00:00) und 604799 (Sonntag, 23:59:59) (int)
	@attr string: Konkatenierter Zeitwert in der Form "dddd hh:mm:ss" (String) 
	"""

	def __init__(self, d="Monday", h=0, m=0, s=0):
		""" Instanziiere ein Objekt der Klasse Uhr

		@param d: Wochentag (String) (default = "Monday")
		@param h: Stunde (int) (default = 0)
		@param m: Minute (int) (default = 0)
		@param s: Sekunde (int) (default = 0)
		"""
		if type(d) is str:
			day = days[d]
		elif type(d) is int:
			day = d
		else:
			print "Bad input on weekday"
			
		self.value = s + 60*(m + 60*(h + 24 * day))
		self.updateString()

	def set(self, d="Monday", h=0, m=0, s=0):
		""" Stelle die Uhr auf gegebene Werte fuer Wochentag und Uhrzeit ein.

		Fehlerhafte Eingaben fuer Wochentage resultieren in einem KeyError des Dictionary "days"
		uebergrosse Eingaben bei Stunden, Minuten, Sekunden werden passend in zusaetzliche Tage/Stunden/Minuten uebersetzt.

		@param d: Wochentag (String) (default = "Monday")
		@param h: Stunde (int) (default = 0)
		@param m: Minute (int) (default = 0)
		@param s: Sekunde (int) (default = 0)
		"""
		if type(d) is str:
			day = days[d]
		elif type(d) is int:
			day = d
		else:
			print "Bad input on weekday"
		self.value = s + 60*(m + 60*(h + 24 * day))
		self.string = ""
		self.updateString()

	def setFromString(self, dhms):
		""" Stelle Tag und Uhrzeit auf den gegebenen Wert.

		@param dhms: Konkatenierter Wert fuer die einzustellenden Werte 
		"""
		d, h, m, s = dhms.split(":")
		self.set(d, h, m, s)

	def get(self):
		""" Gebe die aktuelle Zeit in separierten Werten aus.

		@return: Liste der Zahlwerte fuer die aktuelle Zeit (Tag, Stunde, Minute, Sekunde)
		"""
		val = self.value
		s = val % 60
		val /= 60
		m = val % 60
		val /= 60
		h = val % 24
		val /= 24
		d = val
		return (d, h, m, s)
	
	def getTimeStamp(self):
		""" Gebe die aktuelle Zeit als Zeitstempel aus.

		@return: Zeitstempel der akutellen Zeit
		"""
		time = self.get()
		return timeStamp(time[0], time[1], time[2], time[3])

	def updateString(self):
		""" Aktualisiere die konkatenierte Textversion des aktuellen Zeitwerts.
		"""
		num = self.get()
		string = days[num[0]] + " " + \
				 str(num[1]).zfill(2) + ":" + \
				 str(num[2]).zfill(2) + ":" + \
				 str(num[3]).zfill(2)
		self.string = string
	
	def inc(self):
		""" Erhoehe den Zeitwert um 1
		"""
		if self.value == 604799: self.value = 0 # 7*24*60*60=604800
		else: self.value += 1
		self.updateString()

	
