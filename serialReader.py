import serial
ser = serial.Serial("COM11", 9600)
while True:
     cc=str(ser.readline())
     print(cc[2:][:-5])
