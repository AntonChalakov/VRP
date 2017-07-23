class ClientError(Exception):

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return "CLIENT_ERROR: {0}".format(self.msg)
