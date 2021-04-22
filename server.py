#!/usr/bin/env python

import socketserver
import argparse
#import myservo

class CommandTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("data",type(self.data),self.data)
        self.data = list(self.data)
        print("data",type(self.data),self.data)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", default="127.0.0.1",
        help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
    parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
    args = parser.parse_args()
    
    HOST, PORT = args.ip, int(args.port)
    
    #servo = myservo.Servo(17)
    #servo2 = myservo.Servo(27)
    
    # Create the server, binding to localhost on port 3647
    with socketserver.TCPServer((HOST, PORT), CommandTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
#



