"""
Missy's core functionality
"""

# import land class (default unzoned)
# import residential class (houses, parks)
# import road class (dirt, tar roads)
# import farm class (agricultural stuff)
# import industrial class (factories and such)
# import commercial class (shops, business)

class MissyCore(object):

    def __init__(self):
        # self.worldify() ??
        pass

    def moan(self):
        print "I am Missy, and I am alive."

    def worldify(self):
        # instantiate all classes and stuff

    def persist_world(self, id):
        """
        persist world data as it exists at the time, by id/name
        """

    def land_create(self, id, sizeX, sizeY):
        """
        Create a piece of land, with size X/Y
        """
        pass

    def land_destroy(self, id):
        """
        Destroy a piece of land, by ID
        """
        pass

    def land_info(self, id):
        """
        Return data on a piece of land, if it exists
        """
        pass

