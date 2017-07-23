class MockWebSocket():
	def __init__(self, key, text, reply_sink):
		self.key = key
		self.msg = text
		self.snk = reply_sink

	def getKey(self):
		return self.key

	def getMessage(self):
		return self.msg

	def answer(self, key, msg):
		self.snk.append([key, msg])
