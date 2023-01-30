# Original code by Florin Dragan licensed under the MIT License: https://gitlab.com/florindragan/raspberry_pico_w_websocket/-/blob/main/LICENSE

import socket
from websocket import websocket

# Class for client closing their connection error (Doesn't seem to properly work?)
class ClientClosedError(Exception):
    pass

# Class for the actual connection to client
class WebSocketConnection:
    def __init__(self, addr, s, close_callback):
        self.client_close = False
        self._need_check = False

        self.address = addr
        self.socket = s
        self.ws = websocket(s, True)
        self.close_callback = close_callback

        s.setblocking(False)
        s.setsockopt(socket.SOL_SOCKET, 20, self.notify)

    def notify(self, s):
        self._need_check = True

    # Read incoming data
    def read(self):
        if self._need_check:
            self._check_socket_state()

        msg_bytes = None
        try:
            msg_bytes = self.ws.read()
        except OSError:
            self.client_close = True

        if not msg_bytes and self.client_close:
            raise ClientClosedError()

        return msg_bytes

    # Write outgoing data
    def write(self, msg):
        try:
            self.ws.write(msg)
        except OSError:
            self.client_close = True

    # Required for read. Checks if client is alive?
    def _check_socket_state(self):
        self._need_check = False
        sock_str = str(self.socket)
        state_str = sock_str.split(" ")[1]
        state = int(state_str.split("=")[1])

        # Changed this to not equal 3 because otherwise when sending data client gets disconnected
        if state != 3:
            self.client_close = True

    # Close connection (Doesn't seem to properly work?)
    def close(self):
        print("Closing connection.")
        self.socket.setsockopt(socket.SOL_SOCKET, 20, None)
        self.socket.close()
        self.socket = None
        self.ws = None
        if self.close_callback:
            self.close_callback(self)
