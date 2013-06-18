import mysql.connector
from core.common import loadConfig


class Language(object):
    """
    Languages opens a connection to the lang database and handles
    the translation of the UI using the user language in set config file.
    Languages then severs the connection.
    Alexia Pouyaud
    """
    def __init__(self, conf):
        self.conf = conf

    def connectToDbLang(self):
        """
        Establishes connection to dbLang.
        """
        # open connection
        self.cnx = mysql.connector.connect(user='alexia', password='c0ff33', host='ws1.chillijuice.net', database='dbToast_test')

    def getTranslation(self, name):
        """
        (str -> str)
            Fetches the translation for parameter from the collection stored in dbToast_test.
            Pretty tard code for now but I'll get smarted along the way... or you'll just have to put up with it.

        >>> getTranslation('hello')
        >>> Bonjour
        >>> getTranslations('goodbye')
        >>> Aurevoir
        """

        user_language = str(self.conf.get("general", "language"))

        self.connectToDbLang()
        cursor = self.cnx.cursor()
        nameStr = str(name)
        query = ("SELECT " + user_language + " FROM tblLang WHERE MsgName = '" + nameStr + "'")
        cursor.execute(query)

        val = str(cursor.fetchone())

        cursor.close()
        self.cnx.close()

        print "Val: " + val
        print "Val 2: " + val.encode()

        return val
