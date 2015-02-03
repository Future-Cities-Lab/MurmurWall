import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import de.bezier.data.sql.*; 
import java.util.Map; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class sketch_two extends PApplet {

 

public SQLite db;

// data structured to represent DB info Java-side
public HashMap<String, HashMap<String, Integer>> hm  = new HashMap<String, HashMap<String, Integer>>();
public ArrayList<String> trends = new ArrayList<String>();

// geometric values for the rectangles/words
int rectWidth = 60;
int rectHeight = 15;
int lineDX = 5;

int leftDiff = 40;
int rightDiff = 120;

int c1, c2;

float count = 0;

float zOff = 0.0f;
float zOffDX = 0.2f;

// current words on screen
int ranSpot1;
int ranSpot2;

// list of associated searches for words
ArrayList<String> associated1;
ArrayList<String> associated2;
HashMap<String, Integer> associatedMap1;
HashMap<String, Integer> associatedMap2;

// clock for updating data
int time = 0;

// where each word starts/where it currently is
int[] startWordXPos = new int[10];
int[] currentWordXPos = new int[10];

public void setup() {
  size(1200,200);

  // ambient colors
  c1 = color(204, 102, 0);
  c2 = color(0, 102, 153);

  // drawing states
  ellipseMode(CENTER);
  textSize(10);
  rectMode(CENTER);
  textAlign(RIGHT);
  
  // get data.....
  loadDataFromDB("searches.db");
  
  // load starting words
  getStartingWords();

  // compute starting positions
  getStartingTextPositions();
}

public void getStartingWords() {
  ranSpot1 = PApplet.parseInt(random(0,trends.size()-1));
  ranSpot2 = PApplet.parseInt(random(0,trends.size()-1));
  associatedMap1 = hm.get(trends.get(ranSpot1));
  associatedMap2 = hm.get(trends.get(ranSpot2));
  
  associated1 = new ArrayList<String>();
  for (Map.Entry word : associatedMap1.entrySet()) { 
    associated1.add((String)word.getKey());
  }  
  
  associated2 = new ArrayList<String>();
  for (Map.Entry word : associatedMap2.entrySet()) { 
    associated2.add((String)word.getKey());
  }
}

public void loadDataFromDB(String dataB) {
  db = new SQLite(this, dataB);
  if (db.connect()) {
        String[] tableNames = db.getTableNames();
        for (String name : tableNames) {
          db.query( "SELECT * FROM %s", name );
          HashMap<String, Integer> fields = new HashMap<String, Integer>();
          while (db.next()) {
              fields.put(db.getString("name"), db.getInt("count"));
          }
          hm.put(name, fields);
        }
  }
  
  for (Map.Entry trend : hm.entrySet()) { 
    trends.add((String)trend.getKey());
  }
}

public void getStartingTextPositions() {
  int cnt = 0;
  for (int i = 40; i <= 240; i+=50) {
    startWordXPos[cnt] = i + leftDiff;
    startWordXPos[startWordXPos.length - 1 - cnt] = width - i - leftDiff;
    currentWordXPos[cnt] = i + leftDiff;
    currentWordXPos[startWordXPos.length - 1 - cnt] = width - i - leftDiff;    
    cnt++;
  }
}

public void drawAmbientBackground() {
  float xOff = 0.0f;
  for (int i = 0; i <= width; i+=lineDX) {
    float yOff = 0.0f;
    for (int j = 0; j <= height; j+=lineDX) {
        float inter = map(i, 0, width, 0, 1);
        float yeah = sin(count);
        float alpha = map(noise(xOff,yOff,zOff), 0, 1, 0, 255);
        c1 = color(127+127*yeah, 100, 127+127*-1*yeah);
        c2 = color(127+127*-1*yeah, 100, 127+127*yeah);
        int fc = lerpColor(c1,c2,inter);
        //color fc2 = lerpColor(c1,c2,inter);
        noStroke();
        fill(fc,alpha);
        ellipse(i,j,3,3);
        yOff += 0.05f;
    }
    xOff += 0.05f;
  }
  
  zOff += zOffDX;
}

public void updateEverySeconds(int seconds) {
  if (millis() > time + seconds) {
    updateData();
  }
}

public void updateData() {
  ranSpot1 = PApplet.parseInt(random(0,trends.size()-1));
  ranSpot2 = PApplet.parseInt(random(0,trends.size()-1));
  associatedMap1 = hm.get(trends.get(ranSpot1));
  associatedMap2 = hm.get(trends.get(ranSpot2));
  
  associated1 = new ArrayList<String>();
  for (Map.Entry word : associatedMap1.entrySet()) { 
    associated1.add((String)word.getKey());
  }  
  
  associated2 = new ArrayList<String>();
  for (Map.Entry word : associatedMap2.entrySet()) { 
    associated2.add((String)word.getKey());
  }
  time = millis();
}

public void draw() {
  
  background(0, 0, 0);
  
  // background ambience
  drawAmbientBackground();
  
  int leftXStart = 40;
  int leftXDiff = 50;
  int leftY1 = 65;
  int leftY2 = 40;
  int cnt = 0;
  
  float xAlphaOff = 0.0f;
 
  // update current text data every 30 seconds
  updateEverySeconds(30000);

  // draw boxes and text
  for (int i = leftXStart; i <= 240; i+=leftXDiff) {
    int currentY = leftY1;
    if (cnt % 2 != 0) {
      currentY = leftY2;
    }
    // draw left panels
    fill(0,0,0);
    stroke(255,255,102);
    rect(startWordXPos[cnt], currentY, rectWidth, rectHeight);
    fill(255,255,102);
    
    
    String wordToDisplay = "";
    float w;

    if (cnt == 2) {
      textSize(14);
      fill(255,255,200);
      wordToDisplay = trends.get(ranSpot1);
      text(wordToDisplay, currentWordXPos[cnt], currentY + 6);  
      textSize(10);
    } else if (cnt < associated1.size()) {
      wordToDisplay = associated1.get(cnt);
      Integer value = associatedMap1.get(wordToDisplay);
      float alpha = map(value, 0, 100, 110,220);
      textSize(10);
      fill(255,255,102,100);
      text(wordToDisplay, currentWordXPos[cnt], currentY + 6);  
    }
    
    currentWordXPos[cnt]++;
    w = textWidth(wordToDisplay); 
    if (currentWordXPos[cnt] > startWordXPos[cnt] + w) {
      currentWordXPos[cnt] = startWordXPos[cnt];
    }
    
    // draw right panels
    fill(0,0,0);
    stroke(255,255,102);
    rect(startWordXPos[startWordXPos.length - 1 - cnt], height - currentY, rectWidth, rectHeight);
    fill(255,255,102);
    
    if (cnt == 2) {      
      fill(255,255,200);
      textSize(14);
      wordToDisplay = trends.get(ranSpot2);
      text(wordToDisplay, currentWordXPos[startWordXPos.length - 1 - cnt], height - currentY + 6); 
    } else if (cnt < associated2.size()) {
      wordToDisplay = associated2.get(cnt);
      Integer value = associatedMap2.get(wordToDisplay);
      float alpha = map(value, 0, 100, 110,220);
      textSize(10); 
      fill(255,255,102,alpha);
      text(wordToDisplay, currentWordXPos[startWordXPos.length - 1 - cnt], height - currentY + 6);  
    }
    currentWordXPos[startWordXPos.length - 1 - cnt]++;
    w = textWidth(wordToDisplay); 
    if (currentWordXPos[startWordXPos.length - 1 - cnt] > startWordXPos[startWordXPos.length - 1 - cnt] + w) {
      currentWordXPos[startWordXPos.length - 1 - cnt] = startWordXPos[startWordXPos.length - 1 - cnt];
    }
    
    cnt++;
    xAlphaOff += 0.05f;
  }
  count += 0.2f;

}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "sketch_two" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
