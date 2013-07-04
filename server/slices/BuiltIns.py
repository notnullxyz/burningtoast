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
        self.commandList = [
            'help',
            'language',
            'quit'
        ]
        self.load()
        super(BuiltIns, self).registerPlugin(self)

    def load(self):
        """
        Needed for all burningToast plugins to register, constructor call.
        """
        commands = []
        for command in self.commandList:
            commands.append(command)

    def command_help(self):
        """
        Built in standard 'help' command.
        This is what command methods should look like.
        """
        # loop through all plugins in MainSlice, and find their help dict??
        # then print it out as a guide
        return {'status': 0, 'data': "TODO: a decent help response mechanism"}

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
