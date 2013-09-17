##
#    Copyright 2013 Marlon B van der Linde
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

import importlib

class Database(object):
    """
    Determines the driver (class) from config, and then attempts
    to load it by reflection.
    For now, I am developing this around MariaDB/MySQL

    Database driver classes, for now, should adhere to:
        __init__(self, configObject, errorCallback)
    and have a connection() method which returns a connected
    database object
    """

    def __init__(self, conf, errorCallback):
        self.conf = conf
        self.errCallback = errorCallback

    def determine_driver(self):
        """
        Heads up: this determines the db driver from the config file.
        It uses the driver instance returned from load_driver, and returns
        an instance to that connection via .connection()
        """
        try:
            driver = self.conf.get('database', 'driver')
        except:
            self.errCallback('Database() loader: Couldn\'t find a "driver=" section in configuration')
        driverInstance = self.load_driver(driver)
        return driverInstance.connection()

    def load_driver(self, className):
        """
        An attempt at dynamically importing and instantiating
        a database class. Reflection all mighty.
        Returns an instance of the database driver class requested
        """
        className = 'data' + '.' + className.lower() + '.' + className
        class_data = className.split(".")
        module_path = ".".join(class_data[:-1])
        class_str = class_data[-1]
        try:
            module = importlib.import_module(module_path)
        except ImportError as ie:
            self.errCallback('Database() Loader: %s' % (ie, ))
        # passing conf and errorCallback, drivers need these in constructors
        return getattr(module, class_str)(self.conf, self.errCallback)

