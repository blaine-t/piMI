# For GPIO access
from machine import Pin
# For async sleep so GPIO is non-blocking
from uasyncio import sleep

# Initialize power LED on pin 0
pwrPin = Pin("LED", Pin.OUT) # TODO: "LED" temp for debugging
pwrPin.value(0)
    
# Initialize reset LED on pin 3
rstPin = Pin(3, Pin.OUT)
rstPin.value(0)

# "Press" power button for 1 second
async def shortPress():
    # If statement to ensure that shortPress() doesn't cut longPress() short
    if pwrPin.value() == 0:
        pwrPin.value(1)
        await sleep(1)
        pwrPin.value(0)

# "Hold" power button for 10 seconds
async def longPress():
    pwrPin.value(1)
    await sleep(10)
    pwrPin.value(0)
    
# "Press" reset button for 1 second
async def resetPress():
    rstPin.value(1)
    await sleep(1)
    pwrPin.value(0)
