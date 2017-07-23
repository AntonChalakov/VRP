from middleware.Device import *

class MockHub:
	def __init__(self):
		self._time = {
			'day': 0,
			'hour': 12,
			'minute': 0,
		}

		self._devices = [
			Light("LIGHT1", True, "Living Room"),
			Light("LIGHT2", False, "Kitchen"),
			Radiator("RADIATOR4", False, "Bathroom"),
			Radiator("RADIATOR9", True,  "Hallway"),
		]

	def get_time(self):
		return self._time

	def set_time(self, d, h, m):
		self._time['day'] = d
		self._time['hour'] = h
		self._time['minute'] = m

		return self._time

	def devices(self):
		return self._devices
