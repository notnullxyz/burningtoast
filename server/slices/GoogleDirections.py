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

# uses: The Google Directions API
# https://developers.google.com/maps/documentation/directions/

from MainSlice import MainSlice
import urllib
import json

class GoogleDirections(MainSlice):
    """
    A google directions slice, with a simple origin/destination
    based lookup and simplified responses. Very lazy, sloppy slice
    intended to demonstrate the ease of create a slice.
    """

    endpoint = "http://maps.googleapis.com/maps/api/directions/json?"

    def __init__(self):
        self.commandDict = {
            'direx' : 'provide directions from Google Directions',
        }

        self.load()
        super(GoogleDirections, self).registerPlugin(self)

    def load(self):
        """Standard burningToast requirement method"""
        commands = []
        for command in self.commandDict:
            commands.append(command)

    def command_direx(self, params):
        """
        Calls the Google directions api, and gets things done.
        This is a very crude slice command. Simple and demonstrational

        ---current params---
        param 0: origin
        param 1: destination

        ---params for another version someday---
        mode (driving, walking, bicycling)
        units (metric, imperial)
        avoid (tolls, highways)
        """
        uparms = {}
        okStatus = "ok"
        if len(params) < 2:
            clRespond = super(GoogleDirections, self).needMoreParams(['origin','destination'])
        else:
            uparms['origin'] = params[0]
            uparms['destination'] = params[1]
            uparms['sensor'] = 'false'  # required, else "request denied"
            full = self.endpoint + urllib.urlencode(uparms)
            response = urllib.urlopen(full) 
            clRespond = response.read()

        dats = json.loads(clRespond)
        stat = dats['status'].lower()
        if stat == okStatus.lower():
            status = 0
            data = self.sanitise(dats)
        else:
            status = -1
            data = stat

        return {'status': status, 'data': data}

    def sanitise(self, data):
        # todo - clean up/condense the json data
        return data
