from net.TCPLogHandler import TCPLogHandler, CustomThreadingTCPServer
import SocketServer

if __name__ == "__main__":
	"""
	these values must become config file or db based
	"""
	
	HOST, PORT = "localhost",	1982

	fakelogger = 0;
	fakeauth = 0;

	server = CustomThreadingTCPServer((HOST, PORT), TCPLogHandler, fakelogger, fakeauth)	# new injections here
	server.serve_forever()

