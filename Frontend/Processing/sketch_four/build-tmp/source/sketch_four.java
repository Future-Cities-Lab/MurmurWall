import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class sketch_four extends PApplet {

JSONObject json;
PImage img;

private int TIME_DELAY = 30000;
private int NUM_BUCKETS = 7;
private int time;

ArrayList<String> trends = new ArrayList<String>();

int[] buckets = new int[7];

String[] data;

boolean[] bucket_displaying = new boolean[NUM_BUCKETS];


int rect_width = 150;
int rect_height = 37;

int[][] rectangles = {	{83, 391},
						{122, 478},
						{314, 362},
						{340, 460},
						{537, 354},
						{563, 476},
						{748, 384}
};

float[] angles = {-PI/3.4f,-PI/3.4f,-PI/3.4f,-PI/3.6f,-PI/3.5f,-PI/3.4f,-PI/3.5f};

float[] current_words_x_pos = new float[NUM_BUCKETS];


public void setup() {

	size(900,700);

	time = millis();

	textAlign(LEFT,CENTER);
	textSize(14);

	img = loadImage("Murmur_Wall_Elevation-900x700.png");

	json = loadJSONObject("data.json");
	int num_of_trends = json.keys().size();
	int amount_of_data = num_of_trends*NUM_BUCKETS;
	data = new String[amount_of_data];

	int i = 0;
	for (Object trend : json.keys()) {
		JSONArray responses = json.getJSONArray(trend.toString());
		for (int j = 0; j < NUM_BUCKETS; j++) {
			if (responses.size() == 0) {
				data[i] = "BAD DATA";
			} else {
				data[i] = responses.getString(PApplet.parseInt(random(responses.size())));
			}
			i++;
		}
	}

	for (int j = 0; j < buckets.length; j++) {
		buckets[j] = j;
	}
	updateStartPosition();
	smooth();
}

public void draw() {
	background(0, 0, 0, 255);	
	drawText();
	image(img, 0, 0);
}

private void updateStartPosition() {
	for (int i = 0; i < NUM_BUCKETS; i++) {
		current_words_x_pos[i] = -textWidth(data[buckets[i]]);
	}
}

private void drawText() {
	for (int i = 0; i < rectangles.length; i++) {
	  	pushMatrix();
			translate(rectangles[i][0], rectangles[i][1]);
			rotate(angles[i]);
		  	fill(255,255,255,255);
			text(data[buckets[i]].toUpperCase(), current_words_x_pos[i], rect_height/2.5f);
		popMatrix();
		current_words_x_pos[i]+= 0.5f;
		if (current_words_x_pos[i] > rect_width) {
			buckets[i]--;
			if (buckets[i] == -1) {
				buckets[i] = data.length-1;
			}
			current_words_x_pos[i] = -textWidth(data[buckets[i]]);
 	 	}
	 }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "sketch_four" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
