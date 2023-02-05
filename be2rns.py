#!/usr/bin/env python3

# Format sent by Binary Eye with POST application/json
# {"content":"3560071258757","format":"CODE_128","errorCorrectionLevel":"",
#  "version":"","sequenceSize":"-1","sequenceIndex":"-1","sequenceId":"",
#  "timestamp":"2023-02-04 22:04:02"}

PORT_NUMBER = 4577 # Could be set also on command line
ADD_ENTER   = True # Add a enter after barcode

# Don't modify below -----------------------------------------------------------
# Remote-numpad-server address, on the same machine, with harcoded port
RNS_HOST = '127.0.0.1'
RNS_PORT = 4576

from http.server import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import socketserver
import json
import cgi

import sys
import socket
import time

# Helper function
def send_to_remote_numpad(plusminus, char):
    netcat(RNS_HOST, RNS_PORT, plusminus + char)
    return

# netcat simulation, modified
def netcat(hn, p, content):
    # initialize the connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (hn,p) )

    sock.sendall(content.encode(encoding='utf_8'))
    time.sleep(0.01)
    sock.shutdown(socket.SHUT_WR)

    res = ""

    while True:
        data = sock.recv(1024)
        if (not data):
            break
        res += data.decode()

    sock.close() 

class BEtoRNS_Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        return

    def do_HEAD(self):
        self._set_headers()

    # POST transmits the barcode to Remote-numpad-server one char at a time
    #      + enter at the end if activated
    def do_POST(self):
        ctype, pdict = cgi.parse_header( self.headers.get('content-type') )

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length  = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        # Extract the barcode and send it to Remote-numpad-server
        self._set_headers()
        json_string = json.dumps(message)
        barcode = json.loads(json_string)["content"]

        # Send every digit
        for char in barcode:
            send_to_remote_numpad("+", char)
            send_to_remote_numpad("-", char)

        # Add enter
        if ADD_ENTER:
            send_to_remote_numpad("+", "enter")
            send_to_remote_numpad("-", "enter")

        # Return the barcode that will be displayed in Binary Eye
        self.wfile.write(barcode.encode(encoding='utf_8'))

def run( server_class=HTTPServer, handler_class=BEtoRNS_Server, port=PORT_NUMBER):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting BinaryEye-to-RemoteNumpad proxy on port %d...' % port)
    httpd.serve_forever()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        run( port = int(sys.argv[1]) )
    else:
        run()
