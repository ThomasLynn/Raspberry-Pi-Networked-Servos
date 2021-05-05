#!/usr/bin/env python

import socket
import argparse
import tkinter as tk
import json

parser = argparse.ArgumentParser()
parser.add_argument("ip",
    help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
parser.add_argument("-sizex", default="400", help="X size of window")
parser.add_argument("-sizey", default="400", help="Y size of window")
parser.add_argument("-flip1", action='store_true', help="Flip servo 1?")
parser.add_argument("-flip2", action='store_true', help="Flip servo 2?")
parser.add_argument("-movex", default="1", help="Jump size when using A and D")
parser.add_argument("-movey", default="1", help="Jump size when using W and S")
parser.add_argument("-x", default="0", help="Lowerbound of x servo angle")
parser.add_argument("-w", "--width", default="180", help="Width of x servo angle")
parser.add_argument("-y", default="0", help="Lowerbound of y servo angle")
parser.add_argument("-he", "--height", default="180", help="Height of y servo angle")

args = parser.parse_args()
print("args",args)

HOST, PORT = args.ip, int(args.port)

root = tk.Tk()
root.geometry(args.sizex+"x"+args.sizey)
win_size = [float(args.sizex), float(args.sizey)]
circle_size = [win_size[0] *0.05, win_size[0] * 0.07]
jump_size = [float(args.movex), float(args.movey)]
servo_zero_positions = [float(args.x), float(args.y)]
servo_distance = [float(args.width), float(args.height)]
if args.flip1:
    print("flipping 1")
    servo_zero_positions[0] = 180 - servo_zero_positions[0]
    servo_distance[0] = - servo_distance[0]
if args.flip2:
    print("flipping 2")
    servo_zero_positions[1] = 180 - servo_zero_positions[1]
    servo_distance[1] = - servo_distance[1]


my_canvas = None

x = 90
y = 90

sock = None

def set_socket(new_sock):
    global sock
    sock = new_sock

def key(event):
    if event.char=='d':
        set_pos(x+jump_size[0], y)
    if event.char=='a':
        set_pos(x-jump_size[0], y)
    if event.char=='s':
        set_pos(x, y+jump_size[1])
    if event.char=='w':
        set_pos(x, y-jump_size[1])

def motion(event):
    set_pos(event.x, event.y)
    
def set_pos(new_x, new_y, canvas_sizes = None):
    global x,y
    x, y = new_x, new_y
    if canvas_sizes is None:
        positions = [servo_zero_positions[0] + (float(x)/win_size[0])*servo_distance[0]
            ,servo_zero_positions[1] + (float(y)/win_size[0])*servo_distance[1]]
    else:
        positions = [servo_zero_positions[0] + (float(x)/canvas_sizes[0])*servo_distance[0]
            ,servo_zero_positions[1] + (float(y)/canvas_sizes[0])*servo_distance[1]]
    sock.sendall(json.dumps(positions).encode())
    if my_canvas is not None:
        my_canvas.create_rectangle(0, 0, win_size[0], win_size[1], fill='white')
        my_canvas.create_oval(x-circle_size[0], y-circle_size[1], x+circle_size[0], y+circle_size[1], fill = "red")

if __name__ == "__main__":
    my_canvas = tk.Canvas(root, width = win_size[0], height = win_size[1])
    my_canvas.pack()
    root.bind('<B1-Motion>', motion)
    root.bind('<Button-1>', motion)
    root.bind('<Key>', key)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Connect to server and send data
        set_socket(sock)
        sock.connect((HOST, PORT))
        root.mainloop()