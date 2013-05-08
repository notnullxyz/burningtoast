from datetime import datetime

class MainPart:

	plugins = {}

	def __init__(self):
		pass

	def registerPlugin(self, partObject):
		if isinstance(partObject, MainPart):
				MainPart.plugins[partObject.__class__.__name__] = partObject

	def std_date(self):
		"""return a standard formed date for plugin consumption"""
		now = datetime.now()
		dateformat = "%Y-%m-%d %H:%M:%S"
		return now.strftime(dateformat)

