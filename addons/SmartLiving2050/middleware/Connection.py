import logging

class Connection():

	def __init__(self, socket):
		self.log    = logging.getLogger(__name__)
		self.sess   = None

	def getId(self):
		pass

	def getRole(self):
		return self.sess.getRole()

	def getState(self):
		return self.sess.getState()

	def session(self, session=None):
		if session != None:
			self.sess = session
		return self.sess

	def recv(self, msg):
		assert msg is not None

		if self.sess is None:
			raise RuntimeError("{0} received a message prior to setting up a session.".format(self))

		self.sess.recv(msg)

	def send(self, msg):
		pass

	def terminate(self):
		pass # FIXME
