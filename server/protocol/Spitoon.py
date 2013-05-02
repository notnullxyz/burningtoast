from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

class SpitoonFactory(Factory):
    def buildProtocol(self, addr):
        return Spitoon()

class Spitoon(Protocol):
    
    def __init__ (self, factory):
        self.factory = factory

    def connectionMade(self):
        print "new connection in"
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write("you're spitting as number %d" % (self.factory.numProtocols, ))

    def connectionLost(self, reason):
        print "connection dropped"
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)



