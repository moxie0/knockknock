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

import os, syslog, time
import subprocess

from RuleTimer import RuleTimer

class PortOpener:

    def __init__(self, stream, openDuration):
        self.stream       = stream
        self.openDuration = openDuration

    def waitForRequests(self):
        while True:
            sourceIP    = self.stream.readline().rstrip("\n")
            port        = self.stream.readline().rstrip("\n")

            if sourceIP == "" or port == "":
                syslog.syslog("knockknock.PortOpener: Parent process is closed.  Terminating.")
                os._exit(4)                    

            description = 'INPUT -m limit --limit 1/minute --limit-burst 1 -m state --state NEW -p tcp -s ' + sourceIP + ' --dport ' + str(port) + ' -j ACCEPT'
            command     = 'iptables -I ' + description
            command     = command.split()            

            subprocess.call(command, shell=False)

            RuleTimer(self.openDuration, description).start()

    def open(self, sourceIP, port):
        try:
            self.stream.write(sourceIP + "\n")
            self.stream.write(str(port) + "\n")
            self.stream.flush()
        except:
            syslog.syslog("knockknock:  Error, PortOpener process has died.  Terminating.")
            os._exit(4)
