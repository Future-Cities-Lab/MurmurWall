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

#include <T3Mac.h>
#include <SmartMatrix_32x32.h>
#include <vector>

// The height of each LED matrix
const int MATRIX_HEIGHT = 32;

// The width of each LED matrix
const int MATRIX_WIDTH = 128;

// Text height (pixels) 
const int TEXT_HEIGHT = 11;

// Text width (pixels)
const int  TEXT_WIDTH = 9;

const int MIN_VELOCITY = 1;
const int  MAX_VELOCITY = 3;

const int DELAY_TIME = 70;

// The width of each LED matrix
SmartMatrix matrix;
const int led_pin = 13;

fontChoices fonts[] = {font8x13, font6x10, font5x7, font3x5};
int font_widths[] = {9, 7, 6, 4};

// ?
String input_string = "";

/*
The total byte data:
3 - Color bytes r,g,b
1 - 
140 - Characters of the word
1 - \n 
*/
const int total_data = 3 + 1 + 140 + 1;

// A buffer to hold incoming byte stream
char in_data[total_data];

int prev = 0;
int top_prev_length = 0;
int bottom_prev_length = 0;

/*
A struct representing one Packet in Murmurwall
text - A string of text to be displayed
x_position -
y_position -
color -
font -
width - 
*/
struct Packet
{
    String text;
    int x_position;
    int y_position;
    rgb24 color;
    fontChoices font;
    int width;
};

// A vector holding each packet being displayed
std::vector<struct Packet> packets;

// A vector holding each word marked for removal
std::vector<int> to_erase;


void draw_packet(struct Packet *packet, int pos);


/*
Standard Arduino setup function.
Initiaizes serial port, data pin, matrix and input buffer
*/
void setup() {
  Serial.begin(115200);
  Serial.flush();

  pinMode(led_pin, OUTPUT);
  matrix.begin();
  matrix.setBrightness(255);
  
  input_string.reserve(4000);
}

/*
Standard Arduino setup function.
Initiaizes serial port, data pin, matrix and input buffer
*/
void loop() {
  
  matrix.fillScreen({0,0,0});
  
  int start_char = Serial.read();

  if (start_char == '#') {
    Serial.write('g');
  } else if (start_char == '*') {
    int count = Serial.readBytes((char*)in_data, sizeof(in_data));
    if (count == sizeof(in_data)) {
      load_new_packet();
    } else {
      Serial.write("FAIL");
    }
  } else if (start_char == '&') {
    packets.clear();
  } 
  for (int i = 0; i < packets.size(); i++) {
    draw_packet(&packets[i], i); 
  }
  for (int i = 0; i < to_erase.size(); i++) {
    Serial.write('*');
    String to_send = packets[to_erase[i]].text;
    int text_length = to_send.length();
    for (int i = 0; i < 100 - text_length; i++) {
      to_send += '\n';
    }
    Serial.write(to_send.c_str());
    packets.erase(packets.begin() + to_erase[i]);
  }
  to_erase.clear();
  
  matrix.swapBuffers(true);
  delay(DELAY_TIME);
  
}

void load_new_packet() {
  input_string = "";
  rgb24 word_color = {in_data[0], in_data[1], in_data[2]};
  int speed_delay = (int)in_data[3];
  int pos = 4;
  while (in_data[pos] != '\n') {
    input_string += in_data[pos];
    pos++;
  }
  int font_pos = 0;
  if (packets.size() >= 1) {
    font_pos = map(packets.size(), 1, 5, 1, 3);
  }
  int start_height = TEXT_HEIGHT;
  int height_offset = 10*prev;;
  if (packets.size() == 0 || prev == 0) {
    prev = 1;
  } else if (prev == 1) {
    prev = -1;  
  } else if (prev == -1) {
    prev = 0;
  }
  int start_x_pos = -(input_string.length()*font_widths[font_pos]);
  packets.push_back({input_string, start_x_pos, start_height + height_offset, word_color, fonts[font_pos], font_widths[font_pos]});
}

void draw_packet(struct Packet *packet, int pos) {
  String current_word = packet->text;
  int num_chars = current_word.length();
  int j = 0;
  matrix.setFont(packet->font);
  for (int i = packet->x_position; i < packet->x_position + (packet->width*num_chars); i += packet->width) {
    matrix.drawChar(i, packet->y_position, packet->color, current_word.charAt(j));
    j++;
  }
  if (packet->x_position < (MATRIX_WIDTH/2) - (num_chars/2)) {
    int vel = 4 - map(packet->x_position, -(num_chars*packet->width), (MATRIX_WIDTH/2 - 1) -((num_chars*packet->width)/2), MIN_VELOCITY, MAX_VELOCITY);
    if (vel == 0) {
      vel++;
    }
    packet->x_position += vel;
  } else {
    int vel = map(packet->x_position, (MATRIX_WIDTH/2) -((num_chars*packet->width)/2), MATRIX_WIDTH, MIN_VELOCITY, MAX_VELOCITY);
    if (vel == 0) {
      vel++;
    }
    packet->x_position += vel;
  }
  if (packet->x_position >= MATRIX_WIDTH) {
    to_erase.push_back(pos);
  } 
}
