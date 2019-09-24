#!/bin/bash
. $HOME/.profile
export XDG_RUNTIME_DIR="/run/user/1000"
/usr/bin/python3 /home/pi/listen_serial.py "/home/pi/newlogs.txt" &
