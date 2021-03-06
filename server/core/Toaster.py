##
#    Copyright 2013 Marlon van der Linde
#
#    This file is part of BurningToast
#
#    BurningToast is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BurningToast is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BurningToast.  If not, see <http://www.gnu.org/licenses/>.
##

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from time import gmtime, strftime
import json
from multiprocessing import Process, Queue

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
        self.sendLineToLog('Toaster Construction')
        self.jobs = []

    def tr(self, stringx):
        """
        String translation wrapper. Returns an encoded byte string
        to satisfy Twisted's 'data must not not be unicode'
        """
        ss = self.lang.getTranslation(stringx)
        return ss.encode('utf8')    # todo use config from toastCore

    def connectionMade(self):
        translatedNamePrompt = self.tr('namePrompt')
        self.sendLine(translatedNamePrompt)

    def connectionLost(self, reason):
        if self.origin in self.connections:
            self.sendLineToLog('Connection Lost ' + self.origin)
            del self.connections[self.origin]
            self.transport.abortConnection()
            self.publishPublicData('logout', self.origin)

    def lineReceived(self, line):
        if self.state == "GETORIGIN":
            self.handle_GETORIGIN(line)
        else:
            if len(line):
                requestList = line.split()
                requestCommand = requestList[0]
                # check and isolate command+params
                if len(requestList) > 1:
                    requestParams = requestList[1:]
                else:
                    requestParams = None

                self.handle_REQUEST(requestCommand, requestParams)
            else:
                self.sendLineToClient('-?-')

    def handle_GETORIGIN(self, origin):
        if origin in self.connections:
            self.sendLineToClient(self.tr('usernameTaken'))
            return
        self.sendLineToClient(' '.join([self.tr('hello'), origin]))
        self.origin = origin
        self.publishPublicData('login', origin)
        self.sendLineToLog('Handshake ' + origin)
        self.connections[origin] = self
        self.state = "REQUEST"

    def handle_REQUEST(self, reqCmd, reqParams):
        self.que = Queue()

        feedback = "%s requested %s" % (self.origin, reqCmd)
        # todo - how to deal with privacy/publicity ?
        self.sendLineToAll(feedback)

        p = Process(target = self.pluginbase.call, args = (self.que, reqCmd, reqParams))
        p.start()
        callResponse = self.que.get()
        p.join()

        if callResponse is not None:
            # special status handlers
            if callResponse['status'] == 999:        # 999 = quit code
                self.terminateSelf()
            elif callResponse['status'] == 998:      # 998 = chat code
                self.sendChatMessage(callResponse['data'])
            self.handle_pluginResponse(callResponse)
        else:
            pass

    def sendChatMessage(self, chatData):
        """
        Handle chat messages to other users with special status code 998
        """
        destinationConnection = chatData['destClient']
        messageLine = self.pluginbase.config.get('general', 'chatPrefix') + \
            self.origin + ": " + chatData['message']
        if destinationConnection.lower() == 'announce':
            self.sendLineToAll(messageLine, False)
        else:
            if destinationConnection in self.connections:
                self.sendLineToTarget(messageLine, chatData['destClient'])
            else:
                # TODO: handle invalid chat requests
                pass

    def terminateSelf(self):
        """
        Handle disconnecting on the users whim with the special status 999
        """
        self.sendLineToClient('**' + self.tr('goodbye') + '**')
        self.sendLineToAll(' '.join([self.origin, self.tr('disconnect')]))
        self.connectionLost(self.tr('userQuit'))
        # TODO! how to cleanly disconnect and cleanup a client connection?

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

    def sendLineToTarget(self, line, target):
        """
        send a line of text to a specified connection.
        """
        if target in self.connections:
            self.connections[target].sendLine(line)

    def sendLineToClient(self, line):
        """
        all logic for sending a string to a self, current connection
        """
        if line is None:
            line = '<sendLineToClient:line data None - not normal>'
        self.sendLine(line)

    def sendLineToLog(self, line):
        """
        logic for sending a line to a logging system.
        this should be plugin-based to have a choice between console, db,
        logfile, remote log, etc...
        For now, the default is to output everything to the server console
        """
        dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print "%s | %s" % (dt, line)

    def handle_pluginResponse(self, responseDict, asJson=True): # TODO use toastCore config
        """
        Rethink:
        Simple - most plugins do work, and responds with results. all we ever get
        back, is a result, nothing weird.
        """

        respTxt = 'pluginResponse Unhandled 000'
        if responseDict['status'] is -1:
            respTxt = self.tr('noSuchCommand')
        else:
            if responseDict['data'] is None:
                respTxt = ''
            else:
                respTxt = responseDict['data']

        if asJson is True:
            try:    
                exhaust = json.dumps(responseDict)
            except UnicodeDecodeError:
                exhaust = json.dumps({})
        else:
            exhaust = str(responseDict['status']) + ' ' + respTxt

        self.sendLineToClient(exhaust)
        logLine = "Plugin response code %s sent to %s" % (responseDict['status'], self.origin)
        self.sendLineToLog(logLine)

    def publishPublicData(self, action, client):
        """
        Publishes data in provided, into the plugin base (MainSlice)
        provided to this constructor. This can/should be called on any change
        that affects this data, for instance 'logged in users'
        """
        por = self.__class__.__name__
        self.pluginbase.updateExternalDataMap(str(action), str(client), por)

