#!/usr/bin/env python
import time
import busio
import board
import digitalio
import os
from adafruit_circuitplayground.express import cpx

uart = busio.UART(board.TX, board.RX, baudrate=115200)

switch_position = cpx.switch

#Outputs button signals to serial
while True:
    if cpx.button_a:
        print(1) #Output 1 to start recording
        #Light CPX red while recording
        cpx.pixels.fill((50, 0, 0))
        time.sleep(0.1)
    if cpx.button_b:
        print(2) #Output 2 to stop recording
        cpx.pixels.fill((0, 0, 0))
    if switch_position is not cpx.switch:
        print(3) #Output 3 to reboot RPi
    time.sleep(0.1)