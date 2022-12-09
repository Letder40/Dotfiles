#!/bin/bash

local_ip=$(ip a | grep -Po "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" | grep -v "^127\." | grep -v "^255\." | grep -v "255$" | grep -v "\.0$" | head -n1 | tr -d "\n")
vpn_ip=$(ip a | grep -PA 2 "tun\d+:" | grep -Pv "tun\d+:|link/none" | grep -oP "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" | head -n1 | tr -d "\n")

if [[ $vpn_ip == "" ]]; then
  echo "IP | $local_ip |" | tr -d "\n"
else
  echo  "VPN | $vpn_ip |" | tr -d "\n"
fi


