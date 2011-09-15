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

import string, sys, os, syslog, time

class LogFile:

    def __init__(self, file):
        self.file = file        

    def checkForFileRotate(self, fd):
        freshFile = open(self.file)
            
        if (os.path.sameopenfile(freshFile.fileno(), fd.fileno())):
            freshFile.close()
            return fd
        else:
            fd.close()
            return freshFile

    def tail(self):
        fd = open(self.file)
        fd.seek(0, os.SEEK_END)
        
        while True:
            fd    = self.checkForFileRotate(fd)
            where = fd.tell()
            line  = fd.readline()

            if not line:
                time.sleep(.25)
                fd.seek(where)
            else:
                yield line
