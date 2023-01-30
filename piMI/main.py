# Async code inspired by Digikey youtube video: https://youtu.be/5VLvmA__2v0 and post: https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c
from uasyncio import create_task, sleep, run
# Allow for async serial listening
from serial import listen
# Allow for connection to wireless
from wireless import connectWireless
# TODO: Temp for debugging
from gpio import shortPress, longPress, resetPress

# Original code by Florin Dragan licensed under the MIT License: https://gitlab.com/florindragan/raspberry_pico_w_websocket/-/blob/main/LICENSE
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
    # "Loop"
    while True:
        # Display here eventually
        server.parse_all()
        await sleep(1)

run(main())