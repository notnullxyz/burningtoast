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

