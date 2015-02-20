#include <SmartMatrix_32x128.h>

SmartMatrix matrix;

const int defaultBrightness = 1000;  
const rgb24 red = {0x20, 0, 0};
const rgb24 black = {0, 0, 0};
const int ledPin = 13;

const int string_x_pos_start = -50;
int string_x_pos;

String words[3] = {"FUTURE","CITIES","LABORA"};

int current_word_pos = 0;
char current_word[7] = "FUTURE";

byte inByte;
int count = 0;

boolean ending = false;

rgb24 colors[3] = {{0xFF,0,0xFF},{0xFF,0xFF,0xFF},{0,0,0xFF}};

void setup() {
  Serial.begin(57600);
  inByte = byte(1);
  pinMode(ledPin, OUTPUT);
  matrix.begin();
  matrix.setBrightness(defaultBrightness);
  matrix.setFont(font8x13);
  string_x_pos = string_x_pos_start;
}

void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();
  }
  if (inByte == byte(0)) {
    matrix.fillScreen(black);
    words[current_word_pos].toCharArray(current_word,7);
    matrix.drawString(string_x_pos, matrix.getScreenHeight() / 2, colors[current_word_pos], current_word);
    if (count % 2 == 0) {
      string_x_pos+=1;
    }
    matrix.swapBuffers(true);
    count++;
    ending = true;
  } else {
    if (ending) {
      current_word_pos++;
      current_word_pos %= 3;
      ending = false;
    }
    
    count = 0;
    string_x_pos = string_x_pos_start;
    matrix.fillScreen(black);
    matrix.swapBuffers(true);
  }
}
