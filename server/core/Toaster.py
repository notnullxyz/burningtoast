from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from time import gmtime, strftime


class ToasterFactory(Factory):

    def __init__(self, reactorInstance, pluginBaseInstance, lang):
        self.connections = {}   # to map connections
        self.reactorInstance = reactorInstance
        self.pluginBaseInstance = pluginBaseInstance
        self.lang = lang

    def buildProtocol(self, addr):
        return Toaster(
            self.connections, self.reactorInstance,
            self.pluginBaseInstance, self.lang)


class Toaster(LineReceiver):
    """
    Toaster handles all connections and the logic thereof.
    It takes parameters connections (as the connected client list),
    the reactor instance and the plugin base class instance so that
    plugins can be used (or assed along)
    """

    def __init__(self, connections, reactorInstance, pluginBaseInstance, lang):
        self.connections = connections
        self.reactorInstance = reactorInstance
        self.pluginbase = pluginBaseInstance
        self.lang = lang
        self.origin = None
        self.state = "GETORIGIN"
        self.sendLineToLog(self.tr('toasting'))

    def tr(self, stringx):
        """
        String translation wrapper. Returns an encoded byte string
        to satisfy Twisted's 'data must not not be unicode'
        """
        ss = self.lang.getTranslation(stringx)
        return ss.encode('utf8')

    def connectionMade(self):
        translatedNamePrompt = self.tr('namePrompt')
        self.sendLine(translatedNamePrompt)

    def connectionLost(self, reason):
        if self.origin in self.connections:
            self.sendLineToLog(' '.join([self.tr('conLost'), self.origin]))
            del self.connections[self.origin]
            self.transport.abortConnection()

    def lineReceived(self, line):
        if self.state == "GETORIGIN":
            self.handle_GETORIGIN(line)
        else:
            if len(line):
                requestList = line.split()
                requestCommand = requestList[0]
                if len(requestList) > 1:
                    requestParams = requestList[1:]
                else:
                    requestParams = None

                self.handle_REQUEST(requestCommand, requestParams)
            else:
                self.sendLineToClient('.')

    def handle_GETORIGIN(self, origin):
        if origin in self.connections:
            self.sendLineToClient(self.tr('usernameTaken'))
            return
        self.sendLineToClient(' '.join([self.tr('hello'), origin]))
        self.origin = origin
        self.sendLineToLog(' '.join([self.tr('handshake'), origin]))
        self.connections[origin] = self
        self.state = "REQUEST"

    def handle_REQUEST(self, reqCmd, reqParams):
        feedback = "req: %s => %s " % (self.origin, reqCmd)
        self.sendLineToAll(feedback)
        callResponse = self.pluginbase.call(reqCmd, reqParams)
        if callResponse is not None:
            #print "Response code: %s" % (callResponse['status'], )
            if callResponse['status'] == 999:
                self.terminateSelf()
            self.handle_pluginResponse(callResponse)
        else:
            pass

    def terminateSelf(self):
        self.sendLineToClient('**' + self.tr('goodbye') + '**')
        self.sendLineToAll(' '.join([self.origin, self.tr('disconnect')]))
        self.connectionLost(self.tr('userQuit'))
        # how to cleanly disconnect and cleanup a client connection?

    def sendLineToAll(self, line, skipSelf=True):
        """
        All logic for sending a string to everyone that is connected.
        Sends the line as-is.
        Loop through all connections, and sendline to each.
        This feels clunky. TODO: investigate more optimal approach.
        """
        for origin, protocol in self.connections.iteritems():
            if skipSelf is True and protocol == self:
                pass
            else:
                protocol.sendLine(line)

    def sendLineToClient(self, line):
        """
        all logic for sending a string to a specific connections
        """
        self.sendLine(line)

    def sendLineToLog(send, line):
        """
        logic for sending a line to a logging system.
        this should be plugin-based to have a choice between console, db,
        logfile, remote log, etc...
        For now, the default is to output everything to the server console
        """
        dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print "%s : %s" % (dt, line)

    def handle_pluginResponse(self, responseDict):
        """
        Rethink:
        Simple - plugins do work, and responds with results. all we ever get
        back, is a result, nothing weird.
        """
        print responseDict
        self.sendLineToClient(responseDict['data'])

