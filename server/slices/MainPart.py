from datetime import datetime
#import pprint

class MainPart(object):

    plugins = []
    pluginCommands = {}        # pluginClassName:command

    def __init__(self):
        pass

    def registerPlugin(self, partObject):
        """
        Registers a plugin by taking a reference to its instance. 
        Builds a map of plugin names to commands
        """
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(partObject.commandDict)

        if isinstance(partObject, MainPart):
            pluginClassName = partObject.__class__.__name__
            for command in partObject.commandDict:
                MainPart.pluginCommands.update({command:partObject})

            MainPart.plugins.append(pluginClassName)


    def call(self, commandName):
        """
        All commands entered are passed here. This function seeks for commandName
        in pluginCommands, and calls the mapped function on that plugin instance.
        The return value of all plugin command calls are captured and returned.
        """
        invalidCommand = True
        returnValue = None
        for plugCmd, plugInstance in MainPart.pluginCommands.items():
            if plugCmd == commandName:
                returnValue = getattr(plugInstance, "command_" + plugCmd)()
                invalidCommand = False
        
        if invalidCommand:
            self.noCommandLikeThat(commandName)
        return returnValue

    
    def noCommandLikeThat(self, bogusCommand):
        """
        Handles all commands for which there is no mapping
        """
        print "NO COMMAND LIKE THAT!"


