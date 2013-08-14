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
            'direxhelp' : 'explains a bit about using direx'
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
        Also, just realised the API spews out JSON, so no need
        to massage it :-)

        ---current params---
        param 0: origin
        param 1: destination

        ---params for another version someday---
        mode (driving, walking, bicycling)
        units (metric, imperial)
        avoid (tolls, highways)
        """
        uparms = {}
        if len(params) < 2:
            clRespond = super(GoogleDirections, self).needMoreParams(['origin','destination'])
        else:
            uparms['origin'] = params[0]
            uparms['destination'] = params[1]
            uparms['sensor'] = 'false'  # required, else "request denied"
            response = urllib.urlopen(self.endpoint, urllib.urlencode(uparms))
            clRespond = response.read()

        print clRespond    # todo, massage into bT style response


    def command_direxhelp(self, params):
        """Some help and plugging Google for their API :-)"""
        pass

