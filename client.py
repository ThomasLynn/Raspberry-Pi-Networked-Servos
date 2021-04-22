#!/usr/bin/env python

import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="127.0.0.1",
    help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)
try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes([90,100]))
except KeyboardInterrupt:
    pass
finally:
    servo.stop()
