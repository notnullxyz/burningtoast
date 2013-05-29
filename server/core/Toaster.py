from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from time import gmtime, strftime

class ToasterFactory(Factory):

    def __init__(self, reactorInstance, pluginBaseInstance):
        self.connections = {}   # to map connections
        self.reactorInstance = reactorInstance
        self.pluginBaseInstance = pluginBaseInstance

    def buildProtocol(self, addr):
        return Toaster(self.connections, self.reactorInstance, self.pluginBaseInstance)



class Toaster(LineReceiver):
    """
    Toaster handles all connections and the logic thereof. 
    It takes parameters connections (as the connected client list), the reactor instance
    and the plugin base class instance so that plugins can be used (or assed along)
    """

    def __init__ (self, connections, reactorInstance, pluginBaseInstance):
        self.connections = connections
        self.reactorInstance = reactorInstance
        self.pluginbase = pluginBaseInstance
        self.origin = None  # origin connection name - just for clarity
        self.state = "GETORIGIN"
        self.sendLineToLog('Toaster construction...')


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
        feedback = "req: %s => %s " % (self.origin, entry)
        self.sendLineToAll(feedback)
        callResponse = self.pluginbase.call(entry)
        if callResponse != None:
            self.handle_pluginResponse(callResponse)
        else:
            # there will be something to do when a plugin call is silent.log it?
            pass;


    def sendLineToAll(self, line, skipSelf=True):
        """
        All logic for sending a string to everyone that is connected.
        Sends the line as-is.
        Loop through all connections, and sendline to each. 
        This feels clunky. TODO: investigate more optimal approach.
        """
        for origin, protocol in self.connections.iteritems():
            if skipSelf == True and protocol == self:
                pass
            else:
                protocol.sendLine(line)


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

    def handle_pluginResponse(self, responseValue):
        """
        Handling of anything that a call to a plugin might return.
        This is hard, because it could be anything, that has to go anywhere.
        Make it available in some kind of callback or store?
        """"
        self.sendLineToClient(responseValue) # send to client, until we know!

