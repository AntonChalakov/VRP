from .State import State
from middleware import message

""" FIXME: Remove messages / state transistions that are not allowed
     -- awaidler, 2017-01-23 """

class TechnicianState(State):
	def __init__(self, sess):
		self.sess = sess
		pass

	def role(self):
		return message.ROLES.TECHNICIAN

	def set_time(self, day, hour, minute):
		self.sess.set_time(day, hour, minute)
		return self

	def sessions(self):
		for k, v in self.sess.connections().items():
			self.sess.send(message.event_logged_in(v.getId(), v.getRole()))
		return self

	def change_role(self, device_id, role):
		self.sess.change_role(device_id, role)
		return self

	def kick(self, device_id):
		self.sess.kick(device_id)
		return self

	def list_devices(self):
		for dev in self.sess.devices():
			self.sess.send(message.event_device_added(dev))
		return self

	def broken_device(self, item_id):
		self.sess.broken_device(item_id)
		return self

	def repaired_device(self, item_id):
		self.sess.repaired_device(item_id)
		return self
