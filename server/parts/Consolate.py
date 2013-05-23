from MainPart import MainPart

class Consolate(MainPart):
    """
    Console 'print' output class for burningToast
    This is useful for monitoring as the service runs, or redirection in the shell
    """

    def __init__(self):
        """
        this should be the standard for plugins. Command dict to def map, and a call to load
        """
        self.commandDict = {
                'cdump':'consoleDump', 
                'cspacer':'consoleSpacer'
                }
        self.load()

    
    def load(self):
        """
        Needed for all burningToast plugins to register.
        Must setup all plugin related stuff
        """
        commands = []
        for command in self.commandDict:
            commands.append(command)

        self.registerPlugin(self)


    def handle_command(self, command, args):
        """
        Mandatory plugin method. Takes a command and an args list.
        Maps the command to other internal methods to deal with them.
        """
        if command in self.commandDict:
            self.commandDict[command]()
        else:
            print "E: Calling uncallable command: %s" % (command,)
    

    def cdump(self, args):
        """
        Command handler for cdump: console dump
        Takes a simple list of strings for arguments for printing them on a line of output
        """
        outputLine = "%s : " % (self.std_date(), )
        for arg in args:
            outputLine = "%s - %s" % (outputLine, str(arg))
        print str(outputLine)


    def cspacer(self):
        """ most complex method in the world, print a blank line"""
        print ' '


