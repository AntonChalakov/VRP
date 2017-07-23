from .State import State
from middleware import message

class SpectatorState(State):
	def __init__(self, sess):
		self.sess = sess
		pass

	def role(self):
		return message.ROLES.TECHNICIAN
