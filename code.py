!/usr/bin/env python
import time
import busio
import board
import digitalio
import os
from adafruit_circuitplayground.express import cpx

uart = busio.UART(board.TX, board.RX, baudrate=115200)
cpx.pixels.fill((30, 30, 30))

x =1
recording = False
up = True
#Outputs button signals to serial
while True:
    switch_position = cpx.switch
    if not recording:
        # gently pulsing white light while ready but not recording
        cpx.pixels.fill((x, x, x))
        if up:
            x =x + 1
        if not up:
            x = x - 1
        if x > 25:
            up = False
        if x < 2:
            up = True
    if cpx.button_a:
        print(1) #Output 1 to start recording
        #Light CPX red while recording
        cpx.pixels.fill((50, 0, 0))
        recording = True 
        time.sleep(0.1)
    if cpx.button_b:
        print(2) #Output 2 to stop recording
        recording = False

    if switch_position is not cpx.switch:
        print(3) #Output 3 to reboot RPi
        recording = False
    time.sleep(0.1)
    

