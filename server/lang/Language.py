import mysql.connector
from core.common import loadConfig


class Language(object):
    """
    Languages opens a connection to the lang database and handles
    the translation using the user language set in config file.
    Language then severs the connection.
    Alexia Pouyaud
    """
    def __init__(self, conf):
        self.conf = conf

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
        except mysql.connector.Error as mErr:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)

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
