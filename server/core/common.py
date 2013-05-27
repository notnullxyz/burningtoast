from parts.BuiltIns import BuiltIns


def infomsg():
    version = 0.1
    awesomeName = "BurningToast %s" % (version,)
    print "Starting up %s" % (awesomeName,)


def loadPlugins():
    """
    instantiate plugin classes. They should all extend MainPart. On creation, they
    will run their load() methods, inserting them into the static plugin registry.
    The instances created here will go out of scope with this function, perfect?
    """
    #perhaps
    # for each in a string list of plugin part classnames:
    #     a = reflectTheStringClassName()
    a = BuiltIns()



