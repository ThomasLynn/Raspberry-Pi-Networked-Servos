#!/usr/bin/env python

import socketserver
import socket
import argparse
import myservo
import json
import pigpio

pi = pigpio.pi()

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
parser.add_argument("-x_servo", default="12", help="GPIO pin of servo controlled by x axis movement")
parser.add_argument("-y_servo", default="13", help="GPIO pin of servo controlled by y axis movement")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

servos = myservo.Servo(int(args.x_servo),pi),myservo.Servo(int(args.y_servo),pi)

# Create the server, binding to localhost on port 3647
server = None
try:
    server = socketserver.TCPServer((HOST, PORT), CommandTCPHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    
    server.timeout = 0.1
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        server.handle_request()
        for w in servos:
            w.chill_bro()
    #server.serve_forever()
                
except KeyboardInterrupt:
    pass
finally:
    #for w in servos:
    #    w.stop()
    #GPIO.cleanup()
    pi.stop()
    if server!=None:
        server.server_close()
        print("server closed")
    print("server shutdown")


