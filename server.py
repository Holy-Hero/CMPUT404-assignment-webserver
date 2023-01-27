#  coding: utf-8
import socketserver
import os


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
        self.data = self.request.recv(1024).strip().decode()
        print("Got a request of: %s\n" % self.data)
        data = self.data.split(" ")

        if data[0] == "":
            res = "HTTP/1.1 400 Bad Request\n\n"
            self.request.sendall(bytearray(res, 'utf-8'))
            return
        else:
            if data[0] != "GET":
                res = "HTTP/1.1 405 Method Not Allowed\n\n"
                self.request.sendall(bytearray(res, 'utf-8'))
                return
            else:
                res = "HTTP/1.1 404 Not Found\n"
                path = data[1]

                if path.endswith("/"):
                    path += "/index.html"

                if os.path.isdir("www" + path + "/"):
                    res = "HTTP/1.1 301 Move Permanently\nLocation: " + path + "/"
                    self.request.sendall(bytearray(res, 'utf-8'))
                    return

                try:
                    file = open("./www" + path)
                    content = file.read()
                    file.close()
                    if path.endswith(".html"):
                        res = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + content
                    elif path.endswith(".css"):
                        res = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n" + content
                except Exception as e:
                    res = "HTTP/1.1 404 Not Found\n\n"
                finally:
                    self.request.sendall(bytearray(res, 'utf-8'))
                    return


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
