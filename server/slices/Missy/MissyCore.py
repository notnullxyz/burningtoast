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

class MissyCore(object):
    """
    Missy's core functionality
    """

    def __init__(self):
        # self.worldify() ??
        pass

    def moan(self, params):
        moaning = "I am Missy, and I am alive."
        if params is not None:
            return moaning + ' '.join([word.upper() for word in params])
        return moaning

    def setup_data(self):
        # instantiate all classes and data provider
        pass

    def create_brick(self, id):
        """
        persist world data as it exists at the time, by id/name
        """
        pass

    def delete_brick(self, id):
        """
        Destroy a piece of land, by ID
        """
        pass

    def material_info(self, id):
        """
        Return data on a piece of land, if it exists
        """
        pass

