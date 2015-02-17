#include "FastLED.h"

#define NUM_LEDS 57
#define DATA_PIN 6

CRGB led_state[NUM_LEDS];
byte in_data[3*NUM_PIXELS];

byte inByte;
int index = 0;

void setup() { 
	Serial.begin(9600);
	FastLED.addLeds<NEOPIXEL, DATA_PIN>(led_state, NUM_LEDS);
	for (int i = 0; i < 3 * NUM_PIXELS; i++) {
    	in_data[i] = 200;
	}
}

void loop() { 
	while (index < (3*NUM_PIXELS)) {
		if (Serial.available() > 0) {
			inByte = Serial.read();
			inData[index] = inByte;
			index++;  
		}
	}
	index = 0;
	for (int i = 0; i < 3*NUM_PIXELS; i+=3) {
		leds[i/3].setRGB(inData[i],inData[i+1],inData[i+2]);
	}
	FastLED.show();
}