/*
Copyright (c) 2015, Collin Schupman (Future Citites Lab)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
*/

#include "FastLED.h"
#include "T3Mac.h"

const int NUM_LEDS = 49;
//const int NUM_LEDS_MIDDLE = 60;

const int DATA_PIN = 21;
//const int DATA_PIN_STRIP_2 = 7;
//const int DATA_PIN_STRIP_3 = 8;


//const int TOTAL_LEDS = 360;

CRGB leds[NUM_LEDS];

char in_data[3*NUM_LEDS];

char in_byte;

/*
Standard Arduino setup function.
Initiaizes serial port, clears LED data.

FastLED data is organized as such:
leds - Contains data for all strips
DATA_PIN_STRIP_1 -> Position 0 to NUM_LEDS_STRIP
DATA_PIN_STRIP_2 -> Position NUM_LEDS_STRIP  to 2*NUM_LEDS_STRIP
DATA_PIN_STRIP_3 -> Position 2*NUM_LEDS_STRIP to 2*NUM_LEDS_STRIP + NUM_LEDS_MIDDLE
*/
void setup() { 

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, 0, NUM_LEDS);
  //FastLED.addLeds<NEOPIXEL, DATA_PIN_STRIP_2>(leds, NUM_LEDS_STRIP, NUM_LEDS_STRIP);
  //FastLED.addLeds<NEOPIXEL, DATA_PIN_STRIP_3>(leds, 2*NUM_LEDS_STRIP, NUM_LEDS_MIDDLE);

  Serial.begin(115200);
  
  Serial.flush();
  
  for (int i = 0; i < 3 * NUM_LEDS; i++) {
    in_data[i] = 0;
  }
  
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Red;
  }

}
/*
wait for starting character:
'#' = Send this devices MAC address
'*' = Read in RGB data
'%' = Shut off the system  
*/
void loop() { 
  int startChar = Serial.read();
  if (startChar == '#') {
       Serial.write('a');
  } else if (startChar == '*') {
    int count = Serial.readBytes((char*)in_data, sizeof(in_data));
    if (count == sizeof(in_data)) {
      for (int i = 0; i < 3 * NUM_LEDS; i+=3) {
        leds[i/3].setRGB(in_data[i], in_data[i+1], in_data[i+2]);
      }
      FastLED.show();
    }
  } else if (startChar == '%') {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB::Black;
    }
    FastLED.show();
  }
}
