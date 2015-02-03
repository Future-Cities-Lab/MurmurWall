#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

#include "FastLED.h"


#define PIN 6

#define NUM_PIXELS 57

//Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

CRGB leds[NUM_PIXELS];


int delayval = 500; // delay for half a second

byte inData[3*NUM_PIXELS];

byte inByte;
int index = 0;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 3*NUM_PIXELS; i++) {
    inData[i] = 200;
  }
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_PIXELS);
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
