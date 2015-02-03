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
    if (ran > 0.5) {
      float temp = yPos1;
      yPos1 = yPos2;
      yPos2 = temp;
    }
    points.add(new PVector(random((3*width)/4, (2*width)/3), yPos1));
    points.add(new PVector(random(width/4,width/3), yPos2)) ;
    points.add(new PVector(0, height/3));
  
}
  
  void display() {
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
