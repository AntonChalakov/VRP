from .Connection import Connection
from .Middleware import Middleware
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

class PolyVrMiddlewareAdapter():

	def __init__(self, hub):
		self.log = logging.getLogger(__name__)
		self.mw  = Middleware(hub)

	def recv(self, sck):
		cnxn = self.mw.connections().get(sck.getKey())
		if cnxn is None:
			cnxn = self.mw.open(PolyVrWebSocketConnection(sck))

		assert cnxn is not None
		return self.mw.recv(cnxn, sck.getMessage())
