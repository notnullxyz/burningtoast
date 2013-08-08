##
#    Copyright 2013 Marlon van der Linde
#
#    This file is part of BurningToast
#
#    BurningToast is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BurningToast is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BurningToast.  If not, see <http://www.gnu.org/licenses/>.
##

from slices.BuiltIns import BuiltIns
from slices.GoogleDirections import GoogleDirections
import ConfigParser
from sys import exit

cfname = 'mains.cfg'
cfg = None
version = 0.111
appName = "BurningToast %s" % (version,)



def infomsg():
    print "Starting up %s" % (appName,)


def loadPlugins(conf):
    """
    instantiate plugin classes. They should all extend MainSlice.
    On creation, they will run their load() methods, inserting
    them into the static plugin registry. The instances created
    here will go out of scope with this function, perfect?
    """
    pluginsToLoad = conf.get('plugins', 'loadlist')
    pluginList = pluginsToLoad.split(',')
    plugins = map(__import__, pluginList)

    #perhaps
    #for each in config file section of plugin part classnames:
    #     a = reflectTheStringClassName()
    #a = BuiltIns()
    #b = GoogleDirections()


def configFileExists():
    try:
        with open(cfname):
            return True
    except:
        return False


def loadConfig():
    """loadConfig should happen very early, even before loadPlugins"""
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
