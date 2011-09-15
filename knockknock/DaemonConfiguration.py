# Copyright (c) 2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import os
import ConfigParser

class DaemonConfiguration:

    def __init__(self, file):
        try:
            parser = ConfigParser.SafeConfigParser({'delay': '15', 'error_window': '20'})
            parser.read(file)

            self.delay  = int(parser.get('main', 'delay'))
            self.window = int(parser.get('main', 'error_window'))
        except ConfigParser.NoSectionError:
            print "knockknock-daemon: config file not found, assuming defaults."
            self.delay  = 15
            self.window = 20

    def getDelay(self):
        return self.delay

    def getWindow(self):
        return self.window
