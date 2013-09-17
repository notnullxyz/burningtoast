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

from slices.MainSlice import MainSlice
import MissyCore

class Missy(MainSlice):
    """
    A more complex, package based Slice for a simulation/modelling idea
    """

    def __init__(self):
        self.commandDict = {
            'moan': 'A basic starting command... dumps info'
        }

        self.load()
        super(Missy, self).registerPlugin(self)
        self.createCore()

    def createCore(self):
        print "Creating a Single MissyCore instance"
        self.mc = MissyCore.MissyCore()

    def load(self):
        """
        Needed for all burningToast plugins to register, constructor call.
        """
        commands = []
        for command in self.commandDict:
            commands.append(command)

    # from here onwards, wrap MissyCore functionality into command calls

    def command_moan(self, params):
        """
        Moan, MIssy, Moan
        """
        print params
        return {'status': 0, 'data': self.mc.moan()}

