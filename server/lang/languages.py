import mysql.connector
from core.common import loadConfig


class Languages():
    """
    Languages opens a connection to the lang database and handles
    the translation of the UI using the user language in set config file.
    Languages then severs the connection.
    """
    def __init__(self, reactorInstance, pluginBaseInstance):
	self.conf = loadConfig()
		
	
    def connectToDbLang():
        """
	Establishes connection to dbLang.
        """
		
	# open connection
	cnx = mysql.connector.connect(user='alexia', password='c0ff33', host='ws1.chillijuice.net', database='dbLang')
                                     
        
    def getTranslastion(name):
	"""
	(str -> str)
		
        Fetches the translation for the parameter from the collection stored in dbLang.
		
	>>> getTranslation('hello')
	>>> Bonjour
	>>> getTranslations('goodbye')
	>>> Aurevoir
		
	"""

	user_language = self.conf.get("general", "language")
		
        cursor = cnx.cursor()
        query = ("SELECT %s FROM tblLang WHERE MsgName =  %s")
        
        cursor.execute(query, (user_language, name))
        for (val) in cursor:
            print(val)
        cursor.close()

	# close connection
	cnx.close()
    
