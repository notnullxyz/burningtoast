from protocol.Spitoon import SpitoonFactory
from twisted.internet import reactor

if __name__ == "__main__":
	"""
	port number could probably just be pulled from cmdline args
        version and name should go into a conf file of sorts
	"""

    version = 0.1
	awesomeName = "BurningToast %s" % (version,)
    print "Starting up %s" % (awesomeName,)
	default_port = 1982

    reactor.listenTCP(default_port, SpitoonFactory(reactor))
    print "listen tcp on port %s" % (default_port,)
    print "starting reactor, run forever"
    reactor.run()


def load_plugins(pluginList):
	"""
	Load all the plugins listed in pluginList (list of classnames)
	Will need to somehow, securely, use reflection/dynamic instancing here
	"""
	pass

