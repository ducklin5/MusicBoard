#include <Arduino.h>
int dPins[] = {8,9,10};
const int dPinCount = sizeof(dPins)/sizeof(dPins[0]);
int dpinStates[dPinCount];

int aPins[] = {8,9};
const int aPinCount = sizeof(aPins)/sizeof(aPins[0]);
int apinStates[aPinCount];

void init_aPins(){
    for (int i = 0; i < aPinCount; i++) {
        int pin = aPins[i];
        pinMode(pin, INPUT);
    }
}

// stackoverflow.com/questions/29557459/
int intRound(int num, int factor){
    int result = num + factor/2;
    result -= result % factor;
    return result;
}

void update_aPins(){
    for (int i = 0; i < aPinCount; i++) {
        int pin = aPins[i];
        int newVal = intRound(analogRead(pin), 25);

        if (newVal != apinStates[i]) {
            Serial.print("A");
            Serial.print(pin);
            Serial.print(":");
            Serial.println(newVal);
            apinStates[i] = newVal;
        }
    }
}

void init_dPins(){
    for (int i = 0; i < dPinCount; i++) {
        int pin = dPins[i];
        pinMode(pin, INPUT);
        digitalWrite(pin, HIGH);
    }
}

void update_dPins(){
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

void setup() {
    init();
    Serial.begin(19200);
    init_aPins(); init_dPins(); 
}

int main() {
    setup();
    while (true) {
        // update all digital pins
        update_aPins(); update_dPins(); 
    }
    return 0;
}
