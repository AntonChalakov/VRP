from .ClientError import ClientError
from .Connection import Connection
from .Parser import Parser
from .Session import Session
from .StateFactory import STATE_FACTORY
from .tests.MockHub import MockHub # TODO: See below
from middleware import message
import logging
import json

class Middleware():

	def __init__(self, hub):
		self.log    = logging.getLogger(__name__)
		self.cnxns  = dict()
		self.parser = Parser()
		self.hub    = hub

	def open(self, cnxn):
		key = cnxn.getId()
		if key in self.cnxns:
			raise RuntimeError("Connection with key '{0}' does already exist.".format(key))

		sess = Session(self, cnxn)
		cnxn.session(sess)

		self.cnxns[key] = cnxn
		return cnxn

	def recv(self, cnxn, msg):
		self.log.error("'{0}'".format(self.cnxns))

		assert cnxn is not None
		assert msg is not None

		try:
			cnxn.recv(self.parser.parse(msg))
		except ClientError as e:
			self.log.error(e)
			cnxn.send('"CLIENT_ERROR"')
		except:
			cnxn.send('"SERVER_ERROR"')
			raise

	def broadcast(self, obj):
		msg = json.dumps(obj)
		for k, v in self.connections().items():
			v.send(msg)

	def get_time(self):
		return self.hub.get_time()

	def set_time(self, d, h, m):
		time = self.hub.set_time(d, h, m)
		self.broadcast(message.event_set_time(time))

	def connections(self):
		return self.cnxns


	def change_role(self, device_id, role):
		sess = self.cnxns[device_id].session()

		state = STATE_FACTORY[role](sess)
		sess.setState(state)

		self.broadcast(message.event_role_changed(device_id, role))

	def kick(self, device_id):
		try:
			# TODO: HACK: broadcast response before action
			# so the guy gets notified that he is about to be kicked
			#    -- awaidler, 2016-12-22
			self.broadcast(message.event_kicked(device_id))

			cnxn = self.cnxns.pop(device_id)
			cnxn.terminate()
		except KeyError:
			self.log.error("No key '{0}' in '{1}'.".format(device_id, self.cnxns))

	def devices(self):
		return self.hub.devices()

	def device(self, dev_id):
		dev = list(filter(lambda x: x.id() == dev_id, self.devices()))

		if len(dev) == 0: raise RuntimeError("No such device.")
		if len(dev) > 1:  raise RuntimeError("Internal error: Duplicate device ID")

		return dev[0]

	def broken_device(self, item_id):
		dev = self.device(item_id)
		dev.set_broken()
		# TODO: Check if Hub is MockHub. Broadcast only then
		#    -- lkaiser, 2017-02-05
		# TODO: This is actually a dirty HACK.
		#       MockHub/Device should call pvr_broken_device
		#        -- awaidler, 2017-02-07
		if isinstance(self.hub, MockHub):
			self.broadcast(message.event_device_broken(dev))

	def repaired_device(self, item_id):
		dev = self.device(item_id)
		dev.set_repaired()
		# TODO: Check if Hub is MockHub. Broadcast only then
		#    -- lkaiser, 2017-02-05
		# TODO: This is actually a dirty HACK.
		#       MockHub/Device should call pvr_repaired_device
		#        -- awaidler, 2017-02-07
		if isinstance(self.hub, MockHub):
			self.broadcast(message.event_device_repaired(dev))

	def pvr_broken_device(self, dev):
		self.broadcast(message.event_device_broken(dev))

	def pvr_repaired_device(self, dev):
		self.broadcast(message.event_device_repaired(dev))
