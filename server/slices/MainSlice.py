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

from datetime import datetime


class MainSlice(object):

    plugins = []
    pluginCommands = {}
    externalDataMap = {
        'users': []
    }

    def __init__(self, configObject):
        MainSlice.config = configObject

    def registerPlugin(self, sliceObject):
        """
        Registers a plugin by taking a reference to its instance.
        Builds a map of plugin names to commands
        """

        if isinstance(sliceObject, MainSlice):
            pluginClassName = sliceObject.__class__.__name__
            print '...loading slice', pluginClassName
            for command in sliceObject.commandDict:
                MainSlice.pluginCommands.update({command: sliceObject})

            MainSlice.plugins.append(pluginClassName)

    def call(self, que, commandName, commandParams=None):
        """
        All commands entered are passed here. This function seeks for
        commandName in pluginCommands, and calls the mapped function
        on that plugin instance. The return value of all plugin
        command calls are pushed into a queue for multiprocessing
        """
        invalidCommand = True
        returnValue = None
        for plugCmd, plugInstance in MainSlice.pluginCommands.items():
            if plugCmd == commandName:
                cc = "command_" + plugCmd
                try:
                    returnValue = getattr(plugInstance, cc)(commandParams)
                except AttributeError:
                    print "!!!!! Valid command, but no definition for it " \
                        "was found in the plugin: ", plugCmd

                invalidCommand = False
                break

        if invalidCommand:
            returnValue = self.noCommandLikeThat(commandName)
        que.put(returnValue)

    def noCommandLikeThat(self, bogusCommand):
        """
        Handles all commands for which there is no mapping.
        Return -1 for "no such command"
        """
        data = "Call %s non-existent" % (bogusCommand,)
        returnDict = {'status': -1, 'data': data}
        return returnDict

    def updateExternalDataMap(self, action, client, pointOfOrigin):
        """
        Takes a dictionary of data to store in this instance, to make it
        accesible to all plugins
        """
        # pointOfOrigin will be used to control data storage at some point
        if action is 'logout':
           if client in MainSlice.externalDataMap['users']:
                MainSlice.externalDataMap['users'].remove(client)
        elif action is 'login':
            if client not in MainSlice.externalDataMap['users']:
                MainSlice.externalDataMap['users'].append(client)

    def getFromExternalDataMap(self, key):
        """
        Returns a key and it's value/s from the externalDataMap
        """
        if key in MainSlice.externalDataMap:
            return MainSlice.externalDataMap[key]

    def getLicenseInformation(self):
        """
        Get the project's license information from a file and make it
        available to any slices(plugins) that may want to use it.
        """
        # get it from a file (license file specified in config, yes?)
        # sort it into a dictionary of copyright notice, link, info
        # return to caller
        print "TODO: getLicenseInformation()"

