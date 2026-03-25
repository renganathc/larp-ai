#include <Arduino.h>
#include "ssp_motor.h"
#include "ssp_servo.h"

const unsigned long SERIAL_BAUD = 115200;
String lineBuffer = "";

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(1000);
  Serial.println("[SSP] Ready");

  motor_setup();
  servo_setup();
}

void processCommand(const String &command) {
  String cmd = command;
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "FORWARD") {
    moveForward();
    Serial.println("[SSP] FORWARD");
  } else if (cmd == "BACKWARD") {
    moveBackward();
    Serial.println("[SSP] BACKWARD");
  } else if (cmd == "LEFT") {
    turnLeft();
    Serial.println("[SSP] LEFT");
  } else if (cmd == "RIGHT") {
    turnRight();
    Serial.println("[SSP] RIGHT");
  } else if (cmd == "TURN_180") {
    turn180();
    Serial.println("[SSP] TURN_180");
  } else if (cmd == "TURN_360") {
    turn360();
    Serial.println("[SSP] TURN_360");
  } else if (cmd == "HEAD_UP") {
    headUp();
    Serial.println("[SSP] HEAD_UP");
  } else if (cmd == "HEAD_DOWN") {
    headDown();
    Serial.println("[SSP] HEAD_DOWN");
  } else if (cmd == "HEAD_CENTER") {
    headCenter();
    Serial.println("[SSP] HEAD_CENTER");
  } else if (cmd == "HEAD_LEFT") {
    headLeft();
    Serial.println("[SSP] HEAD_LEFT");
  } else if (cmd == "HEAD_RIGHT") {
    headRight();
    Serial.println("[SSP] HEAD_RIGHT");
  } else if (cmd == "NOD_YES") {
    nodYes();
    Serial.println("[SSP] NOD_YES");
  } else if (cmd == "NOD_NO") {
    nodNo();
    Serial.println("[SSP] NOD_NO");
  } else if (cmd == "STOP") {
    stopMotors();
    Serial.println("[SSP] STOP");
  } else if (cmd.length() > 0) {
    Serial.print("[SSP] Unknown command: ");
    Serial.println(cmd);
  }
}

void loop() {
  while (Serial.available()) {
    char incoming = Serial.read();
    if (incoming == '\r') {
      continue;
    }

    if (incoming == '\n') {
      processCommand(lineBuffer);
      lineBuffer = "";
    } else {
      lineBuffer += incoming;
    }
  }
}
