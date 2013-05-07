class Consolate:
	"""
	Console 'print' output class for burningToast
	This is useful for monitoring as the service runs, or redirection in the shell
	"""

	def __init__(self):
		self.commandList = []
		pass

	
	def load(self):
		"""
		Needed for all burningToast plugins to register.
		Must setup all plugin related stuff, and return available commands
		"""
		pass


	def handle_command(self, command, args):
		"""
		Mandatory plugin method. Takes a command and an args list.
		Maps the command to other internal methods to deal with them.
		"""
		pass

