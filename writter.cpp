#include <Arduino.h>

void setup() {
	Serial.begin(9600);
	init();
}

int main() {
	setup();
	while (true) {
		Serial.println("1 -- info");
	}
	return 0;
}
