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

  void followLine() {
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
  
  PVector getNormalPoint(PVector p, PVector a, PVector b) {
    PVector ap = PVector.sub(p, a);
    PVector ab = PVector.sub(b, a);
    ab.normalize();
    ab.mult(ap.dot(ab));
    PVector normalPoint = PVector.add(a, ab);
    return normalPoint;
  }
  
  void update() {
    velocity.add(acceleration);
    velocity.limit(maxSpeed);
    location.add(velocity);
    acceleration.mult(0);
  }

  void applyForce(PVector force) {
    acceleration.add(force);
  }

  void seek(PVector target) {
    PVector desired = PVector.sub(target,location);
    desired.normalize();
    desired.mult(maxSpeed);

    PVector steer = PVector.sub(desired, velocity);
    steer.limit(maxForce);
    applyForce(steer);
  }

  // Wraparound
  void borders() {
    if (location.x > width) {
      location.x = 0;
    }
    if (location.x < 0 ) {
      location.x = width;
    }
  }
}

