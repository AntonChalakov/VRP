from .states.ConnectedState import ConnectedState
from middleware.StateFactory import STATE_FACTORY
from middleware import message
from . import Device
import logging
import json

class Session():

	def __init__(self, middleware, connection):
		self.log   = logging.getLogger(__name__)
		self.mw    = middleware
		self.cnxn  = connection
		self.state = ConnectedState(self)

	def __str__(self):
		return "Session::{0}".format(self.cnxn)

	def getId(self):
		return self.cnxn.getId()

	def getRole(self):
		return self.state.role()

	def setState(self, state):
		self.state = state

	def getState(self):
		return self.state

	def recv(self, msg):
		self.log.debug("{0}: {1} received".format(self, msg))

		prev_state = self.state
		self.state = msg(self.state)

		self.log.debug("{0}: {1} -> {2}".format(self, prev_state, self.state))

	def send(self, obj):
		msg = json.dumps(obj)
		self.cnxn.send(msg)
		self.log.debug("{0}: {1} sent".format(self, msg))

	def get_time(self):
		return self.mw.get_time()

	def set_time(self, d, h, m):
		return self.mw.set_time(d, h, m)

	def login(self, role):
		# TODO: For now, all logins are allowed.  -- awaidler, 2016-12-10

		new_state = STATE_FACTORY[role](self)

		# FIXME: Getting state this way is a hack.
		m = message.event_logged_in(self.getId(), new_state.role())
		self.mw.broadcast(m)

		return new_state

	def connections(self):
		return self.mw.connections()

	def change_role(self, device_id, role):
		self.mw.change_role(device_id, role)

	def kick(self, device_id):
		self.mw.kick(device_id)

	def devices(self):
		return self.mw.devices()

	def broken_device(self, item_id):
		self.mw.broken_device(item_id)

	def repaired_device(self, item_id):
		self.mw.repaired_device(item_id)
