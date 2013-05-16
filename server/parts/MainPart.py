from datetime import datetime

class MainPart(object):

	plugins = []
	pluginCommands = {}		# pluginClassName:command

	def __init__(self):
		pass

	def registerPlugin(self, partObject):
		"""
		Registers a plugin by taking a reference to its instance. 
		Builds a map of plugin names to commands
		"""
		print "REGISTER PLUGIN CALLED: %s" % (partObject,)
		if isinstance(partObject, MainPart):
			pluginClassName = partObject.__class__.__name__
			for command in partObject.commandDict:
				pluginCommands[partObject] = command
			plugins.append(pluginClassName)


	def call(self, commandName):
		"""
		All commands entered are passed here. This function seeks for commandName
		in pluginCommands, and calls the mapped function on that plugin instance.
		"""
		print "(call happening for %s)" % (commandName,)
		for plugInstance, plugCmd in MainPart.pluginCommands.iteritems():
			if plugCmd == commandName:
				plugInstance[plugCmd]()
			else:
				self.noCommandLikeThat(commandName)

	
	def noCommandLikeThat(self, bogusCommand):
		"""
		Handles all commands for which there is no mapping
		"""
		print "NO COMMAND LIKE THAT!"


