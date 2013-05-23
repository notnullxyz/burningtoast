from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from time import gmtime, strftime

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
        self.origin = None  # origin connection name - just for clarity
        self.state = "GETORIGIN"
        self.sendLineToLog('Spitoon construction...')


    def connectionMade(self):
        self.sendLine("Who are you? ")


    def connectionLost(self, reason):
        if self.connections.has_key(self.origin):
                    self.sendLineToLog('Connection Lost: ' + self.origin)
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
        self.sendLineToLog('Handshake: ' + origin)
        self.connections[origin] = self
        self.state = "REQUEST"


    def handle_REQUEST(self, entry):
        feedback = "%s -> %s" % (self.origin, entry)

        for origin, protocol in self.connections.iteritems():
            if protocol != self:
                protocol.sendLine(feedback);
                self.sendLineToLog('Request from %s: %s' % (self.origin, entry))
        self.pluginbase.call(entry)


        def sendLineToAll(self, line):
            """
            all logic for sending a string to everyone that is connected
            """
            pass


        def sendLineToClient(self, line):
            """
            all logic for sending a string to a specific connections
            """
            pass


        def sendLineToLog(send, line):
            """
            logic for sending a line to a logging system.
            this should be plugin-based to have a choice between console, db,
            logfile, remote log, etc...
            For now, the default is to output everything to the server console
            """
            dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print "%s : %s" % (dt, line)

