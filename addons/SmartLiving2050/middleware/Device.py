class Device(object):
	def __init__(self, item_id, item_type, is_ok, room_name):
		self._id   = item_id
		self._type = item_type
		self._ok   = is_ok
		self._room = room_name

	def id(self):
		return self._id

	def type(self):
		return self._type

	def item_type(self):
		return self._item_type

	def is_ok(self):
		return self._ok

	def room(self):
		return self._room

	def set_broken(self):
		if not self._ok:
			print("Item {0} is already broken.".format(self._id))
		else:
			print("Item {0} broke down.".format(self._id))

		self._ok = False

	def set_repaired(self):
		if self._ok:
			print("Item {0} is already repaired.".format(self._id))
		else:
			print("Item {0} has been repaired.".format(self._id))

		self._ok = True

	def get_repairAppointment(self):
		return "0"


class Light(Device):
	def __init__(self, item_id, is_ok, room_name):
		super(Light, self).__init__(
			item_id, "LIGHT", is_ok, room_name)

class Radiator(Device):
	def __init__(self, item_id, is_ok, room_name):
		super(Radiator, self).__init__(
			item_id, "RADIATOR", is_ok, room_name)
