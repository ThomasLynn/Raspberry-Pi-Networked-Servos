#!/usr/bin/env python

import socketserver
import socket
import argparse
import myservo
import json
import RPi.GPIO as GPIO

class CommandTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("data",type(self.data),self.data)
        #self.data = list(self.data)
        self.data = json.loads(self.data)
        print("data",type(self.data),self.data)
        for i in range(len(servos)):
            servos[i].set_angle(self.data[i], False)
            servos[i].chill_bro()
                

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="127.0.0.1",
    help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
parser.add_argument("-s1", default="17", help="GPIO pin of servo 1")
parser.add_argument("-s2", default="27", help="GPIO pin of servo 2")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

servos = myservo.Servo(int(args.s1)),myservo.Servo(int(args.s2))

# Create the server, binding to localhost on port 3647
server = None
try:
    server = socketserver.TCPServer((HOST, PORT), CommandTCPHandler)
    server.timeout = 0.1
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        server.handle_request()
        #for w in servos:
        #    w.chill_bro()
    #server.serve_forever()
                
except KeyboardInterrupt:
    pass
finally:
    if server!=None:
        server.server_close()
    #server.shutdown()
    for w in servos:
        w.stop()
    GPIO.cleanup()


