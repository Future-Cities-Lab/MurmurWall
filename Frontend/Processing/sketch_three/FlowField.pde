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
  
  void initField() {
    
    noiseSeed((int)random(10000));
    float xOff = 0;
    for (int i = 0; i < cols; i++) {
      float yOff = 0;
      for (int j = 0; j < rows; j++) {
        float theta = map(noise(xOff,yOff),0,1,0,TWO_PI);
        field[i][j] = new PVector(cos(theta),sin(theta));
        yOff += 0.1;
      }
      xOff += 0.1;
    }
  }
    // Draw every vector
  void display() {
    for (int i = 0; i < cols; i++) {
      for (int j = 0; j < rows; j++) {
        drawVector(field[i][j],i*resolution,j*resolution,resolution-2);
      }
    }

  }

  // Renders a vector object 'v' as an arrow and a location 'x,y'
  void drawVector(PVector v, float x, float y, float scayl) {
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
  
  PVector lookup(PVector lookup) {
    int column = int(constrain(lookup.x/resolution,0,cols-1));
    int row = int(constrain(lookup.y/resolution,0,rows-1));
    return field[column][row].get();
  }

}
