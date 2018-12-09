// ---------------------------------------------------
//    Name: Azeez  Abass
//    ID: 1542780
//    Name: Matthew Braun
//    ID: 
//    CMPUT 274 EA1, Fall  2018
//    Project: ZMat 2000 (SerialWriter)
// ---------------------------------------------------

#include <Arduino.h>
// State digital and analog pins to be used
// Initialize all variable
int dPins[] = {2,3,4,5,6,7,8,9,10,11,12,13,22,23,25};
const int dPinCount = sizeof(dPins)/sizeof(dPins[0]);
int dpinStates[dPinCount];

int aPins[] = {0,14,15};
const int aPinCount = sizeof(aPins)/sizeof(aPins[0]);
int apinStates[aPinCount];



int intRound(int num, int factor){
    /**
    * Quick round function for analog smoothing
    * Inputs:
    *   num (int): number to round
    *   factor (int): factor to round by
    **/
    int result = num + factor/2;
    result -= result % factor;
    return result;
}

void init_aPins(){
    // Initializes Stated Analog pins
    for (int i = 0; i < aPinCount; i++) {
        int pin = aPins[i];
        pinMode(pin, INPUT);
    }
}

void init_dPins(){
    // Initializes Stated Digital pins
    for (int i = 0; i < dPinCount; i++) {
        int pin = dPins[i];
        pinMode(pin, INPUT);
        digitalWrite(pin, HIGH);
    }
}

void setup() {
    // Initialize the arduino, analog pins and digital pins
    init();
    Serial.begin(19200);
    init_aPins(); init_dPins(); 
}



void update_aPins(){
    // print the analog pin and value to serial if its has changed
    for (int i = 0; i < aPinCount; i++) {
        int pin = aPins[i];
        int newVal = intRound(analogRead(pin), 500);

        if (newVal != apinStates[i]) {
            Serial.print("A");
            Serial.print(pin);
            Serial.print(":");
            Serial.println(newVal);
            apinStates[i] = newVal;
        }
    }
}



void update_dPins(){
    // print the digital pin and value to serial if its has changed
    for (int i = 0; i < dPinCount; i++) {
        int pin = dPins[i];
        int newVal = not digitalRead(pin);

        if (newVal != dpinStates[i]) {
            Serial.print(pin);
            Serial.print(":");
            Serial.println(newVal);
            dpinStates[i] = newVal;
        }
    }
}



int main() {
    setup();
    while (true) {
        // update all digital pins
        update_aPins(); update_dPins(); 
    }
    return 0;
}
