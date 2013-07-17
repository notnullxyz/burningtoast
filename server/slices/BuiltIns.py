from MainSlice import MainSlice
import datetime


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
            'quit': 'Disconnects and drops the current connection',
            'who': "Shows a list of logged in clients",
            'date': 'Returns the current date in a full format',
            'msg': 'Message another user. msg <userid/name> <message>',
#            'plugins': 'List all registered plugins.'
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

    def command_msg(self, params):
        """
        Built in simple inter-user messager handler
        Two parameters are used, 0-destination client, 1-message
        This simply returns the message and a special handle code to Toaster.
        """
        if len(params) < 2:
            chatDict = {
                'status': -1,
                'data': 'not enough params. Need <destination client> <msg>'
                }
        else:
            msgFull = ' '.join(params[1::1])
            chatDict = {
                'status': 998,
                'data': {
                    'destClient': str(params[0]),
                    'message': str(msgFull)
                    }
                }
        return chatDict

    def command_who(self, params):
        """
        BuiltIn who command. Shows who else is logged in.
        """
        f = super(BuiltIns, self).getFromExternalDataMap('users')
        return {'status': 0, 'data': {'numClients': len(f), 'clients': f}}

    def command_help(self, params):
        """
        Built in standard 'help' command.
        This is what command methods should look like.
        """
        helpOutput = {}
        # loop through all plugins in MainSlice, and find their help dict??
        # then print it out as a guide
        for cmd, sliceObject in MainSlice.pluginCommands.items():
            helpOutput.update({cmd: sliceObject.commandDict[cmd]})

        return {'status': 0, 'data': helpOutput}

    def command_language(self, params):
        """
        Built in 'lang' command, returns whatever is set in the config.
        """
        lang = MainSlice.config.get('general', 'language')
        return {'status': 0, 'data': lang}

    def command_date(self, params):
        dt = datetime.date.today().strftime('day %j of %Y, week %W, %A, %d%B, %H:%M:%S')
        return {'status': 0, 'data': dt}

    def command_quit(self, params):
        """
        Do something to sign off the user gracefully
        Sending back a status 999, Toaster will know what to do
        """
        return {'status': 999, 'data': None}
