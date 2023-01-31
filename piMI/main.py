# Async code inspired by Digikey youtube video: https://youtu.be/5VLvmA__2v0 and post: https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c
from uasyncio import create_task, sleep, run
# Allow for async serial listening
from serial import listen
# Allow for connection to wireless
from wireless import connectWireless
# Allow for GPIO access
from gpio import shortPress, longPress, resetPress
# Allow for display access
from display import test

# Original code for web socket server by Florin Dragan licensed under the MIT License: https://gitlab.com/florindragan/raspberry_pico_w_websocket/-/blob/main/LICENSE
# MIT License
# 
# Copyright (c) 2023 Florin Dragan
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient

class clientHandle(WebSocketClient):
    def parse(self):
        try:
            # Check if the user has sent a command to GPIO
            cmd = self.connection.read()
            if cmd:
                # MicroPython doesn't have switch statements :/
                if cmd == b'short':
                    create_task(shortPress())
                elif cmd == b'long':
                    create_task(longPress())
                elif cmd == b'reset':
                    create_task(resetPress())
        except ClientClosedError:
            self.connection.close()

    def process(self, dataList):
        try:
            # Update graphs
            self.connection.write(dataList)
            
        except ClientClosedError:
            self.connection.close()


class AppServer(WebSocketServer):
    # Sets html to load and max connections allowed
    def __init__(self):
        super().__init__("index.html", 10)

    # Creates a client on connection
    def _make_client(self, conn):
        return clientHandle(conn)

# Connect to WiFi network
connectWireless()

# Configure and start server
server = AppServer()
server.start()

# Main loop
async def main():
    # "Setup"
    create_task(listen(server))
    create_task(test())
    # "Loop"
    while True:
        server.parse_all()
        await sleep(1)

run(main())