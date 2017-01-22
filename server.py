#  coding: utf-8
import SocketServer  # used for handling the tcp connection w/ the client
import mimetypes  # used to decode/encode filename/url <=> MIME type
import os  # used to access files on disk
import inspect  # used to determine the available methods on objects

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


# Example Print out of this file (server.py)
# GET / HTTP/1.1
# Host: 127.0.0.1:8080
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print(inspect.getdoc(SocketServer.BaseRequestHandler))
        # print(inspect.getsource(SocketServer.BaseRequestHandler))
        # print("-----")
        # print(inspect.getdoc(self.request))
        # print(inspect.getsource(self.request))

# HTTP/1.0 200 OK
# Server: SimpleHTTP/0.6 Python/2.7.5
# Date: Sun, 22 Jan 2017 19:33:29 GMT
# Content-type: text/html; charset=utf-8
# Content-Length: 574

        print ("Got a request of: %s\n" % self.data)
        listOfRequestLines = self.data.split("\r\n")
        if((self.getRequestType(listOfRequestLines)).upper() != "GET"):
            self.request.sendall("HTTP/1.1 405 METHOD NOT ALLOWED\r\n")
        else:
            self.request.send("HTTP/1.1 200 OK\r\n")
            self.request.send("Content-type: text/html; charset=utf-8\r\n")
            self.request.send("Content-Length: 574\r\n")
            self.request.send("\r\n")
            fileObj = open("www/index.html", "rU")
            self.request.send(fileObj.read())
            # print(inspect.getdoc(fileObj))

    def getRequestType(self, listOfRequestLines):
        typeOfRequest = listOfRequestLines[0].split(' ')[0]
        return typeOfRequest


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
