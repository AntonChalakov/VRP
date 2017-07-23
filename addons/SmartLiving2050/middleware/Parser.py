import re
import json
from .message import MESSAGE_TYPES, ROLES, DEVICE_TYPES
from .ClientError import ClientError
import logging

class Parser():

	def __init__(self):
		self.log = logging.getLogger(__name__)

		self.MESSAGE_FACTORY = {
			MESSAGE_TYPES.GET_TIME:      self.msg_get_time,
			MESSAGE_TYPES.SET_TIME:      self.msg_time,

			MESSAGE_TYPES.GET_LOGINS:    self.msg_sessions,
			MESSAGE_TYPES.LOGIN:         self.msg_login,
			MESSAGE_TYPES.CHANGE_ROLE:   self.msg_change_role,
			MESSAGE_TYPES.KICK:          self.msg_kick,

			MESSAGE_TYPES.GET_DEVICES:  self.msg_list_devices,
			MESSAGE_TYPES.BREAK_DEVICE:        self.msg_broken,
			MESSAGE_TYPES.REPAIR_DEVICE:      self.msg_repaired,
		}

	def parse(self, text):
		try:
			msg  = json.loads(text)
			code = msg['code']

			if (code not in MESSAGE_TYPES.fromString):
				raise ClientError("No such message type.")

			opcode = MESSAGE_TYPES.fromString[code];
			return self.MESSAGE_FACTORY[opcode](msg)
		except Exception as e:
			m = "Bad message '{0}' triggered exception '{1}'".format(text, repr(e))
			raise ClientError(m)

	def msg_get_time(self, msg):
		return lambda state: state.get_time()

	def msg_time(self, msg):
		d = msg['args']['day']
		h = msg['args']['hour']
		m = msg['args']['minute']
		return lambda state: state.set_time(d, h, m)

	def msg_login(self, msg):
		role = msg['args']['role'];

		if (role not in ROLES.fromString):
			raise ClientError("No such role.")

		return lambda state: state.login(ROLES.fromString[role])

	def msg_sessions(self, msg):
		return lambda state: state.sessions()

	def msg_change_role(self, msg):
		i = msg['args']['id']
		r = msg['args']['role']

		if (r not in ROLES.fromString):
			raise ClientError("No such ROLE.")

		return lambda state: state.change_role(i, ROLES.fromString[r])

	def msg_kick(self, msg):
		return lambda state: state.kick(msg['args']['id'])

	def msg_list_devices(self, msg):
		return lambda state: state.list_devices()

	def msg_broken(self, msg):
		return lambda state: state.broken_device(msg['args']["id"])

	def msg_repaired(self, msg):
		return lambda state: state.repaired_device(msg['args']["id"])
