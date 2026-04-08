#include <Servo.h>

Servo pan;
Servo tilt;

const int trigPin = 11;
const int echoPin = 12;

void setup() {
  Serial.begin(9600); // Match this in your Serial Monitor!
  pan.attach(9);
  tilt.attach(10);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  pan.write(90);
  tilt.write(70); 
  delay(1000);
}

void loop() {
  // TILT loop (Vertical)
  for (int t = 70; t <= 130; t += 5) {
    tilt.write(t);
    delay(100);

    // PAN loop (Horizontal)
    if ((t / 5) % 2 == 0) {
      // Even rows: Go Left to Right (45 to 135)
      for (int p = 0; p <= 180; p += 3) {
        scan(p, t);
      }
    } else {
      // Odd rows: Go Right to Left (135 to 45)
      for (int p = 180; p >= 0; p -= 3) {
        scan(p, t);
      }
    }
  }
  Serial.println("SCAN_COMPLETE");
  while(1); // Stop after one full 3D scan
}

void scan(int p, int t) {
  pan.write(p);
  delay(35); // Small delay to prevent 'glk' and '?' errors
  
  long dist = getDistance();
  
  // Output for your Linux/Conda script
  Serial.print(p);
  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.println(dist);
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000);
  return duration * 0.034 / 2;
}
