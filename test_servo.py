#!/usr/bin/env python

# a script for testing the servo to see if it's working
# you'll need to type "sudo pigpiod" into your terminal before running this script

import pigpio
import argparse
import myservo

parser = argparse.ArgumentParser()
parser.add_argument("-servo_pin", default="12", help="GPIO pin of servo to test")
args = parser.parse_args()

pi = pigpio.pi()

servo = myservo.Servo(int(args.servo_pin),pi)

try:
    for i in range(3):
        servo.set_angle(0, True)
        servo.set_angle(180, True)
        servo.set_angle(45, True)
        servo.set_angle(135, True)
except KeyboardInterrupt:
    pass
finally:
    pi.stop()
    