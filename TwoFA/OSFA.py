import os
import random
import threading
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

with open("osfa_settings.json") as f:
    settings = json.loads(f.read())

hostName = settings["host"]
serverPort = int(settings["port"])

tokenLength = int(settings["tokenLength"])
keyLength = int(settings["keyLength"])

global key
key = ""


def keyGen():
    global key

    while True:
        key = ""
        for i in range(0, keyLength):
            key += random.choice("1234567890")

        with open("active.key", "w") as f:
            f.write(key)
        time.sleep(30)


threading.Thread(target=keyGen).start()


def genRandomKey(length):
    key = ""
    for i in range(0, length):
        key += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_")
    return key


def handleGetRequest(request, self):
    def sendGet(sendData):
        self.wfile.write(sendData)

    if len(request) == 0:
        if not os.path.exists("token.tk"):
            ranToken = genRandomKey(tokenLength)
            with open("token.tk", "a") as f:
                f.write(ranToken)

            sendGet(bytes("<script>window.location = '{}'</script>".format("/auth/" + ranToken), "utf-8"))
            return

        with open("accessible_files/404_screen.html", "r") as f:
            sendGet(bytes(f.read(), "utf-8"))
        return

    with open("token.tk") as f:
        if request[0] != "auth":
            return

        if request[1] == f.read():
            with open("accessible_files/token_screen.html") as f:
                sendGet(bytes(f.read(), "utf-8"))


def handlePostRequest(request, self):
    global key

    def sendPost(sendData):
        response = BytesIO()
        for line in sendData.split("\n"):
            response.write(bytes(line, "utf-8"))
        self.wfile.write(response.getvalue())
        return

    with open("token.tk") as f:
        if request.split("/")[0] != f.read():
            return

        if request.split("/")[1] != "getkey":
            return

        sendPost(key)


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        requestList = list(filter(None, str(self.path).split("/")))
        handleGetRequest(requestList, self)

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        requestRaw = self.rfile.read(content_length)
        request = requestRaw.decode("utf-8")

        handlePostRequest(request, self)  # Send post request


def startServer():
    webServer = HTTPServer((hostName, serverPort), WebServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped")
