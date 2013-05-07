from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class SpitoonFactory(Factory):

    def __init__(self):
        self.connections = {}   # to map connections

    def buildProtocol(self, addr):
        return Spitoon(self.connections)



class Spitoon(LineReceiver):
    
    def __init__ (self, connections):
        self.connections = connections
        self.origin = None  # origin connection name - just for clarity
        self.state = "GETORIGIN"

    def connectionMade(self):
        self.sendLine("Who are you? ")

    def connectionLost(self, reason):
        if self.connections.has_key(self.origin):
            del self.connections[self.origin]

    def lineReceived(self, line):
        if self.state == "GETORIGIN":
            self.handle_GETORIGIN(line)
        else:
            self.handle_PUSHENTRY(line)

    def handle_GETORIGIN(self, origin):
        if self.connections.has_key(origin):
            self.sendLine("Someone with that name signed in already O_o ...")
            return
        self.sendLine("OK : %s" % (origin,))
        self.origin = origin
        self.connections[origin] = self
        self.state = "PUSHENTRY"

    def handle_PUSHENTRY(self, entry):
        entry = "%s -> %s" % (self.origin, entry)
        for origin, protocol in self.connections.iteritems():
            if protocol != self:
                protocol.sendLine(entry);


