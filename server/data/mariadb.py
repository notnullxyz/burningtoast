##
#    Copyright 2013 Alexia Pouyaud
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

import mysql.connector

class MariaDB(object):

    def __init__(self, conf, errorCallback):
        self.conf = conf
        self.errCallback = errorCallback
        self.cnx = None
        self.connect()

    def connect(self):
        dbconf = {
                'user': self.conf.get('database', 'username'),
                'password': self.conf.get('database', 'password'),
                'host': self.conf.get('database', 'hostname'),
                'database': self.conf.get('database', 'database'),
                'port': self.conf.getint('database', 'port'),
                'charset': self.conf.get('database', 'charset'),
                }

        try:
            self.cnx = mysql.connector.connect(**dbconf)
        except mysql.connector.Error as err:
            self.errCallback('Cannot connect to database: %s' % (err, ))

    def connection(self):
        return self.cnx

    def select(self):
        """this must be done at some point"""
        pass

    def insert(self):
        """this must also be done at some point"""
        pass

    def update(self):
        pass

    def delete(self):
        pass

