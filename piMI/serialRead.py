# This code is inspired by jdts' code from December 2019 on the Micropython forms here: https://forum.micropython.org/viewtopic.php?t=7325

# For reading from the serial bus
from sys import stdin
from uselect import poll, POLLIN
# For async sleep so GPIO is non-blocking
from uasyncio import sleep

# Serial read requirements
spoll = poll()
spoll.register(stdin, POLLIN)


previousData = [0]
bootEpoch = 0


def getData():
    return previousData, bootEpoch


async def listen(server):
    # Create a variable to hold until buffer read
    data = ""
    byte = "\n"
    while True:
        # If serial data is ready to be read
        if spoll.poll(0):
            # Read one byte at a time and append it to data
            byte = stdin.read(1)
            data += byte
        # If no serial data ready to read
        elif byte != "\n":
            # Wait 200ms for computer's serial write to finish
            await sleep(0.2)
        else:
            # If there is data in buffer
            if data != "":
                # Send it to websocket
                server.process_all(data)

                # Update variables
                # If it's been more than 60 seconds since last serial update
                # then reset bootEpoch or if it's first run (since it's 0)
                if previousData[-1] + 12 > list(data)[-1]:
                    global bootEpoch
                    bootEpoch = list(data)[-1]

                global previousData
                previousData = list(data)
                # Clear buffer
                data = ""
            # Async wait half a second to allow other processes to run
            await sleep(0.5)
