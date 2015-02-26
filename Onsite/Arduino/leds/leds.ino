#include "FastLED.h"
#include "T3Mac.h"

#define NUM_LEDS_STRIP 150
#define NUM_LEDS_MIDDLE 60


#define DATA_PIN_STRIP_1 6
#define DATA_PIN_STRIP_2 7
#define DATA_PIN_STRIP_3 8


#define TOTAL_LEDS 360

CRGB leds[TOTAL_LEDS];

char in_data[3*TOTAL_LEDS];


char in_byte;

void setup() { 

  FastLED.addLeds<NEOPIXEL, DATA_PIN_STRIP_1>(leds, 0, NUM_LEDS_STRIP);
  FastLED.addLeds<NEOPIXEL, DATA_PIN_STRIP_2>(leds, NUM_LEDS_STRIP, NUM_LEDS_STRIP);
  FastLED.addLeds<NEOPIXEL, DATA_PIN_STRIP_3>(leds, 2*NUM_LEDS_STRIP, NUM_LEDS_MIDDLE);

  Serial.begin(115200);
  
  Serial.flush();
  
  for (int i = 0; i < 3 * TOTAL_LEDS; i++) {
    in_data[i] = 0;
  }
  
  for (int i = 0; i < TOTAL_LEDS; i++) {
    leds[i] = CRGB::Red;
  }

}

void loop() { 
  if (Serial.available() > 0) {
    if (Serial.peek() == '#') {
      Serial.read();
      read_mac();
      print_mac();
    } else {
      int got = Serial.readBytes(in_data, 3*TOTAL_LEDS);
      for (int i = 0; i < 3 * TOTAL_LEDS; i+=3) {
        leds[i/3].setRGB(in_data[i], in_data[i+1], in_data[i+2]);
      }
    }
  }
  FastLED.show();
}
