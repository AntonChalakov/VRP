#!/usr/bin/env python

from middleware.Connection import Connection
from middleware.Middleware import Middleware
from middleware.tests.MockHub import MockHub
from queue import Queue
import asyncio
import logging
import websockets

class WebsocketConnection(Connection):

	ctr = 0

	def __init__(self):
		self.log    = logging.getLogger(__name__)
		self.q  = Queue() # Thread-safe!

		# Race condition!
		self.id = WebsocketConnection.ctr
		WebsocketConnection.ctr += 1

	def __str__(self):
		return "WebsocketConnection"

	def getId(self):
		return self.id

	def send(self, msg):
		print("Appending to queue: '{0}'.".format(msg))
		self.q.put(msg)

	async def getBuffered(self):
		print("Awaiting response...")

		""" If we were to simply use q.get(),
		    the whole application would block
		    somehow.
		      -- awaidler, 2016-12-17
		"""

		while self.q.empty():
			print("Still waiting...")
			await asyncio.sleep(1)

		return self.q.get()

class LocalMiddlewareServer():

	def __init__(self):
		self.log = logging.getLogger(__name__)
		self.mw  = Middleware(MockHub())

	def run(self):
		start_server = websockets.serve(self.handler, 'localhost', 5500)

		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()

	async def handler(self, websocket, path):
		# Borrowed from http://websockets.readthedocs.io/en/stable/intro.html#both
		#   -- awaidler, 2016-12-17
		wsck = WebsocketConnection()
		cnxn = self.mw.open(wsck)
		while True:
			listener_task = asyncio.ensure_future(websocket.recv())
			producer_task = asyncio.ensure_future(self.producer(wsck))
			done, pending = await asyncio.wait(
				[listener_task, producer_task],
				return_when=asyncio.FIRST_COMPLETED)
			
			if listener_task in done:
				message = listener_task.result()
				await self.consumer(cnxn, message)
			else:
				listener_task.cancel()
			
			if producer_task in done:
				message = producer_task.result()
				await websocket.send(message)
			else:
				producer_task.cancel()

	async def producer(self, wsck):
		return await wsck.getBuffered()

	async def consumer(self, cnxn, message):
		return self.mw.recv(cnxn, message)

def main():
	srv = LocalMiddlewareServer()
	srv.run()

if __name__ == "__main__":
	main()

