#!/bin/sh

# This script provides the minimal firewall rules necessary to run
# knockknock.  Essentially, no connections are allowed, unless they
# are authenticated with knockknock.
#
# Courtesy: Jake Appelbaum

IPTABLES="/sbin/iptables"

# We want to allow open connections
$IPTABLES -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# Allow everything out
$IPTABLES -A OUTPUT -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
$IPTABLES -A OUTPUT -j ACCEPT

# We want to reject any attempts to forward
$IPTABLES -A FORWARD -j REJECT

# Add the knock knock rules
$IPTABLES -N REJECTLOG
$IPTABLES -A REJECTLOG -j LOG --log-level debug --log-tcp-sequence --log-tcp-options --log-ip-options -m limit --limit 3/s --limit-burst 8 --log-prefix "REJECT "
$IPTABLES -A REJECTLOG -p tcp -j REJECT --reject-with tcp-reset
$IPTABLES -A REJECTLOG -j REJECT

# Reject all other incoming traffic:
$IPTABLES -A INPUT -j REJECTLOG