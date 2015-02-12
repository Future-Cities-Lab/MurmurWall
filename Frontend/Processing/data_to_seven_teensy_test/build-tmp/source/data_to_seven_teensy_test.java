import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import processing.serial.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class data_to_seven_teensy_test extends PApplet {



Serial[] teensies = new Serial[7];
int[] b_rates = {9600,14400,19200,28800,38400,57600,115200};    

public void setup() {
	println(Serial.list().length);
	for (int i = 0 ; i < Serial.list().length; i++) {
		println(Serial.list()[i]);
		//teensies[i] = new Serial(this, Serial.list()[i+11], b_rates[i]);
	}
}

public void draw() {
	// for (int i = 0; i < teensies.length; i++) {
	// 	teensies[i].write(65);
	// }
	// for (int i = 0; i < teensies.length; i++) {
	// 	if (teensies[i].available() > 0) {
	// 		println(teensies[i].readStringUntil('\n'));
	// 	}
	// }

}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "data_to_seven_teensy_test" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
