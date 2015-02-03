import processing.serial.*;

Serial matrix;       
Serial leds;       

void setup() {
  println(Serial.list());
  leds = new Serial(this, Serial.list()[7], 9600);
}

void draw() {
  for (int i = 0; i < 65; i++) {
    leds.write('a');
    //leds.write(0);
    //leds.write(65);
    //leds.write(0);
  }
}
