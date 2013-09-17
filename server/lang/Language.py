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
from core.common import loadConfig

class Language(object):
    """
    Languages opens a connection to the lang database and handles
    the translation using the user language set in config file.
    Language then severs the connection.
    Alexia Pouyaud
    """
    def __init__(self, conf, errorCallback):
        self.conf = conf
        self.errCallback = errorCallback

    def connectToDbLang(self):
        """
        Establishes connection to dbLang.
        """
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

    def getTranslation(self, name):
        """
        (str -> str)
            Fetches the translation for parameter from the collection stored
            in dbToast_test. Pretty tard code for now but I'll get smarter
            along the way... or you'll just have to put up with it.

        >>> getTranslation('hello')
        >>> Bonjour
        >>> getTranslations('goodbye')
        >>> Aurevoir
        """

        user_language = self.conf.get("general", "language")

        self.connectToDbLang()
        cursor = self.cnx.cursor()
        query = (
            """SELECT """
            + user_language
            + """ FROM tblLang WHERE MsgName = %s""")
        cursor.execute(query, (name, ))
        val = cursor.fetchone()
        cursor.close()
        self.cnx.close()
        # For xlation, only need a unicode object back, not the whole tuple
        return val[0]
