import serial
ser = serial.Serial("/dev/ttyACM0", 19200)

while True:
    cc = str(ser.readline())
    print(cc[2:][:-5])

pins = {}
while True:
    line = str(ser.readline())[2:][:-5]
    print(line)
    line = line.split(":")
    pin = line[0]
    value = line[1]
    pins[pin] = int(value)
    print(pins)
