#  coding: utf-8
import socketserver


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


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        if not self.data == "":
            self.data = self.data.split(" ")
            if not self.data[0] == "GET":
                self.res = "405 Method Not Allowed\n"
            else:
                self.res = "200 OK\n"
                self.path = self.data[1]

        if self.path == "/":
            self.path = "/index.html"

        if self.path.endwith("/") or self.path.endswith(".html") or self.path.endswith(".css"):
            try:
                file = open("www" + self.path + "Content-Type: text/html; UTF-8\n")
                content = file.read()
                file.close()

                self.res = "HTTP/1.0 200 OK\n" + content
            except:
                self.res = "404 not found\n"
            finally:
                self.request.sendall(bytearray(self.res, 'utf-8'))
        else:
            self.res = "301 Moved Permanently/nLocation: " + self.path + "/"
            self.request.sendall(bytearray(self.res, 'utf-8'))
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
