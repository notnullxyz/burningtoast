
if __name__ == "__main__":
	"""
	these values must become config file or db based
	"""
    HOST, PORT = "localhost", 1982
    server = SocketServer.TCPServer((HOST, PORT), TCPLogHandler)
    server.serve_forever()

