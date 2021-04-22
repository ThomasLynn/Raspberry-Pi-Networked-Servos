#!/usr/bin/env python

import myservo
import socket

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="127.0.0.1",
    help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

servo = myservo.Servo(17)
servo2 = myservo.Servo(27)
try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            x = float(sock.recv(32))
            y = float(sock.recv(32))
            servo.set_angle(x)
            servo.set_angle(y)
        #servo.set_angle(0)
        #servo.set_angle(180)
        #servo2.set_angle(0)
        #servo2.set_angle(180)
except KeyboardInterrupt:
    pass
finally:
    servo.stop()
