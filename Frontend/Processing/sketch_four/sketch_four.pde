JSONObject json;

int TIME_DELAY = 30000;
int time;

int current_trend_position;
String current_trend;

ArrayList<String> trends = new ArrayList<String>();
ArrayList<String> buckets = new ArrayList<String>();

int rect_width = 200;
int rect_height = 50;

int[][] rectangles = {{-360,50},{-310,-250},{-260,-100},{-60,150},{0,250},{40,0},{240,200}};

int[] start_words_x_pos = new int[7];
int[] current_words_x_pos = new int[7];


void setup() {

	size(900,700);

	time = millis();

	textAlign(LEFT,CENTER);
	textSize(24);

	for (int i = 0; i < start_words_x_pos.length; i++) {
		start_words_x_pos[i] = rectangles[i][0] - int(textWidth("BUTT SURF HUWA HUWA"));
		current_words_x_pos[i] = start_words_x_pos[i];
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

void draw() {

	background(255, 255, 255, 255);

	// if (millis() > time + TIME_DELAY) {
	// 	buckets.clear();
	// 	println("Updating");
	// 	current_trend_position++;
	// 	current_trend_position %= trends.size();
	// 	current_trend = trends.get(current_trend_position);
	// 	for (int i = 0; i < json.getJSONArray(current_trend).size(); i++) {
	// 		buckets.add(json.getJSONArray(current_trend).getString(i));
	// 		println(buckets.get(i));
	// 	}
	// 	println("");
	// 	time = millis();
	// }

	pushMatrix();
	translate(width/2, height/2);
	rotate(-PI/3.0);
	
	// Draw Boxes and Text
    for (int i = 0; i < rectangles.length; i++) {
    	int[] rect_cords = rectangles[i];
    	fill(0,0,0);
    	stroke(255,255,102);
    	rect(rect_cords[0], rect_cords[1], rect_width, rect_height);
    	fill(255,255,255,255);
		text("BUTT SURF HUWA HUWA", current_words_x_pos[i], rect_cords[1] + rect_height/2);
		current_words_x_pos[i]++;
		if (current_words_x_pos[i] > start_words_x_pos[i] + rect_width + textWidth("BUTT SURF HUWA HUWA")) {
      		current_words_x_pos[i] = start_words_x_pos[i];
    	} 
    }

    popMatrix();
  //   for (int i = 0; i < current_words_x_pos.length; i++) {
		// current_words_x_pos[i]++; 
		// current_words_x_pos[i] %= rectangles[i][0] + rect_width + int(textWidth("BUTT SURF HUWA HUWA"));
  //   }
}