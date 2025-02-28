#include <Arduino.h>

const int stepPins[3] = {3, 5, 7}; // Пины для шага
const int dirPins[3] = {4, 6, 8}; // Пины для направления
const int trigPin = 9; // Пин триггера датчика
const int echoPin = 10; // Пин эхо датчика

int speeds[3] = {1000, 1000, 1000}; // Скорости по умолчанию (в микросекундах между шагами)
bool motorRunning[3] = {false, false, false}; // Флаги для проверки запущены ли двигатели
bool motorDirection[3] = {true, true, true}; // Направление вращения (true - вправо, false - влево)
int thresholdDistance = 5000; // Пороговое расстояние в см
int lastValidDistance = 0; // Последнее корректное расстояние

unsigned long lastSensorRead = 0;
unsigned long lastStepTime[3] = {0, 0, 0};

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(dirPins[i], OUTPUT);
    pinMode(stepPins[i], OUTPUT);
  }
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000); // Ограничение ожидания 30 мс
  
  if (duration == 0) {
    return lastValidDistance; // Если нет отклика, возвращаем последнее корректное значение
  }
  
  lastValidDistance = duration * 0.034 / 2; // Перевод в сантиметры
  return lastValidDistance;
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastSensorRead >= 40) { // Читаем датчик каждые 50 мс
    int distance = getDistance();
    Serial.println("DISTANCE " + String(distance));
    lastSensorRead = currentMillis;

    if (distance >= thresholdDistance) {
      for (int i = 0; i < 3; i++) {
        motorRunning[i] = false;
      }
    }
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command.startsWith("START")) {
      int motor_id = command.charAt(6) - '0';
      motorRunning[motor_id] = true;
    } else if (command.startsWith("STOP")) {
      int motor_id = command.charAt(5) - '0';
      motorRunning[motor_id] = false;
    } else if (command.startsWith("DIRECTION")) {
      int motor_id = command.charAt(10) - '0';
      String direction = command.substring(12);
      motorDirection[motor_id] = (direction == "RIGHT");
      digitalWrite(dirPins[motor_id], motorDirection[motor_id] ? HIGH : LOW);
    } else if (command.startsWith("SPEED")) {
      int first_space = command.indexOf(' ');
      int second_space = command.indexOf(' ', first_space + 1);
      
      if (first_space != -1 && second_space != -1) {
        int motor_id = command.substring(first_space + 1, second_space).toInt();
        int speed_value = command.substring(second_space + 1).toInt();

        if (motor_id >= 0 && motor_id < 3 && speed_value > 0) {
          speeds[motor_id] = speed_value;
          Serial.println("Motor " + String(motor_id) + " speed set to " + String(speeds[motor_id]));
        }
      }
    } else if (command.startsWith("THRESHOLD")) {
      thresholdDistance = command.substring(9).toInt();
    }
  }

  for (int i = 0; i < 3; i++) {
    if (motorRunning[i] && (micros() - lastStepTime[i] >= speeds[i])) {
      digitalWrite(stepPins[i], HIGH);
      delayMicroseconds(0);
      digitalWrite(stepPins[i], LOW);
      lastStepTime[i] = micros();
    }
  }
}