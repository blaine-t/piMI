# Original file:
# *****************************************************************************
# * | File        :   Pico ePaper 2.13 Landscape modification
# * | Author      :   Chris Truebe
# * | Function    :   Electronic paper driver
# * | Info        :   Runs Pico ePaper by Waveshare in Landscape mode.
# *----------------
# * | This version:   V1.0
# * | Date        :   2023-01-10
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

# Modification by Blaine Traudt to add async support and display computer stats

import utime
import framebuf
import ujson as json
from machine import Pin, SPI, Timer

lut_partial_landscape = [
    0x80, 0x60, 0x40, 0x00, 0x00, 0x00, 0x00,  # LUT0: BB:     VS 0 ~7
    0x10, 0x60, 0x80, 0x00, 0x00, 0x00, 0x00,  # LUT1: BW:     VS 0 ~7
    0x80, 0x60, 0x40, 0x00, 0x00, 0x00, 0x00,  # LUT2: WB:     VS 0 ~7
    0x10, 0x60, 0x80, 0x00, 0x00, 0x00, 0x00,  # LUT3: WW:     VS 0 ~7
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # LUT4: VCOM:   VS 0 ~7

    0x03, 0x03, 0x00, 0x00, 0x02,                       # TP0 A~D RP0
    0x09, 0x09, 0x00, 0x00, 0x02,                       # TP1 A~D RP1
    0x03, 0x03, 0x00, 0x00, 0x02,                       # TP2 A~D RP2
    0x00, 0x00, 0x00, 0x00, 0x00,                       # TP3 A~D RP3
    0x00, 0x00, 0x00, 0x00, 0x00,                       # TP4 A~D RP4
    0x00, 0x00, 0x00, 0x00, 0x00,                       # TP5 A~D RP5
    0x00, 0x00, 0x00, 0x00, 0x00,                       # TP6 A~D RP6
    0x22, 0x17, 0x41, 0x00, 0x32, 0x36
    # 0x15,0x41,0xA8,0x32,0x30,0x0A
]

EPD_WIDTH = 128
EPD_HEIGHT = 250

# E_Paper Control Pins
e_Paper_DC = 8  # Data / Command Control Pin
e_Paper_CS = 9  # LOW active
e_Paper_CLK = 10  # SCK
e_Paper_DIN = 11  # MOSI
e_Paper_RST = 12  # External reset (LOW Activce)
e_Paper_BUSY = 13  # Busy Status Output

RST_PIN = e_Paper_RST
DC_PIN = e_Paper_DC
CS_PIN = e_Paper_CS
BUSY_PIN = e_Paper_BUSY

FULL_UPDATE = 0
PART_UPDATE = 1


