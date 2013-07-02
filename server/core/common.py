from slices.BuiltIns import BuiltIns
import ConfigParser
from sys import exit

cfname = 'mains.cfg'
cfg = None


def infomsg():
    version = 0.1
    awesomeName = "BurningToast %s" % (version,)
    print "Starting up %s" % (awesomeName,)


def loadPlugins():
    """
    instantiate plugin classes. They should all extend MainSlice.
    On creation, they will run their load() methods, inserting
    them into the static plugin registry. The instances created
    here will go out of scope with this function, perfect?
    """
    #perhaps
    # for each in a string list of plugin part classnames:
    #     a = reflectTheStringClassName()
    a = BuiltIns()


def configFileExists():
    try:
        with open(cfname):
            return True
    except:
        return False


def loadConfig():
    if configFileExists():
        cfg = ConfigParser.RawConfigParser()
        cfg.read(cfname)
        print "Loaded configuration File: %s" % (cfname, )
        return cfg
    else:
        print "Could not load configuration, you need a %s file" % (cfname, )
        return None


def fatality_iminent(why):
    print "Something is wrong, and we can't really go on like this"
    print "====== %s ======" % (why, )
    exit()
