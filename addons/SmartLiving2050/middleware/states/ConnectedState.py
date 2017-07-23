from .State import State
from middleware import message

class ConnectedState(State):

	def __init__(self, sess):
		self.sess = sess
		pass

	def role(self):
		return message.ROLES.SPECTATOR # FIXME

	def login(self, role):
		return self.sess.login(role)
