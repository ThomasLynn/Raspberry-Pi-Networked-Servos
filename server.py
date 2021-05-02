#!/usr/bin/env python

import socketserver
import socket
import argparse
import myservo
import json
import pigpio
import time

pi = pigpio.pi()

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="",
    help="Specify an ip the server should be bound to, default is all.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
parser.add_argument("-x_servo", default="12", help="GPIO pin of servo controlled by x axis movement")
parser.add_argument("-y_servo", default="13", help="GPIO pin of servo controlled by y axis movement")
parser.add_argument("-laser_timeout", default="10", help="Number of seconds until the laser pin is turned off after movement")
parser.add_argument("-laser_pin", default="27", help="pin used for the laser (required a transistor)")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

servos = myservo.Servo(int(args.x_servo),pi),myservo.Servo(int(args.y_servo),pi)

laser_pin = int(args.laser_pin)
laser_timeout_length = float(args.laser_timeout)

server = None

laser_timeout = time.time()

# read the data and sets servos to their new positions
def set_position(data):
    for i in range(len(data)):
        if chr(data[i]) == "]":
            data = data[:i+1]
            break
    data = json.loads(data)
    for i in range(len(servos)):
        servos[i].set_angle(data[i], False)
        servos[i].chill_bro()
    global laser_timeout
    laser_timeout = time.time() + laser_timeout_length

# Create the server, binding to localhost on port 3647
try:
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
    sock.bind((HOST, PORT))
    
    sock.settimeout(.1)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            set_position(data)
        except socket.timeout:
            pass
        for w in servos:
            w.chill_bro()
        if laser_timeout < time.time():
            pi.write(laser_pin,0)
        else:
            pi.write(laser_pin,1)
                
except KeyboardInterrupt:
    pass
finally:
    pi.write(laser_pin,0)
    pi.stop()
    if server!=None:
        server.server_close()
        print("server closed")
    print("server shutdown")


