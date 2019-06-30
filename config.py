# Setup LiPoPi global variable array
lipopi = {}

# input GPIO that receives shutdown requests from momentary button press
lipopi["shutdown_pin"] = 24

# input GPIO that receives low battery signal from PowerBoost board
lipopi["low_battery_pin"] = 23

# output GPIO that disables power once RPi has performed shutdown
# NB: This pin needs to start at HIGH once pi is booted, and go LOW once pi shuts down.
# This pin is not controlled by this script.
# Per "BCM2835 Arm Peripherals 6.2 Alternative function assignments" valid pins are:
# GPIO/BCM: 0, 1, 2, 3, 4, 5, 6, 7, 8, 34, 35, 36
lipopi["power_disable_pin"] = 5

# full path to logfile
lipopi["logfile"] = "/home/pi/lipopi.log"

# Seconds to wait before initiating shutdown
lipopi["shutdown_wait"] = 2

