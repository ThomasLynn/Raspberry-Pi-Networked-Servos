#!/usr/bin/env python

import socket
import argparse
import tkinter as tk
import json

parser = argparse.ArgumentParser()
parser.add_argument("-ip", default="127.0.0.1",
    help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
parser.add_argument("-sizex", default="400", help="defaut x size of window")
parser.add_argument("-sizey", default="400", help="defaut x size of window")
args = parser.parse_args()

HOST, PORT = args.ip, int(args.port)

root = tk.Tk()
root.geometry(args.sizex+"x"+args.sizey)
win_size = (float(args.sizex), float(args.sizey))

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(json.dumps([float(x)*180.0/win_size[0],float(y)*180.0/win_size[0]]).encode())
        #sock.sendall(bytes([x,y]))

root.bind('<Motion>', motion)
root.mainloop()