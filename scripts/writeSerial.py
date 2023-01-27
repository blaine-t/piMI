import serial

#init serial port and bound
# bound rate on two ports must be the same
ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.portstr)

#send data via serial port
ser.write("012345688902341")
ser.close()
