# ---------------------------------------------------
#    Name: Azeez  Abass
#    ID: 1542780
#    Name: Matthew Braun
#    ID: 1497171
#    CMPUT 274 EA1, Fall  2018
#    Project: ZMat 2000 (SerialReader)
# ---------------------------------------------------

# import the pySerial module
import serial


def run(serialPort, pins, debug=False):
    """
    Reads the given Serial Port and mirrors the pin states to the dictionary 'pins'
    Inputs:
        serialPort (string): path to the input serialPort 
        pins (dictionary): The dictionary to be updated with Arduino pin states
        debug (bool): run the funcion in debug mode will print each time  line is recieved
    Refrences:
        https://stackoverflow.com/questions/16077912/python-serial-how-to-use-the-read-or-readline-function-to-read-more-than-1-char
    """
    # open the port for reading
    ser = serial.Serial(serialPort, 19200)

    while True:
        # read the line and remove unnecessary leading and trailing chars
        line = str(ser.readline())[2:][:-5]
        # split the line to get key and value for the dictionary
        line = line.split(":")
        pin = line[0]
        value = line[1]
        # append pin and value to the dictionary
        pins[pin] = int(value)
        if debug:
            print(pins, '\n')


if __name__ == "__main__":
    inputs = {}
    run("/dev/ttyACM0", inputs, True)
