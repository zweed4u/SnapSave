#!/bin/bash -e

if [ $# -lt 1 ]; then
    echo "usage: $0 --set or $0 --unset"
    exit 0
else
    if [ $1 = "--set" ]
    then 
        SET=1
    elif [ $1 = "--unset" ]
    then
        SET=0
    else 
        echo "usage: $0 --set or $0 --unset"
        exit 0
    fi
fi

IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')

# Open firewall to accept connections 
iptables -P FORWARD ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

# Set to 1 the kernel forwarding
sysctl -w net.ipv4.ip_forward=$SET

if [ $SET -eq 1 ]
then
    RULE="-A"
else 
    RULE="-D"
fi

# Ruleset to send receivd traffic from port 80 and 443 to port 8080 
iptables -t nat $RULE PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to $IP:8080
iptables -t nat $RULE PREROUTING -i wlan0 -p tcp --dport 443 -j DNAT --to $IP:8080


# Export LANG variable needed by mitmproxy
if [ $SET -eq 1 ]; then
    echo "Maybe to use mitmproxy you need to export LANG=en_US.UTF-8"
fi
