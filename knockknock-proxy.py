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

import os, sys, asyncore, socket

from knockknock.Profiles import Profiles
from knockknock.proxy.SocksRequestHandler import SocksRequestHandler

import knockknock.daemonize

class ProxyServer(asyncore.dispatcher):

    def __init__(self, port, profiles):
        asyncore.dispatcher.__init__(self)
        self.profiles = profiles
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("127.0.0.1", port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        SocksRequestHandler(conn, self.profiles)


def usage():
    print "knockknock-proxy <listenPort>"
    sys.exit(3)

def getProfiles():
    homedir  = os.path.expanduser('~')
    profiles = Profiles(homedir + '/.knockknock/')
    profiles.resolveNames()
    
    return profiles

def checkPrivileges():
    if not os.geteuid() == 0:
        print "\nSorry, knockknock-proxy has to be run as root.\n"
        usage()

def checkProfiles():
    homedir = os.path.expanduser('~')

    if not os.path.isdir(homedir + '/.knockknock/'):
        print "Error: you need to setup your profiles in " + homedir + "/.knockknock/"
        sys.exit(2)

def main(argv):
    
    if len(argv) != 1:
        usage()
        
    checkPrivileges()
    checkProfiles()

    profiles = getProfiles()        
    server   = ProxyServer(int(argv[0]), profiles)

    knockknock.daemonize.createDaemon()
    
    asyncore.loop(use_poll=True)

if __name__ == '__main__':
    main(sys.argv[1:])
