/*
Problems/TODO: 
- Still no solution for > 10
- Need to take in Color
- Need to take in Speed
*/

#include <SmartMatrix_32x32.h>
#include "T3Mac.h"

#define TEXT_HEIGHT 11
#define TEXT_WIDTH 9

SmartMatrix matrix;

const int defaultBrightness = 1000;  
const rgb24 red = {0x20, 0, 0};
const rgb24 black = {0, 0, 0};
const int ledPin = 13;

String inputString = "";

int current_word_x_pos = 0;

boolean stringComplete = false;

int speed_delay = 40;

rgb24 currentColor = {0x20,0,0};

// DEBUG
boolean debug = false;
String debug_string = "TESTING...";

void setup() {
  Serial.begin(115200);
  Serial.flush();
  pinMode(ledPin, OUTPUT);
  
  matrix.begin();
  matrix.setBrightness(defaultBrightness);
  matrix.setFont(font8x13);
  
  inputString.reserve(4000);
  current_word_x_pos = -(debug_string.length()*TEXT_WIDTH);

}

void loop() {
  matrix.fillScreen(black);
  if (debug) {
    if (current_word_x_pos == 128 + 1) {
      current_word_x_pos = -(debug_string.length()*TEXT_WIDTH);
    } else {
      matrix.drawString(current_word_x_pos, TEXT_HEIGHT, {0xFF,0,0xFF}, debug_string.c_str());
      current_word_x_pos++;
      matrix.swapBuffers(true);
      delay(speed_delay);
    }
    
  } else {
    if (Serial.available() > 0) {
      if (Serial.peek() == '#') {
        Serial.read();
        read_mac();
        print_mac();
      } else {
        inputString = "";
        currentColor.red = Serial.read(); 
        currentColor.green = Serial.read(); 
        currentColor.blue = Serial.read();
        speed_delay = (int)Serial.read();
        while (Serial.available() > 0) {
          char inChar = (char)Serial.read(); 
          inputString += inChar;
          if (inChar == '\n') {
            stringComplete = true;
            current_word_x_pos = -(inputString.length()*TEXT_WIDTH);
          } 
        }
      }
    }
   
    if (stringComplete) {
      if (current_word_x_pos == 128 + 1) {
        current_word_x_pos = 0;
        stringComplete = false;
        Serial.write("Done");
      } else {
        matrix.drawString(current_word_x_pos, TEXT_HEIGHT, currentColor, inputString.c_str());
        current_word_x_pos++;
        matrix.swapBuffers(true);
        delay(speed_delay);
      }
    }
  }
}
