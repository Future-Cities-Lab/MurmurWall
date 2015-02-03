import de.bezier.data.sql.*; 
import java.util.Map;
public SQLite db;
import processing.serial.*;


public HashMap<String, HashMap<String, Integer>> hm  = new HashMap<String, HashMap<String, Integer>>();
public ArrayList<String> trends = new ArrayList<String>();


ArrayList<Path> paths;
ArrayList<Vehicle> vehicles;

Serial myPort;

int time = 500;

void setup() {
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

void loadDataFromDB(String dataB) {
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

void draw() {
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
      String toArduino = trends.get(int(random(0,trends.size()-1))) + "\n";
      myPort.write(toArduino);
      println("writting to arduino");
      time = 0;
    }
    ellipse(vehicle.location.x, vehicle.location.y, 5,5);
  }
  time++;
}

void mouseReleased() {
  String toArduino = trends.get(int(random(0,trends.size()-1))) + "\n";
  myPort.write(toArduino);
  println("writting to arduino");
}
