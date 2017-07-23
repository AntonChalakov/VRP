import VR

class TimedEvent:
	""" Definiert ein zeitlich gesteuertes Event fuer die VR-Umgebung.

	Ein TimedEvent ist ein Wrapper fuer eine festgelegte Funktion, die, mit zeitlicher Verzoegerung, ein- oder mehrfach
	ausgefuehrt werden kann.
	TimedEvent-Objekte muessen in regelmaessigen Intervallen aufgerufen werden, um sich
	zu aktualisieren und bei Bedarf auszuloesen.

	@attr lifetime: Gueltigkeitsdauer des Events in Sekunden. Nach Ablauf dieser kann das Event geloescht werden (float)
	@attr event: Funktion/Methode, die zum Aktivierungszeitpunkt aufgerufen wird. (function)
	@attr executionTimer: Ausfuehrungstimer in Sekunden. Beschreibt die Dauer zwischen Event-Aktivierungen. Wenn dieser nicht zugewiesen (None)
	ist, wird das Event einmalig, zu Ende seiner Gueltigkeitsdauer aufgerufen. ACHTUNG: Wenn executionTimer > lifetime, wird das Event 
	nicht aufgerufen! (flroat)
	@attr timer: aktueller Stand des Timers nach der letzten Aktualisierung
	"""
	def __init__(self, lifetime, event, executionTimer = None):
		""" Erstellt eine Instanz von TimedEvent.

		@param lifetime: Gueltigkeitsdauer des Events in Sekunden (float)
		@param event: auszufuehrende Funktion (function)
		@executionTimer: Ausfuehrungstimer, der das Zeitintervall zwischen Aktivierungen bestimmt (float) (default = None)
		"""
		self.lifetime = lifetime
		self.event = event
		self.executionTimer = executionTimer
		self.timer = executionTimer
		
	def update(self, elapsedTime):
		""" Aktualisiere den Zustand des Events.

		Verrechne die vergangene Zeit mit den Timern des Events. Ist die Gueltigkeitsdauer bereits abgelaufen, findet keine weitere Bearbeitung statt.
		Ist der Ausfuehrungstimer nach der Aktualisierung abgelaufen, oder die Gueltigkeitsdauer bei nicht gesetztem Timer, wird das definierte Event
		ausgefuehrt. 

		@param elapsedTime: vergangene Zeit in Sekunden, seit der letzten Aktualisierung (float)
		"""
		if self.lifetime <= 0:
			return
		
		self.lifetime -= elapsedTime
		
		if self.executionTimer is not None:
			self.timer -= elapsedTime
			if self.timer <= 0.0:
				self.event()
				self.timer = self.executionTimer
		elif self.lifetime <= 0:
			self.event()