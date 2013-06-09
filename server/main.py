from core.Toaster import ToasterFactory
from twisted.internet import reactor
from slices.MainSlice import MainSlice
from core.common import infomsg, loadPlugins


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
    # creating the base mainslice, and then merely
    # instantiating plugins extending it
    # should keep instances of them, in it's static registry,
    # which cna then be injected into Toaster and used via the
    # MainSlice.plugins['pluginname'].function sort of thing...
    plugbase = MainSlice()

    reactor.listenTCP(default_port, ToasterFactory(reactor, plugbase))
    print "listen tcp on port %s" % (default_port,)
    print "starting reactor, run forever"
    reactor.run()
