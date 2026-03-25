#pragma once

#include <Arduino.h>

// Left motor controller pins
const int LEFT_A_IN1 = 16;
const int LEFT_A_IN2 = 17;
const int LEFT_A_PWM = 4;
const int LEFT_B_IN1 = 18;
const int LEFT_B_IN2 = 19;
const int LEFT_B_PWM = 5;

// Right motor controller pins
const int RIGHT_A_IN1 = 21;
const int RIGHT_A_IN2 = 22;
const int RIGHT_A_PWM = 2;
const int RIGHT_B_IN1 = 23;
const int RIGHT_B_IN2 = 25;
const int RIGHT_B_PWM = 15;

const int PWM_FREQUENCY = 20000;
const int PWM_RESOLUTION = 8;
const int LEFT_A_CHANNEL = 0;
const int LEFT_B_CHANNEL = 1;
const int RIGHT_A_CHANNEL = 2;
const int RIGHT_B_CHANNEL = 3;

void motor_setup();
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void turn180();
void turn360();
void stopMotors();

static void setMotor(int pwmChannel, int in1Pin, int in2Pin, int speed, bool forward) {
  digitalWrite(in1Pin, forward ? HIGH : LOW);
  digitalWrite(in2Pin, forward ? LOW : HIGH);
  ledcWrite(pwmChannel, speed);
}

static void setSide(int pwmSpeed, bool forward, bool isRightSide) {
  if (isRightSide) {
    setMotor(RIGHT_A_CHANNEL, RIGHT_A_IN1, RIGHT_A_IN2, pwmSpeed, forward);
    setMotor(RIGHT_B_CHANNEL, RIGHT_B_IN1, RIGHT_B_IN2, pwmSpeed, forward);
  } else {
    setMotor(LEFT_A_CHANNEL, LEFT_A_IN1, LEFT_A_IN2, pwmSpeed, forward);
    setMotor(LEFT_B_CHANNEL, LEFT_B_IN1, LEFT_B_IN2, pwmSpeed, forward);
  }
}

void motor_setup() {
  pinMode(LEFT_A_IN1, OUTPUT);
  pinMode(LEFT_A_IN2, OUTPUT);
  pinMode(LEFT_B_IN1, OUTPUT);
  pinMode(LEFT_B_IN2, OUTPUT);
  pinMode(RIGHT_A_IN1, OUTPUT);
  pinMode(RIGHT_A_IN2, OUTPUT);
  pinMode(RIGHT_B_IN1, OUTPUT);
  pinMode(RIGHT_B_IN2, OUTPUT);

  ledcSetup(LEFT_A_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);
  ledcSetup(LEFT_B_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);
  ledcSetup(RIGHT_A_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);
  ledcSetup(RIGHT_B_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);

  ledcAttachPin(LEFT_A_PWM, LEFT_A_CHANNEL);
  ledcAttachPin(LEFT_B_PWM, LEFT_B_CHANNEL);
  ledcAttachPin(RIGHT_A_PWM, RIGHT_A_CHANNEL);
  ledcAttachPin(RIGHT_B_PWM, RIGHT_B_CHANNEL);

  stopMotors();
}

void moveForward() {
  setSide(220, true, false);
  setSide(220, true, true);
}

void moveBackward() {
  setSide(220, false, false);
  setSide(220, false, true);
}

void turnLeft() {
  setSide(140, true, false);
  setSide(220, true, true);
}

void turnRight() {
  setSide(220, true, false);
  setSide(140, true, true);
}

void turn180() {
  setSide(220, true, false);
  setSide(220, false, true);
  delay(800);
  stopMotors();
}

void turn360() {
  setSide(220, true, false);
  setSide(220, false, true);
  delay(1600);
  stopMotors();
}

void stopMotors() {
  setSide(0, true, false);
  setSide(0, true, true);
}
