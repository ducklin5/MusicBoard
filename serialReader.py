import serial


def run(serialPort, pins, debug=False):
    ser = serial.Serial(serialPort, 19200)

    while True:
        line = str(ser.readline())[2:][:-5]
        print(line)
        line = line.split(":")
        pin = line[0]
        value = line[1]
        pins[pin] = int(value)
        if debug:
            print(pins, '\n')


if __name__ == "__main__":
    inputs = {}
    run("/dev/ttyACM0", inputs, True)
