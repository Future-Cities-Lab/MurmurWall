#include <SmartMatrix_32x128.h>
#include "T3Mac.h"

SmartMatrix matrix;

const int defaultBrightness = 1000;  
const rgb24 red = {0x20, 0, 0};
const rgb24 black = {0, 0, 0};
const int ledPin = 13;

String inputString = "";

int current_word_x_pos = 0;

boolean stringComplete = false;

void setup() {
  Serial.begin(115200);
  Serial.flush();
  pinMode(ledPin, OUTPUT);
  
  matrix.begin();
  matrix.setBrightness(defaultBrightness);
  matrix.setFont(font8x13);
  
  inputString.reserve(4000);
}

void loop() {
  matrix.fillScreen(black);
  if (Serial.available() > 0) {
    if (Serial.peek() == '#') {
      Serial.read();
      read_mac();
      print_mac();
    } else {
      inputString = "";
      while (Serial.available() > 0) {
        char inChar = (char)Serial.read(); 
        inputString += inChar;
        if (inChar == '\n') {
          stringComplete = true;
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
      matrix.drawString(current_word_x_pos, matrix.getScreenHeight() / 2, {0xFF,0,0xFF}, inputString.c_str());
      current_word_x_pos++;
      matrix.swapBuffers(true);
    }
  }
}
