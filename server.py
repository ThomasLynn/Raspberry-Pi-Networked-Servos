#!/usr/bin/env python

import socketserver
import socket
import argparse
import myservo
import json
import pigpio

pi = pigpio.pi()

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="",
    help="Specify an ip the server should be bound to, default is all.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
parser.add_argument("-x_servo", default="12", help="GPIO pin of servo controlled by x axis movement")
parser.add_argument("-y_servo", default="13", help="GPIO pin of servo controlled by y axis movement")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

servos = myservo.Servo(int(args.x_servo),pi),myservo.Servo(int(args.y_servo),pi)

server = None

# read the data and sets servos to their new positions
def set_position(data):
    print("got data",type(data),data)
    for i in range(len(data)):
        if chr(data[i]) == "]":
            data = data[:i+1]
            break
    print("got data2",type(data),data)
    data = json.loads(data)
    print("data2",type(data),data)
    for i in range(len(servos)):
        servos[i].set_angle(data[i], False)
        servos[i].chill_bro()

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
            print("data",data,"addr",addr)
            set_position(data)
        except socket.timeout:
            pass
        for w in servos:
            w.chill_bro()
                
except KeyboardInterrupt:
    pass
finally:
    pi.stop()
    if server!=None:
        server.server_close()
        print("server closed")
    print("server shutdown")


