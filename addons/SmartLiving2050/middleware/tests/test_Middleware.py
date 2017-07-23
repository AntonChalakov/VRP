from middleware.PolyVrMiddlewareAdapter import PolyVrMiddlewareAdapter
from .MockWebSocket import MockWebSocket
from .MockHub import MockHub
import unittest
import logging
import json

logging.basicConfig(level=logging.DEBUG)

class TestMiddleware(unittest.TestCase):

	def setUp(self):
		self.sut = PolyVrMiddlewareAdapter(MockHub())
		self.exp = []
		self.q   = []

	def tearDown(self):
		self.verify()

	def send(self, key, message):
		assert key is not None
		assert message is not None

		msg = message if type(message) is str else json.dumps(message)
		sck = MockWebSocket(key, msg, self.q)

		self.sut.recv(sck)

	def recv(self, key, *responses):
		assert key is not None
		assert responses is not None

		for r in responses:
			obj = r if type(r) is str else json.dumps(r)
			self.exp.append([key, obj])

	def send_recv(self, key, message, *responses):
		self.send(key, message)
		for r in responses: self.recv(key, r)

	def verify(self):
		self.assertEqual(self.exp, self.q)

	def test_login_invalid(self):
		m = { 'code': "LOGIN", 'args': { 'role': "BANANAS" } }
		self.send_recv(666, m, '"CLIENT_ERROR"')

	def test_login_op1(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

	def test_login_op2(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

	def test_relogin(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)
		self.send_recv(666, m, '"CLIENT_ERROR"')

	def test_get_time(self):
		m = { 'code': "GET_TIME", 'args': { } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "SET_TIME", 'args': { 'day': 0, 'hour': 12, 'minute': 0}}}}
		self.send_recv(666, m, r)

	def test_set_time(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "SET_TIME", 'args': { 'day': 3, 'hour': 13, 'minute': 37} }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)

	def test_set_time_gets_broadcasted(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "SET_TIME", 'args': { 'day': 3, 'hour': 13, 'minute': 37 }}
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)

	def test_op_get_sess1(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "GET_LOGINS", 'args': { } }
		self.send_recv(666, m, r)

	def test_op_get_sess2(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "GET_LOGINS", 'args': { } }
		self.send_recv(666, m, r1, r2)

		m = { 'code': "GET_LOGINS", 'args': { } }
		self.send_recv(123, m, r1, r2)

	def test_op_change_role(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "CHANGE_ROLE", 'args': { 'id': 123, 'role': "TENANT"}}
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)

	def test_op_change_role_actually_changes(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "CHANGE_ROLE", 'args': { 'id': 123, 'role': "TENANT"}}
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)

		m = { 'code': "GET_LOGINS", 'args': { } }
		r3 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "TENANT" }}}}
		self.send_recv(666, m, r1, r3)

	def test_op_kick(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "KICK", 'args': { 'id': 123 }}
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)


	def test_op_kick_actually_changes_sessions(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "KICK", 'args': { 'id': 123 }}
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)

		m = { 'code': "GET_LOGINS", 'args': { } }
		self.send_recv(666, m, r1)

	def test_op_list_devices(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m  = { 'code': "GET_DEVICES", 'args': { } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT1",    'type': "LIGHT",    'state': "OK", 'room': "Living Room" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT2",    'type': "LIGHT",    'state': "FAULT", 'room': "Kitchen" }}}}
		r3 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR4", 'type': "RADIATOR", 'state': "FAULT", 'room': "Bathroom" }}}}
		r4 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR9", 'type': "RADIATOR", 'state': "OK", 'room': "Hallway" }}}}
		self.send_recv(666, m, r1, r2, r3, r4)

	def test_op_broken_light(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "BREAK_DEVICE", 'args': { 'id': "LIGHT1" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)

	def test_op_broken_light_actually_changes_state(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "BREAK_DEVICE", 'args': { 'id': "LIGHT1" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)

		m  = { 'code': "GET_DEVICES", 'args': { } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT1",    'type': "LIGHT",    'state': "FAULT", 'room': "Living Room" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT2",    'type': "LIGHT",    'state': "FAULT", 'room': "Kitchen" }}}}
		r3 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR4", 'type': "RADIATOR", 'state': "FAULT", 'room': "Bathroom" }}}}
		r4 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR9", 'type': "RADIATOR", 'state': "OK",    'room': "Hallway" }}}}
		self.send_recv(666, m, r1, r2, r3, r4)

	def test_op_broken_light_gets_broadcasted(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "BREAK_DEVICE", 'args': { 'id': "LIGHT1" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)

	def test_op_repaired_light(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "REPAIR_DEVICE", 'args': { 'id': "LIGHT2" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)

	def test_op_repaired_light_actually_changes_state(self):
		m = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r)

		m = { 'code': "REPAIR_DEVICE", 'args': { 'id': "LIGHT2" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)

		m  = { 'code': "GET_DEVICES", 'args': { } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT1",    'type': "LIGHT",    'state': "OK",    'room': "Living Room" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "LIGHT2",    'type': "LIGHT",    'state': "OK",    'room': "Kitchen" }}}}
		r3 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR4", 'type': "RADIATOR", 'state': "FAULT", 'room': "Bathroom" }}}}
		r4 = { 'code': "EVENT", 'args': { 'cause': { 'code': "ADD_DEVICE", 'args': { 'id': "RADIATOR9", 'type': "RADIATOR", 'state': "OK",    'room': "Hallway" }}}}
		self.send_recv(666, m, r1, r2, r3, r4)

	def test_op_repaired_light_gets_broadcasted(self):
		m  = { 'code': "LOGIN", 'args': { 'role': "OPERATOR" } }
		r1 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 666, 'role': "OPERATOR" }}}}
		r2 = { 'code': "EVENT", 'args': { 'cause': { 'code': "LOGIN", 'args': { 'id': 123, 'role': "OPERATOR" }}}}
		self.send_recv(666, m, r1, r2)
		self.send_recv(123, m, r2)

		m = { 'code': "REPAIR_DEVICE", 'args': { 'id': "LIGHT2" } }
		r = { 'code': "EVENT", 'args': { 'cause': m }}
		self.send_recv(666, m, r)
		self.recv(123, r)
