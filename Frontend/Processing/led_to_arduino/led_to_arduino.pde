import processing.serial.*;


private int particlePosition;

private int NUM_PIXELS;

private byte[] ledState;

private Serial ledPort;   
private Serial matrixPort;   


private int timeDelay;

private int lastTime;

private int rgb_state = 0;


void setup() {
  frameRate(8);
  particlePosition = 0;
  NUM_PIXELS = 57;
  ledState = new byte[3*NUM_PIXELS];
  
  timeDelay = 6500;
  
  //initalize to a color
  for (int i = 0; i < ledState.length; i+=3) {
    color rgb = color(0,0,0);
    byte red = byte(red(rgb));
    byte green = byte(green(rgb));
    byte blue = byte(blue(rgb));
    ledState[i] = red;
    ledState[i+1] = green;
    ledState[i+2] = blue;
  } 
  
  println(Serial.list());
  ledPort = new Serial(this, Serial.list()[7], 115200);
  matrixPort = new Serial(this, Serial.list()[6], 57600);

}

void draw() {
  for (int i = 0; i < ledState.length; i+=3) {
    color rgb = color(0,0,0);
    byte red = byte(red(rgb)); 
    byte green = byte(green(rgb));
    byte blue = byte(blue(rgb));
    ledState[i] = red;
    ledState[i+1] = green;
    ledState[i+2] =   blue;
  }

  if (particlePosition == 18 && millis() - lastTime <= timeDelay) {
    matrixPort.write(byte(0));
  } else {
    matrixPort.write(byte(1));
    
    if (millis() - lastTime > timeDelay) {
      particlePosition = 34;
    } else {
      particlePosition++;
      if (particlePosition == 57) {
        particlePosition = 0;
        rgb_state++;
        rgb_state%=3;
      }
    }
   
    lastTime = millis();
    println(rgb_state);
    if (rgb_state == 0) {
      
      ledState[particlePosition*3] = byte(255);
      ledState[particlePosition*3 + 1] = byte(0);
      ledState[particlePosition*3 + 2] = byte(255);
      
      if ((particlePosition*3 + 0) - (3*3) > 0) ledState[(particlePosition*3 + 0) - 9] = byte(105); 
      if ((particlePosition*3 + 0) - (3*2) > 0) ledState[(particlePosition*3 + 0) - 6] = byte(155); 
      if ((particlePosition*3 + 0) - (3*1) > 0) ledState[(particlePosition*3 + 0) - 3] = byte(205); 
      
      if ((particlePosition*3 + 1) - (3*3) > 0) ledState[(particlePosition*3 + 1) - 9] = byte(0); 
      if ((particlePosition*3 + 1) - (3*2) > 0) ledState[(particlePosition*3 + 1) - 6] = byte(0); 
      if ((particlePosition*3 + 1) - (3*1) > 0) ledState[(particlePosition*3 + 1) - 3] = byte(0); 
      
      if ((particlePosition*3 + 2) - (3*3) > 0) ledState[(particlePosition*3 + 2) - 9] = byte(105); 
      if ((particlePosition*3 + 2) - (3*2) > 0) ledState[(particlePosition*3 + 2) - 6] = byte(155); 
      if ((particlePosition*3 + 2) - (3*1) > 0) ledState[(particlePosition*3 + 2) - 3] = byte(205);       

      if ((particlePosition*3 + 0) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 3] = byte(205); 
      if ((particlePosition*3 + 0) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 6] = byte(155); 
      if ((particlePosition*3 + 0) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 9] = byte(105); 
      
      if ((particlePosition*3 + 1) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 3] = byte(0); 
      if ((particlePosition*3 + 1) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 6] = byte(0); 
      if ((particlePosition*3 + 1) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 9] = byte(0); 

      if ((particlePosition*3 + 2) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 3] = byte(205); 
      if ((particlePosition*3 + 2) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 6] = byte(155); 
      if ((particlePosition*3 + 2) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 9] = byte(105); 
      
    } else if (rgb_state == 1) {
      ledState[particlePosition*3] = byte(255);
      ledState[particlePosition*3 + 1] = byte(255);
      ledState[particlePosition*3 + 2] = byte(255);

      if ((particlePosition*3 + 0) - (3*3) > 0) ledState[(particlePosition*3 + 0) - 9] = byte(105); 
      if ((particlePosition*3 + 0) - (3*2) > 0) ledState[(particlePosition*3 + 0) - 6] = byte(155); 
      if ((particlePosition*3 + 0) - (3*1) > 0) ledState[(particlePosition*3 + 0) - 3] = byte(205); 
      
      if ((particlePosition*3 + 1) - (3*3) > 0) ledState[(particlePosition*3 + 1) - 9] = byte(105); 
      if ((particlePosition*3 + 1) - (3*2) > 0) ledState[(particlePosition*3 + 1) - 6] = byte(155); 
      if ((particlePosition*3 + 1) - (3*1) > 0) ledState[(particlePosition*3 + 1) - 3] = byte(205); 
      
      if ((particlePosition*3 + 2) - (3*3) > 0) ledState[(particlePosition*3 + 2) - 9] = byte(105); 
      if ((particlePosition*3 + 2) - (3*2) > 0) ledState[(particlePosition*3 + 2) - 6] = byte(155); 
      if ((particlePosition*3 + 2) - (3*1) > 0) ledState[(particlePosition*3 + 2) - 3] = byte(205);       

      if ((particlePosition*3 + 0) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 3] = byte(205); 
      if ((particlePosition*3 + 0) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 6] = byte(155); 
      if ((particlePosition*3 + 0) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 9] = byte(105); 
      
      if ((particlePosition*3 + 1) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 3] = byte(205); 
      if ((particlePosition*3 + 1) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 6] = byte(155); 
      if ((particlePosition*3 + 1) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 9] = byte(105); 

      if ((particlePosition*3 + 2) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 3] = byte(205); 
      if ((particlePosition*3 + 2) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 6] = byte(155); 
      if ((particlePosition*3 + 2) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 9] = byte(105);     
      
    } else {
      ledState[particlePosition*3] = byte(0);
      ledState[particlePosition*3 + 1] = byte(0);
      ledState[particlePosition*3 + 2] = byte(255);
      
      if ((particlePosition*3 + 0) - (3*3) > 0) ledState[(particlePosition*3 + 0) - 9] = byte(0); 
      if ((particlePosition*3 + 0) - (3*2) > 0) ledState[(particlePosition*3 + 0) - 6] = byte(0); 
      if ((particlePosition*3 + 0) - (3*1) > 0) ledState[(particlePosition*3 + 0) - 3] = byte(0); 
      
      if ((particlePosition*3 + 1) - (3*3) > 0) ledState[(particlePosition*3 + 1) - 9] = byte(0); 
      if ((particlePosition*3 + 1) - (3*2) > 0) ledState[(particlePosition*3 + 1) - 6] = byte(0); 
      if ((particlePosition*3 + 1) - (3*1) > 0) ledState[(particlePosition*3 + 1) - 3] = byte(0); 
      
      if ((particlePosition*3 + 2) - (3*3) > 0) ledState[(particlePosition*3 + 2) - 9] = byte(105); 
      if ((particlePosition*3 + 2) - (3*2) > 0) ledState[(particlePosition*3 + 2) - 6] = byte(155); 
      if ((particlePosition*3 + 2) - (3*1) > 0) ledState[(particlePosition*3 + 2) - 3] = byte(205);       

      if ((particlePosition*3 + 0) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 3] = byte(0); 
      if ((particlePosition*3 + 0) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 6] = byte(0); 
      if ((particlePosition*3 + 0) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 0) + 9] = byte(0); 
      
      if ((particlePosition*3 + 1) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 3] = byte(0); 
      if ((particlePosition*3 + 1) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 6] = byte(0); 
      if ((particlePosition*3 + 1) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 1) + 9] = byte(0); 

      if ((particlePosition*3 + 2) + (3*1) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 3] = byte(205); 
      if ((particlePosition*3 + 2) + (3*2) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 6] = byte(155); 
      if ((particlePosition*3 + 2) + (3*3) < 3*NUM_PIXELS) ledState[(particlePosition*3 + 2) + 9] = byte(105);
    }
 
  }

  ledPort.write(ledState);
 
}
