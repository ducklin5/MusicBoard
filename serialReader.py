import serial
ser = serial.Serial("/dev/ttyACM0", 19200)
pins = {}
while True:
    line = str(ser.readline())[2:][:-5]
    print(line)
    line = line.split(":")
    pin = line[0]
    value = line[1]
    pins[pin] = int(value)
    print(pins)
