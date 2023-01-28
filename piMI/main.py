from serial.read import startSerialThread
from web.webServer import connectToWireless, startServer

startSerialThread()
connectToWireless()
startServer()
