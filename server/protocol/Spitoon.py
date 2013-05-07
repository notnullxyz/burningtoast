#from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class SpitoonFactory(Factory):

    def __init__(self, reactorInstance):
        self.connections = {}   # to map connections
        self.reactorInstance = reactorInstance

    def buildProtocol(self, addr):
        return Spitoon(self.connections, self.reactorInstance)



class Spitoon(LineReceiver):
    
    def __init__ (self, connections, reactorInstance):
        self.connections = connections
        self.reactorInstance = reactorInstance
        print "WE HAVE REACTOR?"
        print self.reactorInstance
        self.origin = None  # origin connection name - just for clarity
        self.state = "GETORIGIN"

    def connectionMade(self):
        self.sendLine("Who are you? ")

    def connectionLost(self, reason):
        if self.connections.has_key(self.origin):
            print "%s left" % (self.origin,)
            del self.connections[self.origin]

    def lineReceived(self, line):
        if self.state == "GETORIGIN":
            self.handle_GETORIGIN(line)
        else:
            self.handle_REQUEST(line)

    def handle_GETORIGIN(self, origin):
        if self.connections.has_key(origin):
            self.sendLine("Someone with that name signed in already O_o ...")
            return
        self.sendLine("Hello %s" % (origin,))
        self.origin = origin
        print "%s joined" % (origin,)
        self.connections[origin] = self
        self.state = "REQUEST"

    def handle_REQUEST(self, entry):
        entry = "%s -> %s" % (self.origin, entry)
        
        for origin, protocol in self.connections.iteritems():
            if protocol != self:
                protocol.sendLine(entry);

    def handle_COMMAND(self, command):
        """
        This is going to be ugly, will dict it later...
        """
        #if command == 'quit' or command == 'bye':
        



