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

public class multiple_teensy extends PApplet {



private int NUM_MATRICES = 7;
private String[] teensies = new String[NUM_MATRICES];
private String[] teensies_new = new String[NUM_MATRICES];

private Serial[] teensy_serial = new Serial[NUM_MATRICES];
private int last_time;
private int dT = 30000;
private String[] usb_ports = {"688851","616481","618061","688531","688321","688291","604971"};


public void setup() {
	for (int i = 0; i < NUM_MATRICES; i++) {
		teensies[i] = Serial.list()[Serial.list().length-1-i];
	}

	//DEBUG
	// for (int i = 0; i < Serial.list().length; i++) {
	// 	println(Serial.list()[i]);
	// }
	for (int i = 0; i < NUM_MATRICES; i++) {
		String to_find = usb_ports[i];
		String port = "";
		for (int j = 0; j < NUM_MATRICES; j++) {
			if (teensies[j].contains(to_find)) {
				teensy_serial[i] = new Serial(this, teensies[j], 9600);
				teensy_serial[i].bufferUntil('\n');
			}
		}
	}
	last_time = millis();

}

public void draw() {
	for (int i = 0; i < NUM_MATRICES; i++) {
		println("Writting to " + teensy_serial[i].toString());
		teensy_serial[i].write(65);
		delay(10000);
	}
}

public void serialEvent(Serial p) { 
	String val = p.readStringUntil('\n');
	println(val); 
	p.clear();
} 

public void stop() {
	for (int i = 0; i < NUM_MATRICES; i++) {
		println("Closing!");
		teensy_serial[i].stop();
	}

} 
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "multiple_teensy" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
