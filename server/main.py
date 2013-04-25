from net import TCPLogHandler
import SocketServer

if __name__ == "__main__":
	"""
	these values must become config file or db based
	"""
	
	HOST, PORT = "localhost",	1982
	server = ThreadingTCPServer((HOST, PORT), TCPLogHandler)
	server = ThreadingTCPServer((HOST, PORT), TCPLogHandler, XXXXXX, YYYYYY)	# new injections here
	server.serve_forever()

