#!/bin/bash
interface=$(/bin/cat /home/letder/media/scripts/iface.txt)
ip_addr=$(/bin/ip -br a | grep $interface | grep -oP "\d{1,3}\.\d{1,3}\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}")

/bin/printf " Local IP | $ip_addr | "
