import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import de.bezier.data.sql.*; 
import java.util.Map; 
import processing.serial.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class sketch_three extends PApplet {

 

public SQLite db;



public HashMap<String, HashMap<String, Integer>> hm  = new HashMap<String, HashMap<String, Integer>>();
public ArrayList<String> trends = new ArrayList<String>();


ArrayList<Path> paths;
ArrayList<Vehicle> vehicles;

Serial myPort;

int time = 500;

public void setup() {
  size(1200,200);
  
  loadDataFromDB("searches.db");
  
  //arduino com
  String portName = Serial.list()[5];
  myPort = new Serial(this, portName, 38400);
  
  smooth();
  paths = new ArrayList<Path>();
  for (int i = 0; i < trends.size(); i++) {
    paths.add(new Path());
  }
  
  vehicles = new ArrayList<Vehicle>();
  int cnt = 0;
  for (Path path : paths) {
    vehicles.add(new Vehicle(new PVector(width, height/2), 2,1, path, trends.get(cnt))); 
    cnt++;
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

public void draw() {
  background(255);
  noFill();
  
  for (Path path : paths) {
    path.display(); 
  }
  
  int leftXStart = 100;
  int leftXDiff = 50;
  int leftY1 = 65;
  int leftY2 = 40;
  int cnt = 0;
  for (int i = leftXStart; i <= 240; i+=leftXDiff) {
    int currentY = leftY1;
    if (cnt % 2 != 0) {
      currentY = leftY2;
    }
    // draw left panels
    fill(255,255,255);
    strokeWeight(3);
    stroke(0,0,0);
    rect(i, currentY, 60, 15);
    cnt++;
  }
  
  fill(204, 102, 0);
  stroke(204, 102, 0);
  for (Vehicle vehicle : vehicles) {
    vehicle.run();
    // if vehicle is in box, dont display
    if (vehicle.location.x > 200 && vehicle.location.x < 260 && vehicle.location.y > 65 && vehicle.location.y < 80 && time > 500) {
      String toArduino = trends.get(PApplet.parseInt(random(0,trends.size()-1))) + "\n";
      myPort.write(toArduino);
      println("writting to arduino");
      time = 0;
    }
    ellipse(vehicle.location.x, vehicle.location.y, 5,5);
  }
  time++;
}

public void mouseReleased() {
  String toArduino = trends.get(PApplet.parseInt(random(0,trends.size()-1))) + "\n";
  myPort.write(toArduino);
  println("writting to arduino");
}
class FlowField {
  PVector[][] field;
  int cols, rows;
  int resolution;
  
  FlowField() {
    resolution = 10;
    cols = width/resolution;
    rows = height/resolution;
    field = new PVector[cols][rows];
    
    initField();
  }
  
  public void initField() {
    
    noiseSeed((int)random(10000));
    float xOff = 0;
    for (int i = 0; i < cols; i++) {
      float yOff = 0;
      for (int j = 0; j < rows; j++) {
        float theta = map(noise(xOff,yOff),0,1,0,TWO_PI);
        field[i][j] = new PVector(cos(theta),sin(theta));
        yOff += 0.1f;
      }
      xOff += 0.1f;
    }
  }
    // Draw every vector
  public void display() {
    for (int i = 0; i < cols; i++) {
      for (int j = 0; j < rows; j++) {
        drawVector(field[i][j],i*resolution,j*resolution,resolution-2);
      }
    }

  }

  // Renders a vector object 'v' as an arrow and a location 'x,y'
  public void drawVector(PVector v, float x, float y, float scayl) {
    pushMatrix();
    float arrowsize = 4;
    // Translate to location to render vector
    translate(x,y);
    stroke(0,100);
    // Call vector heading function to get direction (note that pointing to the right is a heading of 0) and rotate
    rotate(v.heading2D());
    // Calculate length of vector & scale it to be bigger or smaller if necessary
    float len = v.mag()*scayl;
    // Draw three lines to make an arrow (draw pointing up since we've rotate to the proper direction)
    line(0,0,len,0);
    //line(len,0,len-arrowsize,+arrowsize/2);
    //line(len,0,len-arrowsize,-arrowsize/2);
    popMatrix();
  }
  
  public PVector lookup(PVector lookup) {
    int column = PApplet.parseInt(constrain(lookup.x/resolution,0,cols-1));
    int row = PApplet.parseInt(constrain(lookup.y/resolution,0,rows-1));
    return field[column][row].get();
  }

}
class Path {
 
  ArrayList<PVector> points;
  
  int radius;
  
  Path() {
    radius = 10;
    points = new ArrayList<PVector>();
   
//    points.add(new PVector(0, height/3));
//    points.add(new PVector(random(width/4,width/3), random(0,height/2))) ;
//    points.add(new PVector(random((3*width)/4, (2*width)/3), random(height/2,height)));
//    points.add(new PVector(width, (2*height)/3));
//    
    points.add(new PVector(width, (2*height)/3));
    float ran = random(0,1);
    float yPos1 = random(height/2,height);
    float yPos2 = random(0,height/2);
    if (ran > 0.5f) {
      float temp = yPos1;
      yPos1 = yPos2;
      yPos2 = temp;
    }
    points.add(new PVector(random((3*width)/4, (2*width)/3), yPos1));
    points.add(new PVector(random(width/4,width/3), yPos2)) ;
    points.add(new PVector(0, height/3));
  
}
  
  public void display() {
//  
//    strokeWeight(10*2);  
//    stroke(0, 100);
//    beginShape();
//    for (PVector v : points) {
//      vertex(v.x,v.y);
//    }
//    endShape(); 
    
    strokeWeight(1);  
    stroke(0);
    beginShape();
    for (PVector v : points) {
      vertex(v.x,v.y);
    }
    endShape(); 
  }

  
}
class Vehicle {

  PVector location;
  PVector velocity;
  PVector acceleration;

  Path path;

  int maxSpeed;
  int maxForce;
  
  String word;

  Vehicle(PVector l, int mS, int mF, Path p, String w) {
    acceleration = new PVector(0, 0);
    velocity = new PVector(-random(0,100), -random(0,100));
    location = l.get();
    maxSpeed = mS;
    maxForce = mF;
    path = p;
    word = w;  
  }

  public void run() {
    followLine();
    update();
    borders();
  }

  public void followLine() {
    PVector predict = velocity.get();
    predict.normalize();
    predict.mult(50);
    PVector predictLoc = PVector.add(location, predict);

    PVector normal = null;
    PVector target = null;
    float worldRecord = 1000000;  

    for (int i = 0; i < path.points.size()-1; i++) {

      PVector a = path.points.get(i);
      PVector b = path.points.get(i+1);

      PVector normalPoint = getNormalPoint(predictLoc, a, b);
      
      if (normalPoint.x < min(a.x,b.x) || normalPoint.x > max(a.x,b.x)) {
        normalPoint = b.get();
      }

      float distance = PVector.dist(predictLoc, normalPoint);
      if (distance < worldRecord) {
        worldRecord = distance;
        normal = normalPoint;

        PVector dir = PVector.sub(b, a);
        dir.normalize();
        dir.mult(10);
        target = normalPoint.get();
        target.add(dir);
      }
    }

    if (worldRecord > path.radius) {
      seek(target);
    }
    
  }
  
  public PVector getNormalPoint(PVector p, PVector a, PVector b) {
    PVector ap = PVector.sub(p, a);
    PVector ab = PVector.sub(b, a);
    ab.normalize();
    ab.mult(ap.dot(ab));
    PVector normalPoint = PVector.add(a, ab);
    return normalPoint;
  }
  
  public void update() {
    velocity.add(acceleration);
    velocity.limit(maxSpeed);
    location.add(velocity);
    acceleration.mult(0);
  }

  public void applyForce(PVector force) {
    acceleration.add(force);
  }

  public void seek(PVector target) {
    PVector desired = PVector.sub(target,location);
    desired.normalize();
    desired.mult(maxSpeed);

    PVector steer = PVector.sub(desired, velocity);
    steer.limit(maxForce);
    applyForce(steer);
  }

  // Wraparound
  public void borders() {
    if (location.x > width) {
      location.x = 0;
    }
    if (location.x < 0 ) {
      location.x = width;
    }
  }
}

  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "sketch_three" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
