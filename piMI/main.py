from gpio.led import initLED
from serial.read import startSerialThread
from web.webServer import connectToWireless, startServer

initLED()
startSerialThread()
connectToWireless()
startServer()
