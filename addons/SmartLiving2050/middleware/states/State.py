from middleware import message
import json
import logging

class State():
	def __init__(self, sess):
		self.log    = logging.getLogger(__name__)
		self.sess = sess
		raise Exception("Tried to instantiate basic State class.")

	def role(self):
		raise Exception("Basic State class has no role.")

	def error(self):
		self.sess.send("CLIENT_ERROR")
		return self

	def get_time(self):
		self.sess.send(message.event_set_time(self.sess.get_time()))
		return self

	def login(self, role):
		self.log.error("Bad message 'login' in state {0}".format(self))
		return self.error()

	def sessions(self):
		self.log.error("Bad message 'sessions' in state {0}".format(self))
		return self.error()

	def change_role(self, device_id, role):
		self.log.error("Bad message 'change_role' in state {0}".format(self))
		return self.error()

	def kick(self, device_id):
		self.log.error("Bad message 'kick' in state {0}".format(self))
		return self.error()

	def list_devices(self):
		self.log.error("Bad message 'list_dev' in state {0}".format(self))
		return self.error()

	def broken_device(self, item_id):
		self.log.error("Bad message 'broken' in state {0}".format(self))
		return self.error()

	def repaired_device(self, item_id):
		self.log.error("Bad message 'repaired' in state {0}".format(self))
		return self.error()
