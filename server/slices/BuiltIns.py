from MainSlice import MainSlice

class BuiltIns(MainSlice):
    """
    This is the sample plugin for future plugins and contains the built-in commands
    and features of core.

    """

    def __init__(self):
        """
        this should be the standard for plugins. Command dict to def map, and a call to load
        """
        self.commandDict = {
                'help':'command_help', 
                'version':'command_version',
                'quit':'command_quit'
                }
        self.load()
        super(BuiltIns, self).registerPlugin(self)

    
    def load(self):
        """
        Needed for all burningToast plugins to register, called from constructor.
        """
        commands = []
        for command in self.commandDict:
            commands.append(command)

    
    def command_help(self):
        """
        Built in standard 'help' command.
        This is what command methods should look like.
        """
        print "THIS IS THE HELP COMMAND!"


    def command_version(self):
        """
        Built in standard 'version' command
        """
        print "THIS IS THE VERSION COMMAND!?!?"
        return "5.5"


