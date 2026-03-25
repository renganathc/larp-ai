#pragma once

#include <Servo.h>
#include <Arduino.h>

const int HEAD_SERVO_PIN = 13;
const int HEAD_UP_ANGLE = 130;
const int HEAD_DOWN_ANGLE = 50;
const int HEAD_CENTER_ANGLE = 90;

Servo headServo;

void servo_setup();
void headUp();
void headDown();
void headCenter();
void headLeft();
void headRight();
void nodYes();
void nodNo();

void servo_setup() {
  headServo.attach(HEAD_SERVO_PIN);
  headCenter();
}

void headUp() {
  headServo.write(HEAD_UP_ANGLE);
}

void headDown() {
  headServo.write(HEAD_DOWN_ANGLE);
}

void headCenter() {
  headServo.write(HEAD_CENTER_ANGLE);
}

void headLeft() {
  headServo.write(HEAD_CENTER_ANGLE);
}

void headRight() {
  headServo.write(HEAD_CENTER_ANGLE);
}

void nodYes() {
  headServo.write(HEAD_DOWN_ANGLE + 10);
  delay(220);
  headServo.write(HEAD_UP_ANGLE - 10);
  delay(220);
  headCenter();
}

void nodNo() {
  headServo.write(HEAD_CENTER_ANGLE + 20);
  delay(180);
  headServo.write(HEAD_CENTER_ANGLE - 20);
  delay(180);
  headCenter();
}
