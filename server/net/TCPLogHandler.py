import SocketServer

class CustomThreadingTCPServer(SocketServer.ThreadingTCPServer):
	"""
	Extending ThreadingTCPServer to gain the ability of taking arguments (by override of constructor). 
	I couldn't think of anything else yet.
	"""
	def __init__(self, server_address, requestHandler, logger, auth):
		print "---CustomThreadingTCPServer init"
		SocketServer.ThreadingTCPServer.__init__(self, server_address, requestHandler)
		self.logger = logger
		self.auth = auth


class TCPLogHandler(SocketServer.BaseRequestHandler):
	""" 
	Server Request handler.
	Instantiation per connection. handle() must be overridden.
	TODO: ThreadingMixIn later
	"""

	def __init__(self):
		"""
		constructor with dependency injection for the logger class
		"""
		print "--- TCPLogHandler init"
		self.logger = self.server.logger
		self.auth = self.server.auth


	def setup(self):
		"""
		override: called before handle() for init purposes
		"""
		print self.data


	def handle(self):
		"""
		override: main handler of the incoming request
		"""
		self.data = self.request.recv(1024).strip()
		# self.client_address and self.server is available here - *boop*		
		#respond(self.request.sendall(self.data or whatever)

	
	def respond(self, response):
		"""
		do the response to client stuff here. will self.request be available here?
		"""
		pass


	def finish(self):
		"""
		override: called after handle() to do cleanups
		"""
		pass


	def writeLog(self):
		"""
		if the request is auth'd, and a valid log call, this is where it should go
		Uses the self.logger dependency
		"""
		pass


	def authOrigin(self):
		"""
		all incoming requests chirp in here, validate auth, confirm and return or handle otherwise.
		Uses the self.auth dependency
		"""
		pass


