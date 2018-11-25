import serial
ser = serial.Serial("/dev/ttyACM0", 19200)
apins = {}
dpins = {}
while True:
    line = str(ser.readline())[2:][:-5]
    print(line)
    line = line.split(":")
    pin = line[0]
    value = line[1]
    if pin[0] == 'A':
        pin = pin[1:]
        apins[pin] = int(value)
    else:
        dpins[pin] = int(value)
    print(apins)
    print(dpins)
