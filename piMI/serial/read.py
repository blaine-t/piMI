#
# USB serial communication for the Raspberry Pi Pico (RD2040) using the second RD2040
# thread/processor (inspiration from Dorian Wiskow - Janaury 2021) https://forums.raspberrypi.com/viewtopic.php?t=302889 
#
from sys import stdin
from _thread import start_new_thread

#
# listen() function to execute in parallel on second Pico RD2040 thread/processor
#
def listen():
    data = ""
    reading = False
    cpuReading = True
    previousByte = ""
    digits = ""
    while True:
        byte = stdin.read(1)
        if(reading):
            if(byte == "\n"):
                # Fix lost 0
                data += digits
                if (digits):
                    data += ","
                data = data.replace(" ", "") # Remove unnecessary spaces
                data = data[:-1] # Remove trailing comma
                data += "]" # Add closing bracket for list
                if (data[1] != ","):
                    print(data)
                reading = False
                cpuReading = True
            elif(byte == "d"):
                reading = False
            elif(byte == " " and cpuReading):
                if (previousByte.isdigit()):
                    data += ","
            elif(byte == "|"):
                cpuReading = False
                if(data[-1] != ","): # Make sure no duped commas
                    data += ","
            elif(not cpuReading):
                if(byte.isdigit() or byte == "."):
                    digits += byte
                elif(byte == "T"):
                    if ("." in digits):
                        digits = int(float(digits) * 1000000000000)
                    else:
                        digits = int(digits) * 1000000000000
                    data += str(digits)
                    data += ","
                    digits = ""
                elif(byte == "G"):
                    if ("." in digits):
                        digits = int(float(digits) * 1000000000)
                    else:
                        digits = int(digits) * 1000000000
                    data += str(digits)
                    data += ","
                    digits = ""
                elif(byte == "M"):
                    if ("." in digits):
                        digits = int(float(digits) * 1000000)
                    else:
                        digits = int(digits) * 1000000
                    data += str(digits)
                    data += ","
                    digits = ""
                elif(byte == "k"):
                    if ("." in digits):
                        digits = int(float(digits) * 1000)
                    else:
                        digits = int(digits) * 1000
                    data += str(digits)
                    data += ","
                    digits = ""
                elif(byte == "b"):
                    data += digits
                    data += ","
                    digits = ""
                elif(byte == " " and digits == "0"):
                    data += "0,"
                    digits = ""
                else:
                    data += byte
            else:
                data += byte
                
                
        elif(byte == "|"):
            data = "["
            reading = True
            
        previousByte = byte
#
# instantiate second 'background' thread on RD2040 dual processor to monitor and buffer
# incomming data from 'stdin' over USB serial port using ‘listen‘ function (above)
#
def startSerialThread():
    start_new_thread(listen, ())