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

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print(inspect.getdoc(self.request))
        # print(inspect.getsource(self.request))

        print ("Got a request of: %s\n" % self.data)
        listOfRequestLines = self.data.split("\r\n")
        if((self.getRequestType(listOfRequestLines)).upper() != "GET"):
            self.sendMethodNotAllowed()
        else:
            filePath = "www/index.html"  # TODO: don't hardcode this
            if(self.getFileSize(filePath) > 0):
                self.sendFile(filePath)
            else:
                self.sendFileNotFound()
        self.request.close()

    def getRequestType(self, listOfRequestLines):
        typeOfRequest = listOfRequestLines[0].split(' ')[0]
        return typeOfRequest

    def getFileSize(self, filePath):
        if(os.access(filePath, os.R_OK)):
            return os.stat(filePath).st_size
        else:
            return 0

    def sendFileNotFound(self):
        self.request.sendall("HTTP/1.1 404 NOT FOUND\r\n")
        self.request.sendall("\r\n")

    def sendMethodNotAllowed(self):
        self.request.sendall("HTTP/1.1 405 METHOD NOT ALLOWED\r\n")
        self.request.sendall("\r\n")

    def sendFile(self, filePath):
        self.request.sendall("HTTP/1.1 200 OK\r\n")
        self.request.sendall("Content-type: text/html; charset=utf-8\r\n")
        self.request.sendall("Content-Length: %s\r\n" % self.getFileSize(filePath))
        self.request.sendall("\r\n")
        fileObj = open(filePath, "rU")  # TODO: i need a try, except on this!
        self.request.sendall(fileObj.read())
        # print(inspect.getdoc(fileObj))
        # print(self.getFileSize("www/noSuchFile.txt"))
        # self.request.sendall("\r\n")  # TODO: how to close connection when sending file


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
