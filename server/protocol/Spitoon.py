#from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class SpitoonFactory(Factory):

    def __init__(self, reactorInstance, pluginBaseInstance):
        self.connections = {}   # to map connections
        self.reactorInstance = reactorInstance
		self.pluginBaseInstance = pluginBaseInstance

    def buildProtocol(self, addr):
        return Spitoon(self.connections, self.reactorInstance, self.pluginBaseInstance)



class Spitoon(LineReceiver):
	"""
	Spitoon handles all connections and the logic thereof. 
	It takes parameters connections (as the connected client list), the reactor instance
	and the plugin base class instance so that plugins can be used (or assed along)
	"""
    def __init__ (self, connections, reactorInstance, pluginBaseInstance):
        self.connections = connections
        self.reactorInstance = reactorInstance
		self.pluginbase = pluginBaseInstance
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
		pluginCall = self.commandDeRef(command)
		if (pluginCall != None):
			# invoke it
		else:
			# ignore or process alternatives
        
	
	def commandDeRef(self, command):
		"""
		Dereference the plugin command map to find a possible call.
		If found, a reference to the function call on that plugin is returned,
		or a None if not found.
		"""
		for plugin, command in self.pluginbase.pluginCommands:
			# ideas ideas!!!! arg!
			# so if it's found, we call it?!



