#!/bin/sh
sudo sh -c '/sbin/iptables-restore < /etc/iptables.up.rules'
