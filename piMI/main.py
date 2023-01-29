# Async code inspired by Digikey youtube video: https://youtu.be/5VLvmA__2v0 and post: https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c
from uasyncio import create_task, sleep, run
# Allow for async serial listening
import serial
# TODO: Temp for debugging
import gpio

async def main():
    create_task(gpio.shortPress())
    create_task(serial.listen())
    while True:
        await sleep(5)

run(main())
