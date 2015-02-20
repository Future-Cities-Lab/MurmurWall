#include "FastLED.h"
#include "T3Mac.h"

#define NUM_LEDS 57
#define NUM_LEDS_BACK 76

#define DATA_PIN 6
#define DATA_PIN_BACK 7

CRGB led_state[NUM_LEDS];
CRGB led_state_back[NUM_LEDS_BACK];

char in_data[3*NUM_LEDS];
char in_byte;

void setup() { 
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(led_state, NUM_LEDS);
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN_BACK>(led_state_back, NUM_LEDS_BACK);

  Serial.begin(115200);
  
  Serial.flush();
  
  for (int i = 0; i < 3 * NUM_LEDS; i++) {
    in_data[i] = 200;
  }
  
  for (int i = 0; i < NUM_LEDS; i++) {
    led_state[i] = CRGB::Blue;
  }
  for (int i = 0; i < NUM_LEDS_BACK; i++) {
    led_state_back[i] = CRGB::Red;
  }
}

void loop() { 
  if (Serial.available() > 0) {
    if (Serial.peek() == '#') {
      Serial.read();
      read_mac();
      print_mac();
    } else {
      int got = Serial.readBytes(in_data, 3*NUM_LEDS);
      for (int i = 0; i < 3 * NUM_LEDS; i+=3) {
        led_state[i/3].setRGB(in_data[i], in_data[i+1], in_data[i+2]);
      }
      for (int i = 0; i < NUM_LEDS_BACK; i++) {
        led_state_back[i] = CRGB::Red;
      }      
    }
  } else {
  
  }

 // else {
//    for (int i = 0; i < NUM_LEDS_BACK; i++) {
//      led_state_back[i] = CRGB::Red;
//    }
//    for (int i = 0; i < NUM_LEDS; i++) {
//      led_state[i] = CRGB::White;
//    }    
  //}
  FastLED.show();
}
