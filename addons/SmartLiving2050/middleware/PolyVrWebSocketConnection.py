from Connection import Connection
import logging

class PolyVrWebSocketConnection(Connection):

	def __init__(self, socket):
		self.log    = logging.getLogger(__name__)
		self.borg   = socket
		self.key    = socket.getKey()

	def __str__(self):
		return "PolyVrWebSocketConnection#{0}".format(self.key)

	def getId(self):
		return self.key

	def send(self, msg):
		self.borg.answer(self.key, msg)
