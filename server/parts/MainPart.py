from datetime import datetime

class MainPart:

	plugins = {}
	pluginCommands = {}

	def __init__(self):
		pass

	def registerPlugin(self, partObject):
		if isinstance(partObject, MainPart):
			# map each cmd on the registrant to itself so it can be found
			for command in partObject.commandDict:
				pluginCommands[partObject.__class__.__name__] = command


	def std_date(self):
		"""return a standard formed date for plugin consumption"""
		now = datetime.now()
		dateformat = "%Y-%m-%d %H:%M:%S"
		return now.strftime(dateformat)

