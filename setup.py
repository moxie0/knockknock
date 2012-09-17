import sys, os, shutil
from distutils.core import setup, Extension

if sys.argv[1] != "sdist":
    shutil.copyfile("knockknock-daemon.py", "knockknock/knockknock-daemon")
    shutil.copyfile("knockknock-genprofile.py", "knockknock/knockknock-genprofile")
    shutil.copyfile("knockknock-proxy.py", "knockknock/knockknock-proxy")
    shutil.copyfile("knockknock.py", "knockknock/knockknock")

setup  (name         = 'knockknock',
        version      = '0.8',
        description  = 'A cryptographic single-packet port-knocker.',
        author       = 'Moxie Marlinspike',
        author_email = 'moxie@thoughtcrime.org',
        url          = 'http://www.thoughtcrime.org/software/knockknock/',
        license      = 'GPL',
        packages     = ["knockknock", "knockknock.proxy"],
        scripts      = ['knockknock/knockknock-daemon',
                        'knockknock/knockknock-genprofile',
                        'knockknock/knockknock-proxy',
                        'knockknock/knockknock'],
        data_files   = [("", ["minimal-firewall.sh", "knockknock-daemon.py", 
                              "knockknock-genprofile.py", "knockknock-proxy.py", 
                              "knockknock.py"]),
                        ('share/knockknock', ['README', 'INSTALL', 'COPYING']),
                        ('/etc/knockknock.d/', ['config'])]
       )

print "Cleaning up..."

if os.path.exists("build/"):
    shutil.rmtree("build/")

try:
    os.remove("knockknock/knockknock-proxy")
    os.remove("knockknock/knockknock-daemon")
    os.remove("knockknock/knockknock-genprofile")
    os.remove("knockknock/knockknock")

except:
    pass

def capture(cmd):
    return os.popen(cmd).read().strip()
