from piMI.serial.read import startSerialThread
from piMI.web.webServer import connectToWireless, startServer

startSerialThread()
connectToWireless()
startServer()