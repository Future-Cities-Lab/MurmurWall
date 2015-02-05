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

int TIME_DELAY = 30000;
int time;

int current_trend_position;
String current_trend;

ArrayList<String> trends = new ArrayList<String>();
ArrayList<String> buckets = new ArrayList<String>();

int rect_width = 200;
int rect_height = 50;

int[][] rectangles = {{-360,50},{-310,-250},{-260,-100},{-60,50},{0,-250},{40,-100},{240,50}};


int[] current_words_x_pos = new int[7];


public void setup() {

	size(900,700);

	time = millis();

	textAlign(LEFT,CENTER);

	for (int i = 0; i < current_words_x_pos.length; i++) {
		current_words_x_pos[i] = rectangles[i][0];
	}
	
	// json = loadJSONObject("data.json");
	// for (Object trend : json.keys()) {
	// 	trends.add(trend.toString());
	// }
	// current_trend_position = 0;
	// current_trend = trends.get(current_trend_position);

	// for (int i = 0; i < json.getJSONArray(current_trend).size(); i++) {
	// 	if (!json.getJSONArray(current_trend).getString(i).equals("")) {
	// 		buckets.add(json.getJSONArray(current_trend).getString(i));
	// 	}
	// }
	// println(buckets);

}

public void draw() {

	background(255, 255, 255, 255);

	if (millis() > time + TIME_DELAY) {
		buckets.clear();
		println("Updating");
		current_trend_position++;
		current_trend_position %= trends.size();
		current_trend = trends.get(current_trend_position);
		for (int i = 0; i < json.getJSONArray(current_trend).size(); i++) {
			buckets.add(json.getJSONArray(current_trend).getString(i));
			println(buckets.get(i));
		}
		println("");
		time = millis();
	}

	translate(width/2, height/2);
	rotate(-PI/3.0f);
	
	// Draw Boxes and Text
    for (int i = 0; i < rectangles.length; i++) {
    	int[] rect_cords = rectangles[i];
    	fill(0,0,0);
    	stroke(255,255,102);
    	rect(rect_cords[0], rect_cords[1], rect_width, rect_height);
    	fill(255,255,255,255);
		textSize(24);
		text("BUTT SURF HUWA HUWA", current_words_x_pos[i], rect_cords[1] + rect_height/2);
		current_words_x_pos[i]++; 
    }

    // Draw Mask
	for (int i = 0; i < width; i++) {
		for (int j = 0; j < height; j++) {
			boolean not_in_rectangle = true;
			for (int k = 0; k < rectangles.length; k++) {
				int[] rect_cords = rectangles[k];
				if (i >= rect_cords[0] && i <= rect_cords[0] + rect_width && j >= rect_cords[1] && j <= rect_cords[1] + rect_height) {
					not_in_rectangle = false;
				}
			}
			if (not_in_rectangle) {
				stroke(255,255,255,255);
				point(i,j);
			}
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
