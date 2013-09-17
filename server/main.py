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

from core.Toaster import ToasterFactory
from twisted.internet import reactor
from slices.MainSlice import MainSlice
from core.common import infomsg, loadPlugins, loadConfig, fatality_iminent
from lang.Language import Language
from data.Database import Database

if __name__ == "__main__":
    """
        Fire this up for a crispy snack
    """
    conf = loadConfig(fatality_iminent)
    db = Database(conf, fatality_iminent).determine_driver()
    print "%s %s" % ('Database loaded:', db)
    infomsg()
    loadPlugins(conf)
    lang = Language(conf, fatality_iminent)
 
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
