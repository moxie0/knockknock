#!/usr/bin/env python
__author__ = "Moxie Marlinspike"
__email__  = "moxie@thoughtcrime.org"
__license__= """
Copyright (c) 2009 Moxie Marlinspike <moxie@thoughtcrime.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

"""

import time, os, sys
import getopt
import subprocess

from struct import *
from knockknock.Profile import Profile

def usage():
    print "Usage: knockknock.py -p <portToOpen> <host>"
    sys.exit(2)
    
def parseArguments(argv):
    try:
        port       = 0
        host       = ""
        opts, args = getopt.getopt(argv, "h:p:")
        
        for opt, arg in opts:
            if opt in ("-p"):
                port = arg
            else:
                usage()
                
        if len(args) != 1:
            usage()
        else:
            host = args[0]

    except getopt.GetoptError:           
        usage()                          

    if port == 0 or host == "":
        usage()

    return (port, host)

def getProfile(host):
    homedir = os.path.expanduser('~')
    
    if not os.path.isdir(homedir + '/.knockknock/'):
        print "Error: you need to setup your profiles in " + homedir + '/.knockknock/'
        sys.exit(2)

    if not os.path.isdir(homedir + '/.knockknock/' + host):
        print 'Error: profile for host ' + host + ' not found at ' + homedir + '/.knockknock/' + host
        sys.exit(2)

    return Profile(homedir + '/.knockknock/' + host)

def verifyPermissions():
    if os.getuid() != 0:
        print 'Sorry, you must be root to run this.'
        sys.exit(2)    

def existsInPath(command):
    def isExe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        exeFile = os.path.join(path, command)
        if isExe(exeFile):
            return exeFile

    return None

def main(argv):
    (port, host) = parseArguments(argv)
    verifyPermissions()
    
    profile      = getProfile(host)
    port         = pack('!H', int(port))
    packetData   = profile.encrypt(port)
    knockPort    = profile.getKnockPort()
    
    (idField, seqField, ackField, winField) = unpack('!HIIH', packetData)

    hping = existsInPath("hping3")

    if hping is None:
        print "Error, you must install hping3 first."
        sys.exit(2)

    command = [hping, "-S", "-c", "1",
               "-p", str(knockPort),
               "-N", str(idField),
               "-w", str(winField),
               "-M", str(seqField),
               "-L", str(ackField),
               host]
    
    try:
        subprocess.call(command, shell=False, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        print 'Knock sent.'

    except OSError:
        print "Error: Do you have hping3 installed?"
        sys.exit(3)

if __name__ == '__main__':
    main(sys.argv[1:])
