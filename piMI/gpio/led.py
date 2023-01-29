from machine import Pin
from time import sleep

def initLED():
    global pwr
    pwr = Pin(0, Pin.OUT)
    global rst
    rst = Pin(3, Pin.OUT)

def shortPress():
    pwr.value(1)
    sleep(1)
    pwr.value(0)

def longPress():
    pwr.value(1)
    sleep(10)
    pwr.value(0)

def resetPress():
    rst.value(1)
    sleep(1)
    rst.value(0)
