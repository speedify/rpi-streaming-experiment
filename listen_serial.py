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

#(Ex: /dev/video0, /dev/video1)
input_video_device = "YOUR VIDEO DEVICE"  #Can find available devices with "v4l2-ctl --list-devices"
#(Ex: hw:=Headset,DEV=0, hw:CARD=Link,DEV=0, hw:0)
input_audio_device = "YOUR AUDIO DEVICE" #Can find available inputs with "aplay -L", or "arecord -l"
input_resolution = None #Leave None or specify a resolution (ex: 1920x1080)
input_framerate = None #Leave None or specify a framerate (ex: 60)
output_resolution = None #Leave None or specify a resolution (ex: 1920x1080)
output_framerate = None  #Leave None or specify a framerate (ex: 60)
stream_key = "YOUR STREAM KEY HERE" #Copied from your Twitch channel settings.


#Command to start ffmpeg streaming.
ffmpeg_command = ("ffmpeg -nostdin -f v4l2 {0} {1} -i {2} "
     "-f alsa -ac 1 -i {3} "
     "-vcodec libx264 -rtbufsize 2000k {4} {5} -preset ultrafast -pix_fmt yuv420p -crf 17 -force_key_frames "
     "'expr:gte(t,n_forced*2)' -minrate 850k -maxrate 1000k -b:v 1000k -bufsize 1000k "
     "-acodec libmp3lame -rtbufsize 2000k -b:v 96k -ar 44100 -f flv 'rtmp://live.twitch.tv/app/{6}'"
     .format("-s {0}".format(input_resolution) if input_resolution is not None else '',
             "-framerate {0}".format(input_framerate) if input_framerate is not None else '',
             input_video_device,
             input_audio_device,
             "-s {0}".format(output_resolution) if output_resolution is not None else '',
             "-framerate {0}".format(output_framerate) if output_framerate is not None else '',
             stream_key))
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