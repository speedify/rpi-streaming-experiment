# Circuit Playground Express Setup

### For ffmpeg streaming to Twitch on the Raspberry Pi

We used these steps here at Connectify to set up the Adafruit Circuit Playground Express as a remote for Twitch livestreaming on the Raspberry Pi. We have it set up so that the left button starts the live stream from a camera connected via an Elgato Cam Link plugged into one of your USB 3.0 ports, and the right button terminates the stream. Moving the switch to the right will reboot the Raspberry Pi if needed. 

1. First, you will need to install ffmpeg on the Raspberry Pi for streaming to Twitch. The install command is `apt-get install ffmpeg` but for more detailed compilation instructions see [this compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu).

1. Next, plug the Circuit Playground Express in via USB and make sure you have CircuitPy installed on it. [Install instructions for CircuitPy are here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).

1. Install [Mu Editor](https://codewith.mu/en/howto/1.0/install_raspberry_pi) or another preferred python editor if you don't already have it, and save the code.py file to the top level directory of Circuit Playground Express device. This file should output button inputs over serial.

1. Save the listen_serial.py file in your home directory. Open the file in your editor and set the stream_key, input_video_device, and input_audio_device variables. The stream_key variable is your own Twitch stream key inside quotes - found in your Twitch channel settings. Comments in listen_serial.py detail how to find the right audio and video devices. This python script will listen over serial and execute the appropriate bash commands when the buttons are pressed.

1. Save the listen_serial.sh file in your home directory. This is a shell script to start the python script as a background process. If you would like to save log files from the Python script's output for debugging, you can add a directory flag in this file before the '&'. e.g. `/usr/bin/python3 /home/pi/listen_serial.py "/home/pi/log.txt" &` 

1. Enter `crontab -e` into the terminal to edit the crontab and add this line to the bottom. This will wait 30 seconds after Pi reboot and then run the listen_serial.sh shell script.
``` @reboot sleep 30; /home/pi/listen_serial.sh ```

Now, with the Circuit Playground express plugged into the pi via usb, your camera plugged into the Cam Link and powered on, and a stable internet connection, you should be able to press the left button, see the remote light up red, and stream to your Twitch channel. 

If it doesn't start streaming after a few seconds, try hitting the right button to quit and starting the stream with left button again. If it still isn't working, you may want to enable logs in the shell script and check for errors. You might have to modify the ffmpeg command in the listen_serial.py file to suit your own equipment setup. Additionally, if you aren't seeing the red ring of lights on the Circuit Playground Express when you press the left button, then there may be an issue with the CircuitPy installation. 

