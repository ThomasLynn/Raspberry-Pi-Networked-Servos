#!/usr/bin/env python

import socketserver

# Takes text data from the client and runs that text as a command

# WARNING: This is super-duper NOT secure. anyone with a little
# technical know-how on your local network will be able to run
# any command they want on your computer while this server is running.
# Use at your own risk.

# NOTE: Your firewall and your router's firewall will stop anyone from
# accessing this server from outside your network by default.
# I strongly advise you do NOT let people outside your network run
# any command they want on your machine

# NOTE2: To be able to connect to this server from another computer on
# your network, you must bind your local ip address with the -ip <ip>
# argument.
# To get your local ip address, go to your command line and type
# ipconfig (windows)
# ifconfig (linux)
# and find your ipv4 (or ipv6) address.

class CommandTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        
        # convert the recieved data to a regular string
        text = self.data.decode()
        print(text)
            
        # just send back the same data, but upper-cased
        # this is totally not required for the command stuff
        # but I just haven't gotten around to removing it
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", default="127.0.0.1",
        help="The ip the server should be bound to, type ipconfig (or ifconfig) in the command line to get your local ip.")
    parser.add_argument("-port", default="3647", help="The port the server should be bound to.")
    args = parser.parse_args()
    
    HOST, PORT = args.ip, int(args.port)

    # Create the server, binding to localhost on port 3647
    with socketserver.TCPServer((HOST, PORT), CommandTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
#



