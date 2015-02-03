import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import de.bezier.data.sql.*; 
import java.util.Map; 
import java.util.Set; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class sketch_one extends PApplet {

 



public SQLite db;

public HashMap<String, HashMap<String, Integer>> hm  = new HashMap<String, HashMap<String, Integer>>();
public ArrayList<String> trends = new ArrayList<String>();

public int startWordOne = 0;
public int startWordTwo = 1;

public int currentWordOne;
public int currentWordTwo;

public int startWordOneXPos;
public int startWordTwoXPos;

public int currentWordOneXPos;
public int currentWordTwoXPos;

public float startAngle;
public float currentAngle;
public float angleVelocity;

public void setup() {
  size(1200,600);
  
  // Load Data
  db = new SQLite(this, "searches.db");
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
  // Drawing Setup
  textSize(60);
  textAlign(CENTER);
  currentWordOne = startWordOne;
  currentWordTwo = startWordTwo;
  
  startWordOneXPos = (2*width)/3;
  startWordTwoXPos = width/3;
 
  currentWordOneXPos = startWordOneXPos;
  currentWordTwoXPos = startWordTwoXPos;
  
  startAngle = 0;
  currentAngle = startAngle;
  angleVelocity = 0.01f;
}

public void draw() {
  background(64,64,64);
  
  translate(-(frameCount % (width*trends.size())), 0);

  int currentX = width/2;
  int deltaX = width;
  fill(0, 102, 153);
  text(trends.get(0), currentX, height/2);
  for (int i = 1; i < trends.size(); i++) {
    currentX += deltaX;
    fill(0, 102, 153);
    text(trends.get(i), currentX, height/2);
    HashMap<String, Integer> map = hm.get(trends.get(i));
    currentAngle += angleVelocity;
    for (Map.Entry me : map.entrySet()) {
      ///println(me.getKey());
      float blue = map((Integer)me.getValue(),0,100,50,200);
      float topAlpha = map((Integer)me.getValue(),0,100,50,20);
      float alpha = map(sin(currentAngle), -1.0f,1.0f,1,topAlpha);
      fill(blue - 50, blue, 163,alpha);
      float randomX;
      if ((Integer)me.getValue() >= 50) {
        randomX = map((Integer)me.getValue(),50,100,-180,180);
      } else if ((Integer)me.getValue() >= 25 && (Integer)me.getValue() < 50) {
          randomX = map((Integer)me.getValue(),25,49,180,280);
      } else {
          randomX = map((Integer)me.getValue(),0,24,-180,-280);
      }
      text((String)me.getKey(), currentX + randomX, height/2 + randomX);
    }
    //println();
  }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "sketch_one" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
