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

import syslog

from LogEntry import LogEntry
from MacFailedException import MacFailedException

class KnockWatcher:

    def __init__(self, config, logFile, profiles, portOpener):
        self.config     = config
        self.logFile    = logFile
        self.profiles   = profiles
        self.portOpener = portOpener

    def tailAndProcess(self):
        for line in self.logFile.tail():
            try:
                logEntry = LogEntry(line)
                profile  = self.profiles.getProfileForPort(logEntry.getDestinationPort())

                if (profile != None):
                    try:
                        ciphertext = logEntry.getEncryptedData()
                        port       = profile.decrypt(ciphertext, self.config.getWindow())
                        sourceIP   = logEntry.getSourceIP()
                    
                        self.portOpener.open(sourceIP, port)
                        syslog.syslog("Received authenticated port-knock for port " + str(port) + " from " + sourceIP)
                    except MacFailedException:
                        pass
            except:
#                print "Unexpected error:", sys.exc_info()
                syslog.syslog("knocknock skipping unrecognized line.")
