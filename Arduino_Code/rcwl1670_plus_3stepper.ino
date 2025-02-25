const int trigPin = 9;
const int echoPin = 10;

// Пины управления для двигателя 1
const int stepPin1 = 2;
const int dirPin1 = 3;
//const int enablePin1 = 4; // Убрали enablePin

// Пины управления для двигателя 2
const int stepPin2 = 5;
const int dirPin2 = 6;
//const int enablePin2 = 7; // Убрали enablePin

// Пины управления для двигателя 3
const int stepPin3 = 11;
const int dirPin3 = 12;
//const int enablePin3 = 13; // Убрали enablePin

// Настройка количества шагов на оборот (зависит от двигателя и настроек микрошага DM542)
const int stepsPerRevolution = 200; // Пример: 200 шагов на оборот (без микрошага)

// Определяем переменные
long duration;
int distance;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Настраиваем пины шаговых двигателей как выходы
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  //pinMode(enablePin1, OUTPUT); // Убрали enablePin

  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  //pinMode(enablePin2, OUTPUT); // Убрали enablePin

  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin3, OUTPUT);
  //pinMode(enablePin3, OUTPUT); // Убрали enablePin

  // Включаем драйверы (если используем enablePin) - ТЕПЕРЬ ЭТО НЕ НУЖНО
  //digitalWrite(enablePin1, LOW); // Optional
  //digitalWrite(enablePin2, LOW); // Optional
  //digitalWrite(enablePin3, LOW); // Optional

  Serial.println("Starting");
}

void loop() {
  // 1. Измерение расстояния
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.println(distance);

  // 2. Выбор двигателя для активации в зависимости от расстояния
  if (distance < 20) {
    activateMotor(1); // Активируем двигатель 1
  } else if (distance >= 21 && distance <= 40) {
    activateMotor(2); // Активируем двигатель 2
  } else if (distance >= 41 && distance <= 60) {
    activateMotor(3); // Активируем двигатель 3
  } else {
    deactivateAllMotors(); // Выключаем все двигатели
  }

  delay(100);
}

// Функция для активации одного двигателя
void activateMotor(int motorNumber) {
  deactivateAllMotors(); // Сначала выключаем все двигатели

  int stepPin;
  int dirPin;

  switch (motorNumber) {
    case 1:
      stepPin = stepPin1;
      dirPin = dirPin1;
      break;
    case 2:
      stepPin = stepPin2;
      dirPin = dirPin2;
      break;
    case 3:
      stepPin = stepPin3;
      dirPin = dirPin3;
      break;
    default:
      return; // Ничего не делаем, если номер двигателя недействителен
  }

  // Вращаем двигатель на небольшое количество шагов (например, 200)
  for (int i = 0; i < 200; i++) { //200 это количество шагов
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500); // Скорость вращения (уменьшите для увеличения скорости)
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
}

// Функция для выключения всех двигателей
void deactivateAllMotors() {
  digitalWrite(stepPin1, LOW);
  digitalWrite(stepPin2, LOW);
  digitalWrite(stepPin3, LOW);
}
