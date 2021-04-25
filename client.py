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
parser.add_argument("-flip1",action='store_true', help="flip servo 1")
parser.add_argument("-flip2",action='store_true', help="flip servo 2")
args = parser.parse_args()
print("args",args)

HOST, PORT = args.ip, int(args.port)

root = tk.Tk()
root.geometry(args.sizex+"x"+args.sizey)
win_size = (float(args.sizex), float(args.sizey))
my_canvas = tk.Canvas(root)
my_canvas.pack()

x = 90
y = 90

def key(event):
    print("event",event)
    if event.char=='d':
        set_pos(x+1, y)
    if event.char=='a':
        set_pos(x-1, y)
    if event.char=='s':
        set_pos(x, y+1)
    if event.char=='w':
        set_pos(x, y-1)

def motion(event):
    set_pos(event.x, event.y)
    
def set_pos(new_x, new_y):
    global x,y
    x, y = new_x, new_y
    print('{}, {}'.format(x, y))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        positions = [float(x)*180.0/win_size[0],float(y)*180.0/win_size[0]]
        if args.flip1:
            positions[0] = 180 - positions[0]
        if args.flip2:
            positions[1] = 180 - positions[1]
        sock.sendall(json.dumps(positions).encode())
        #sock.sendall(bytes([x,y]))
    my_canvas.create_rectangle(0, 0, win_size[0], win_size[1], fill='white')
    my_canvas.create_oval(x-5, y-5, x+5, y+5)

root.bind('<B1-Motion>', motion)
root.bind('<Button-1>', motion)
root.bind('<Key>', key)
root.mainloop()