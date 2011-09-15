Some History:

    The port knockingconcept has been around for a while, and there
    are many different port knocking implementations.  The core idea
    is that you send a sequence of innocuous looking packets to a
    server, which have the effect of adjusting the firewall rules to
    allow you to connect through on a port that was previously
    firewalled off.
  
    Originally, this was simply conceived as a series of connection
    attempts to closed ports in a specific order.  The "knock" would
    be something like trying to connect to ports 12, 23, 18, 66, or
    whatever, in that order, over a specific period of time.
  
    The problem with the original concept was that if your port
    sequence was observed by passive eavesdropping, it was easily
    replayable.  The obvious solution was to develop a port knocking
    system that did not allow for replay attacks.  Such a solution
    suggests the use of cryptography.
  
    And this is where the insanity begins.  People started
    implementing all kinds of stuff to achieve this goal, and along
    the way lost sight of the original intent behind port knocking.
  
    Let me tell you what I /don't/ want from a port knocking
    implementation:
    
      * I don't want something written in an an unsafe language.  This
        should be a very small application, and the performance
        requirements should be minimal.  
      * I don't want something that runs /in the kernel/.  
      * I don't want an entirely new service that binds to a port.  
      * I don't want something that uses libpcap and inspects /every/ 
        packet.  
      * I don't want something that uses UDP.  
      * I don't want something that generates obvious port-knock 
        requests and leaves an observer knowing exactly what port is 
        about to open up.  
      * I don't want something which requires that more than one
        packet move over the network.  
      * I don't want something that uses half-baked cryptography and
        isn't provably IND-CCA secure.
    
  
    But from what I can tell, this is exactly what people have
    implemented.  Despite the fact that the main thrust of this is to
    have less services running, the direction that this has been going
    is to have whole servers written in C that bind to sockets and
    exchange UDP packets.  The entire /point/ of port-knocking was for
    it to be stealthy, simple, and secure.  The goal was to eliminate
    network services, not create more of them.  We can use
    cryptography to /simplify/ the initial port knocking concept,
    rather than making it more complex.
  
knockknock Overview:

    So here's how knockknock works:
    
      * Servers run the python app 'knockknock-daemon', and clients
        open ports on those servers by running the python app
        'knockknock'

      * 'knockknock-daemon' simply tails kern.log.  It doesn't bind to
        any sockets, load libpcap and inspect every packet, or send
        anything onto the network at all.

      * When you want to open a port from a client, you run
        'knockknock', which sends a /single/ SYN packet to the server.
        The packet's IP and TCP headers are encoded to represent an
        IND-CCA secure encrypted request to open a specified port from
        the source IP address.

      * Fields from this packet are logged to kern.log and processed
        by 'knockknock-daemon', which validates them.

      * You connect from the client to the now-open port on the
        server.

      * The port closes behind you and doesn't allow any new
        connections.
    
  
    That's it.  Written in python, simple, single-packet, secure.
  
    The request is encrypted using AES in CTR mode, with an HMAC-SHA1
    using the authenticate-then-encrypt paradigm.  It protects against
    evesdropping, replay attacks, and all known forms of cryptanalysis
    against IND-CCA secure schemes.
  
Why Is knockknock Secure?
  
    * The knockknock-daemon code is very simple, and is written in
      python (a 'safe' language).  The code is concise enough to be
      easily audited, and doesn't make use of any crazy libraries like
      libpcap.

    * While knockknock-daemon needs root priviledges to adjust
      iptables rules, it employs privilege separation to isolate the
      code that actually runs as root to ~15 lines.  So even though
      the entire code base is very small and very simple, the only
      part of the code actually running with root privilges is even
      smaller and even simpler.  When you run knockknock-daemon, it
      will fork out the privileged code and drop privilges everywhere
      else before processing knockknock requests.

    * The communication protocol is a simple IND-CCA secure encryption
      scheme that uses standard, contemporary, cryptographic
      constructions.  An observer watching packets is not given any
      indication that the SYN packet transmitted by 'knockknock' is a
      port knocking request, but even if they knew, there would be no
      way for them to determine which port was requested to open.
      Replaying the knock request later does them no good, and in fact
      does not provide any information that might be useful in
      determining the contents of future requets.
  
  
Why Is This Even Necessary?  

    /You are running network services with security vulnerabilities in
    them./ Again, /you are running network services with security
    vulnerabilities in them/.  If you're running a server, this is
    almost universally true.  Most software is complex.  It changes
    rapidly, and innovation tends to make it more complex.  It is
    going to be, forever, hopelessly, insecure.  Even projects like
    OpenSSH that were designed from the ground-up with security in
    mind, where every single line of code is written with security as
    a top priority, where countless people audit the changes that are
    made every day -- even projects like this have suffered from
    remotely exploitable vulnerabilities.  If this is true, what hope
    do the network services that are written with different priorities
    have?
  
    The name of the game is to isolate, compartmentalize, and /expose
    running services as little as possible/.  That's where knockknock
    comes in.  Given that your network services are insecure, you want
    to expose as few of them to the world as possible.  I offer
    knockknock as a possible solution to minimizing exposure.
  

