#!/usr/bin/env python

# lipopi.py

# Example python script that uses the LiPoPi circuitry to handle the safe shutdown of
# a Raspberry Pi in response to user request or low battery

# See the README file for details on how to set this up with systemd
# this script is called by /etc/systemd/system/lipopi.service
# This version uses the GPIO event trigger machinery

# 2016 - Robert Jones - Freely distributed under the MIT license

# based on Daniel Bull"s LiPoPi project - https://github.com/NeonHorizon/lipopi

# 2019 - James Sinclair - Modified for use with a 555 timer.

import os
import time

import RPi.GPIO as GPIO
from config import lipopi

# TODO: use logging to write to logfile
# TODO: refactor with gpiozero

# Configure the GPIO pins
def lipopi_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # setup the pin to check the shutdown switch - use the internal pull down resistor
    GPIO.setup(lipopi["shutdown_pin"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # setup the low battery check pin
    GPIO.setup(lipopi["low_battery_pin"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # create a trigger for the shutdown switch and low battery pins
    GPIO.add_event_detect(lipopi["shutdown_pin"], GPIO.FALLING, callback=lipopi_user_shutdown, bouncetime=300)
    GPIO.add_event_detect(lipopi["low_battery_pin"], GPIO.FALLING, callback=lipopi_low_battery_shutdown, bouncetime=300)

    # open log file in append mode
    lipopi["logfile_pointer"] = open(lipopi["logfile"], "a+")


# Detect when the switch is pressed - wait shutdown_wait seconds - then shutdown
def lipopi_user_shutdown(channel):
    cmd = "sudo wall 'System shutting down in %d seconds'" % lipopi["shutdown_wait"]
    os.system(cmd)
    msg = time.strftime("User Request - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())
    rpi_shutdown(msg)


def rpi_shutdown(msg):
    lipopi["logfile_pointer"].write(msg)
    lipopi["logfile_pointer"].close()
    time.sleep(lipopi["shutdown_wait"])
    GPIO.cleanup()
    os.system("sudo shutdown now")


# Respond to a low battery signal from the PowerBoost and shutdown
# Pin goes low on low battery
def lipopi_low_battery_shutdown(channel):
    cmd = "sudo wall 'System shutting down in %d seconds'" % lipopi["shutdown_wait"]
    os.system(cmd)
    msg = time.strftime("Low Battery - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())
    rpi_shutdown(msg)


# Close the log file, reset the GPIO pins
def lipopi_cleanup():
    lipopi["logfile_pointer"].close()
    GPIO.cleanup()


if __name__ == "__main__":
    # setup the GPIO pins and event triggers
    lipopi_setup()

    # Although the shutdown is triggered by an interrupt, we still need a loop
    # to keep the script from exiting - just do a very long sleep
    while True:
        time.sleep(6000)

    # clean up if the script exits without machine shutdown
    lipopi_cleanup()
