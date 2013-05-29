from slices.BuiltIns import BuiltIns


def infomsg():
    version = 0.1
    awesomeName = "BurningToast %s" % (version,)
    print "Starting up %s" % (awesomeName,)


def loadPlugins():
    """
    instantiate plugin classes. They should all extend MainSlice. On creation, they
    will run their load() methods, inserting them into the static plugin registry.
    The instances created here will go out of scope with this function, perfect?
    """
    a = BuiltIns()



