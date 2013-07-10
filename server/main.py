from core.Toaster import ToasterFactory
from twisted.internet import reactor
from slices.MainSlice import MainSlice
from core.common import infomsg, loadPlugins, loadConfig, fatality_iminent
from lang.Language import Language



if __name__ == "__main__":
    """
    port number could probably just be pulled from cmdline args
        version and name should go into a conf file of sorts
    """
    conf = loadConfig()
    if conf is None:
        fatality_iminent('no config file')

    infomsg()
    loadPlugins()

    lang = Language(conf)

    default_port = conf.getint('server', 'port')

    # ------- this comment will be gone some day -----------------------
    # for now, this is a very shitty way of loading plugins... TODO asap
    # creating the base mainslice, and then merely
    # instantiating plugins extending it
    # should keep instances of them, in it's static registry,
    # which cna then be injected into Toaster and used via the
    # MainSlice.plugins['pluginname'].function sort of thing...
    # ------------------------------------------------------------------
    plugbase = MainSlice(conf)

    reactor.listenTCP(default_port, ToasterFactory(reactor, plugbase, lang))
    listenMsg = lang.getTranslation('sysListenPort')
    print "%s %d" % (listenMsg, default_port)

    reactor.run()
