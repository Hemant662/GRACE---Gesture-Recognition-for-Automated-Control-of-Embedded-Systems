// Motor control pins (Left Motor Driver)
const int in1_left = 3;  // Motor A forward (left motor)
const int in2_left = 4;  // Motor A backward (left motor)
const int in3_left = A1;  // Motor B forward (left motor)
const int in4_left = A2;  // Motor B backward (left motor)
const int ena_left = 10;  // Motor A speed (set to HIGH for full speed)
const int enb_left = 11; // Motor B speed (set to HIGH for full speed)

// Motor control pins (Right Motor Driver)
const int in1_right = 7;  // Motor A forward (right motor)
const int in2_right = 8;  // Motor A backward (right motor)
const int in3_right = 9;  // Motor B forward (right motor)
const int in4_right = 12; // Motor B backward (right motor)
const int ena_right = 5;  // Motor A speed (set to HIGH for full speed)
const int enb_right = 6;  // Motor B speed (set to HIGH for full speed)

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  // Initialize motor control pins as OUTPUT
  pinMode(in1_left, OUTPUT);
  pinMode(in2_left, OUTPUT);
  pinMode(in3_left, OUTPUT);
  pinMode(in4_left, OUTPUT);
  pinMode(ena_left, OUTPUT);  // Enable motor A (Left) at full speed
  pinMode(enb_left, OUTPUT);  // Enable motor B (Left) at full speed

  pinMode(in1_right, OUTPUT);
  pinMode(in2_right, OUTPUT);
  pinMode(in3_right, OUTPUT);
  pinMode(in4_right, OUTPUT);
  pinMode(ena_right, OUTPUT); // Enable motor A (Right) at full speed
  pinMode(enb_right, OUTPUT); // Enable motor B (Right) at full speed
  
 // Set ENA and ENB pins to HIGH to enable motors at full speed
  analogWrite(ena_left, 127);
  analogWrite(enb_left, 127);
  analogWrite(ena_right, 127);
  analogWrite(enb_right, 127);
  
  stopCar();
}

void loop() {
    if (Serial.available() > 0) {
        delay(10);
        char command = Serial.read();
        Serial.print("Received command: ");
        Serial.println(command);

        // Process the command
        if (command == 'F') {
            moveForward();
        } else if (command == 'B') {
            moveBackward();
        } else if (command == 'L') {
            turnLeft();
        } else if (command == 'R') {
            turnRight();
        } else if (command == 'S') {
            stopCar();
        }
    }
}


void moveForward() {
  digitalWrite(in1_left, HIGH);
  digitalWrite(in2_left, LOW);
  digitalWrite(in3_left, HIGH);
  digitalWrite(in4_left, LOW);
  digitalWrite(in1_right, HIGH);
  digitalWrite(in2_right, LOW);
  digitalWrite(in3_right, HIGH);
  digitalWrite(in4_right, LOW);
}

void moveBackward() {
  digitalWrite(in1_left, LOW);
  digitalWrite(in2_left, HIGH);
  digitalWrite(in3_left, LOW);
  digitalWrite(in4_left, HIGH);
  digitalWrite(in1_right, LOW);
  digitalWrite(in2_right, HIGH);
  digitalWrite(in3_right, LOW);
  digitalWrite(in4_right, HIGH);
}

void turnLeft() {
  digitalWrite(in1_left, LOW);
  digitalWrite(in2_left, HIGH);
  digitalWrite(in3_left, LOW);
  digitalWrite(in4_left, HIGH);
  digitalWrite(in1_right, HIGH);
  digitalWrite(in2_right, LOW);
  digitalWrite(in3_right, HIGH);
  digitalWrite(in4_right, LOW);
}

void turnRight() {
  digitalWrite(in1_left, HIGH);
  digitalWrite(in2_left, LOW);
  digitalWrite(in3_left, HIGH);
  digitalWrite(in4_left, LOW);
  digitalWrite(in1_right, LOW);
  digitalWrite(in2_right, HIGH);
  digitalWrite(in3_right, LOW);
  digitalWrite(in4_right, HIGH);
}

void stopCar() {
  digitalWrite(in1_left, LOW);
  digitalWrite(in2_left, LOW);
  digitalWrite(in3_left, LOW);
  digitalWrite(in4_left, LOW);
  digitalWrite(in1_right, LOW);
  digitalWrite(in2_right, LOW);
  digitalWrite(in3_right, LOW);
  digitalWrite(in4_right, LOW);
}
