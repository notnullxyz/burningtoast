from MainSlice import MainSlice


class BuiltIns(MainSlice):
    """
    This is the sample plugin for future plugins and contains the
    built-in commands and features of core.
    """

    def __init__(self):
        """
        this should be the standard for plugins. 
        Command list of allowed calls on this plugin/slice
        """
        self.commandDict = {
            'help': 'Prints this help command.',
            'language': 'Shows what language is specified in config',
            'quit': 'Disconnects and drops the current connection'
        }
        self.load()
        super(BuiltIns, self).registerPlugin(self)


    def load(self):
        """
        Needed for all burningToast plugins to register, constructor call.
        """
        commands = []
        for command in self.commandDict:
            commands.append(command)

    def command_help(self):
        """
        Built in standard 'help' command.
        This is what command methods should look like.
        """
        helpOutput = ''
        # loop through all plugins in MainSlice, and find their help dict??
        # then print it out as a guide
        for cmd, sliceObject in MainSlice.pluginCommands.items():
            helpOutput = ''.join(cmd + "-" + sliceObject.commandDict[cmd])

        return {'status': 0, 'data': helpOutput}

    def command_language(self):
        """
        Built in 'lang' command, returns whatever is set in the config.
        """
        lang = MainSlice.config.get('general', 'language')
        return {'status': 0, 'data': lang}

    def command_quit(self):
        """
        Do something to sign off the user gracefully
        Sending back a status 999, Toaster will know what to do
        """
        return {'status': 999, 'data': None}
