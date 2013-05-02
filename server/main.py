from protocol.Spitoon import SpitoonFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

if __name__ == "__main__":
	"""
	these values must become config file or db based
	"""

	port = 1982
        
        endpoint = TCP4ServerEndpoint(reactor, port)
        endpoint.listen(SpitoonFactory())
        reactor.run()






        

