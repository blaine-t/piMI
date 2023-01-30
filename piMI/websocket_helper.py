# Original code by Florin Dragan licensed under the MIT License: https://gitlab.com/florindragan/raspberry_pico_w_websocket/-/blob/main/LICENSE

# Hashing required for server handshake
from ubinascii import b2a_base64
from uhashlib import sha1

# No clue how this works as it is not my original code
def server_handshake(sock):
    clr = sock.makefile("rwb", 0)
    l = clr.readline()

    webkey = None

    while True:
        l = clr.readline()
        if not l:
            raise OSError("EOF in headers")
        if l == b"\r\n":
            break
        h, v = [x.strip() for x in l.split(b":", 1)]
        if h == b'Sec-WebSocket-Key':
            webkey = v

    if not webkey:
        raise OSError("Not a websocket request")

    d = sha1(webkey)
    d.update(b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
    respkey = d.digest()
    respkey = b2a_base64(respkey)[:-1]

    sock.send(b"""\
HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: """)
    sock.send(respkey)
    sock.send("\r\n\r\n")