class EPD_2in13_V3_Landscape(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else:
            self.width = (EPD_WIDTH // 8) * 8 + 8

        self.height = EPD_HEIGHT

        self.full_lut = lut_partial_landscape
        self.spi = SPI(1)
        self.spi.init(baudrate=1000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    @staticmethod
    def digital_write(pin, value):
        pin.value(value)

    @staticmethod
    def digital_read(pin):
        return pin.value()

    @staticmethod
    def delay(delaytime):
        utime.sleep(delaytime)

    @staticmethod
    def delay_ms(delaytime):
        utime.sleep(delaytime / 1000.0)

    '''
    function : Write data to SPI
    parameter:
        data : data
    '''

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    '''
    function :Hardware reset
    parameter:
    '''

    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)

    '''
    function :send command
    parameter:
     command : Command register
    '''

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    '''
    function :send data
    parameter:
     data : Write data
    '''

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    '''
    function :Wait until the busy_pin goes LOW
    parameter:
    '''

    def ReadBusy(self):
        print('busy')
        while self.digital_read(self.busy_pin) == 1:  # 0: idle, 1: busy
            self.delay_ms(10)
        print('busy release')

    '''
    function : Turn On Display
    parameter:
    '''

    def TurnOnDisplay(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    '''
    function : Turn On Display Part
    parameter:
    '''

    def TurnOnDisplayPart(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0x0c)  # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    '''
    function : Set LUT
    parameter :
        lut : lut data
    '''

    def LUT(self, lut):
        self.send_command(0x32)
        for i in range(0, 70):
            self.send_data(lut[i])
        self.ReadBusy()

    '''
    function : Send the lut data and configuration
    parameter :
        lut : lut data
    '''

    def LUT_by_host(self, lut):
        self.LUT(lut)  # lut
        self.send_command(0x3F)
        self.send_data(lut[70])
        self.send_command(0x03)  # gate voltage
        self.send_data(lut[71])
        self.send_command(0x04)  # source voltage
        self.send_data(lut[72])  # VSH
        self.send_data(lut[73])  # VSH2
        self.send_data(lut[74])  # VSL
        self.send_command(0x2C)  # VCOM
        self.send_data(lut[75])

    '''
    function : Setting the display window
    parameter:
        Xstart : X-axis starting position
        Ystart : Y-axis starting position
        Xend : End position of X-axis
        Yend : End position of Y-axis
    '''

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart >> 3) & 0xFF)
        self.send_data((Xend >> 3) & 0xFF)

        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)

    '''
    function : Set Cursor
    parameter:
        Xstart : X-axis starting position
        Ystart : Y-axis starting position
    '''

    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)

    '''
    function : Initialize the e-Paper register
    parameter:
    '''

    def init(self) -> object:
        print('init')
        self.reset()
        self.delay_ms(100)

        self.ReadBusy()
        self.send_command(0x12)  # SWRESET
        self.ReadBusy()

        self.send_command(0x01)  # Driver output control
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x07)

        self.SetWindows(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x05)

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.send_command(0x18)  # Read built-in temperature sensor
        self.send_data(0x80)

        self.ReadBusy()
        self.LUT_by_host(self.full_lut)

    def Clear(self, color):
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(0xFF)
        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(0xFF)

        self.TurnOnDisplay()

    def display(self, image: object) -> object:
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplay()

    def Display_Base(self, image):
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.send_command(0x26)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplay()

    def display_Partial(self, image):
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
        self.digital_write(self.reset_pin, 1)

        self.LUT_by_host(self.full_lut)

        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.ReadBusy()

        self.SetWindows(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplayPart()

    def sleep(self):
        self.send_command(0x10)  # enter deep sleep
        self.send_data(0x03)
        self.delay_ms(100)
        # self.module_exit()


def timeout_sleep():
    epd = EPD_2in13_V3_Landscape()
    epd.init()
    epd.Clear(0xff)
    epd.delay_ms(2000)
    epd.sleep()


async def test():
    epd = EPD_2in13_V3_Landscape()
    epd.Clear(0xff)

    epd.fill(0xff)
    epd.text("Waveshare", 0, 10, 0x00)
    epd.text("ePaper-2.13_V3", 0, 20, 0x00)
    epd.text("Raspberry Pico", 0, 30, 0x00)
    epd.text("Hello World", 0, 40, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    epd.vline(5, 55, 60, 0x00)
    epd.vline(100, 55, 60, 0x00)
    epd.hline(5, 55, 95, 0x00)
    epd.hline(5, 115, 95, 0x00)
    epd.line(5, 55, 100, 115, 0x00)
    epd.line(100, 55, 5, 115, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    epd.rect(130, 10, 40, 80, 0x00)
    epd.fill_rect(190, 10, 40, 80, 0xff)
    epd.Display_Base(epd.buffer)
    epd.delay_ms(2000)

    epd.init()
    for i in range(0, 10):
        epd.fill_rect(175, 105, 10, 10, 0xff)
        epd.text(str(i), 177, 106, 0x00)
        epd.display_Partial(epd.buffer)

    print("sleep")
    epd.init()
    epd.Clear(0xff)
    epd.delay_ms(2000)
    epd.sleep()


async def displayStats():
    epd = EPD_2in13_V3_Landscape()
    while True:
        epd.Clear(0xff)
        epd.fill(0xff)
        # Box for stats
        epd.rect(15, 15, 101, 101, 0x00)
        # Top thickness
        #        X1  Y1  X2   Y2  Color
        epd.line(15, 14, 115, 14, 0x00)
        epd.line(15, 13, 115, 13, 0x00)
        epd.line(15, 12, 115, 12, 0x00)
        # Right side thickness
        #        X1   Y1  X2   Y2  Color
        epd.line(116, 15, 116, 115, 0x00)
        epd.line(117, 15, 117, 115, 0x00)
        epd.line(118, 15, 118, 115, 0x00)
        # Bottom thickness
        #        X1   Y1   X2  Y2  Color
        epd.line(115, 116, 15, 116, 0x00)
        epd.line(115, 117, 15, 117, 0x00)
        epd.line(115, 118, 15, 118, 0x00)
        # Left side thickness
        #        X1  Y1   X2  Y2  Color
        epd.line(14, 115, 14, 15, 0x00)
        epd.line(13, 115, 13, 15, 0x00)
        epd.line(12, 115, 12, 15, 0x00)

        # (Text is 8 pixels wide monospace)
        # Text stats            X   Y   Color
        epd.text("CPU:   100%", 21, 25, 0x00)
        epd.text("USED: 7000M", 21, 35, 0x00)
        epd.text("FREE: 7000M", 21, 45, 0x00)
        epd.text("CACHE: 700M", 21, 55, 0x00)
        epd.text("DOWN:  100M", 21, 65, 0x00)
        epd.text("UP:    100M", 21, 75, 0x00)
        epd.text("READ:  100M", 21, 85, 0x00)
        epd.text("WRITE: 100M", 21, 95, 0x00)

        # IP info
        epd.text("192.168.100.100", 125, 10, 0x00)

        # Current time
        epd.text("24:00", 165, 50, 0x00)

        # Uptime
        epd.text("Uptime:", 125, 80, 0x00)
        epd.text("999:12:12:12", 125, 90, 0x00)

        # Clients
        epd.text("Web Clients:100", 125, 110, 0x00)

        # Output data to display
        epd.display(epd.buffer)
        epd.delay(180)
