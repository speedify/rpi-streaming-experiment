#!/usr/bin/python3
import serial
import subprocess
import os
import time
import sys

def write_log(log_file, log):
    with open(log_file, "a") as f:
        f.write(log+"\n")
log_file = sys.stdout
if (len(sys.argv) > 1):
    log_file = sys.argv[1]
write_log(log_file, "Starting script")
try:
    ser = serial.Serial('/dev/ttyACM0', 115200)
except:
    write_log(log_file, "Caught exception creating serial object")
    sys.exit()
ffmpeg_file = None


streamKey = "YOUR STREAM KEY HERE" #Copied from your Twitch channel settings.


#Command to start ffmpeg streaming.
ffmpeg_command = "/home/pi/bin/ffmpeg -nostdin -re -f v4l2 -s '1280x720' -framerate 24 -i /dev/video0 -f alsa -ac 2 -i hw:CARD=Link,DEV=0 -vcodec libx264 -framerate 24 -rtbufsize 1500k -s 1280x720 -preset ultrafast -pix_fmt yuv420p -crf 17 -force_key_frames 'expr:gte(t,n_forced*2)' -minrate 850k -maxrate 1000k -b:v 1000k -bufsize 1000k -acodec libmp3lame -rtbufsize 1500k -b 96k -ar 44100 -f flv - | ffmpeg -f flv -i - -c copy -f flv -drop_pkts_on_overflow 1 -attempt_recovery 1 -recovery_wait_time 1 'rtmp://live.twitch.tv/app/" + streamKey + "'\n"
proc_running = False
while True:
    line = ser.readline()
    if (b"1" in line and proc_running is False): #if left button is pressed, start streaming
        write_log(log_file, "Starting ffmpeg")
        open_log = open(log_file,"a")
        subprocess.Popen(["bash","-c",ffmpeg_command], stdout=open_log, stderr=open_log)
        proc_running = True
    if (b"2" in line and proc_running is True): #if right button is pressed, terminate streaming
        subprocess.Popen(["bash", "-c", "pkill ffmpeg"])
        proc_running = False
        open_log.close()
        write_log(log_file, "terminated script")
    if (b"3" in line): #if CPX switch is moved, reboot RPi
        os.system('sudo reboot')
    time.sleep(.5)
ser.close()