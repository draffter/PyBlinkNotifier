#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess


class ServerHandle(BaseHTTPRequestHandler):
    blink = None

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if self.path == "/blink":
            self.play_notification()
            self.blink.blink_pattern((0, 170, 85,), 500, 0.5)

    @staticmethod
    def play_notification():
        f = '0745.wav'
        subprocess.Popen(['aplay', '-q', 'wav/' + f])


class Server(object):

    def __init__(self, blink):
        ServerHandle.blink = blink
        server_address = ('', 9996)
        httpd = HTTPServer(server_address, ServerHandle)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
