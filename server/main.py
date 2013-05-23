from core.Spitoon import SpitoonFactory
from twisted.internet import reactor
from parts.MainPart import MainPart
from core.common import infomsg,loadPlugins


if __name__ == "__main__":
    """
    port number could probably just be pulled from cmdline args
        version and name should go into a conf file of sorts
    """
    default_port = 1982

    infomsg()
    loadPlugins()

    # -------------
    # for now, this is a very shitty way of loading plugins... TODO asap
    # creating the base mainpart, and then merely instantiating plugins extending it
    # should keep instances of them, in it's static registry, which cna then be injected
    # into spitoon and used via the MainPart.plugins['pluginname'].function sort of thing...
    plugbase = MainPart()

    reactor.listenTCP(default_port, SpitoonFactory(reactor, plugbase))
    print "listen tcp on port %s" % (default_port,)
    print "starting reactor, run forever"
    reactor.run()

