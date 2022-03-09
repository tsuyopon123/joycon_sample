String url = "http://localhost:8080";
// String url = "http://192.168.3.9:8080";

void setup() {
  size(800, 800, P3D);
}

void draw() {
  try {
    JSONObject data = loadJSONObject(url);
    // memo: https://github.com/tocoteron/joycon-python/blob/master/pyjoycon/gyro.py#L75
    float x = data.getFloat("x") * 57;
    float y = data.getFloat("y") * 57;
    float z = data.getFloat("z") * 57;

    background(0);
    translate(width/2, height/2, -200);
    rotateX(radians(-x));
    rotateY(radians(-y));
    rotateZ(radians(z));
    box(300, 150, 100);
  }
  catch(Exception e) {
    println("loadJSON Failed");
  }
  
  delay(10);
}
