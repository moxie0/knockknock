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

import os, sys
from knockknock.Profiles import Profiles
from knockknock.Profile  import Profile

DAEMON_DIR   = '/etc/knockknock.d/'
PROFILES_DIR = DAEMON_DIR + 'profiles/'

def usage():
    print "knockknock-genprofile <profileName> <knockPort>"
    sys.exit(3)

def checkProfile(profileName):
    if (os.path.isdir(PROFILES_DIR + profileName)):
        print "Profile already exists.  First rm " + PROFILES_DIR + profileName + "/"
        sys.exit(0)

def checkPortConflict(knockPort):
    if (not os.path.isdir(PROFILES_DIR)):
        return

    profiles        = Profiles(PROFILES_DIR)    
    matchingProfile = profiles.getProfileForPort(knockPort)

    if (matchingProfile != None):
        print "A profile already exists for knock port: " + str(knockPort) + " at this location: " + matchingProfile.getDirectory()

def createDirectory(profileName):
    if not os.path.isdir(DAEMON_DIR):
        os.mkdir(DAEMON_DIR)

    if not os.path.isdir(PROFILES_DIR):
        os.mkdir(PROFILES_DIR)
    
    if not os.path.isdir(PROFILES_DIR + profileName):
        os.mkdir(PROFILES_DIR + profileName)

def main(argv):
    
    if len(argv) != 2:
        usage()

    profileName = argv[0]
    knockPort   = argv[1]
        
    checkProfile(profileName)
    checkPortConflict(knockPort)
    createDirectory(profileName)

    random    = open('/dev/urandom', 'rb')
    cipherKey = random.read(16)
    macKey    = random.read(16)
    counter   = 0

    profile = Profile(PROFILES_DIR + profileName, cipherKey, macKey, counter, knockPort)
    profile.serialize()
    random.close()

    print "Keys successfully generated in " + PROFILES_DIR + profileName

if __name__ == '__main__':
    main(sys.argv[1:])
