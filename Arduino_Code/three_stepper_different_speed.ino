// Константы
const int pulsePin1 = 2; // Пин для первого двигателя
const int pulsePin2 = 3; // Пин для второго двигателя
const int pulsePin3 = 4; // Пин для третьего двигателя

const int stepDelay = 1000; // Задержка между шагами в микросекундах
const int initialRuntime = 5000; // Время работы всех двигателей в начале (5 секунд)
const int stopTime = 2000; // Время остановки (2 секунды)
const int sequenceTime = 3000; // Время работы каждого этапа последовательности (3 секунды)

// Переменные для скорости
int speed1 = stepDelay;
int speed2 = stepDelay * 0.7; // На 30% быстрее первого
int speed3 = stepDelay * 0.49; // На 30% быстрее второго

// Установка
void setup() {
  pinMode(pulsePin1, OUTPUT);
  pinMode(pulsePin2, OUTPUT);
  pinMode(pulsePin3, OUTPUT);
}

// Главная функция
void loop() {
  // Вращение всех двигателей
  runMotors(speed1, speed1, speed1, initialRuntime);
  
  // Остановка
  delay(stopTime);

  // Запуск первого двигателя
  runMotor(pulsePin1, speed1, sequenceTime);

  // Запуск второго двигателя
  runMotor(pulsePin2, speed2, sequenceTime);

  // Запуск третьего двигателя
  runMotor(pulsePin3, speed3, sequenceTime);

  // Вращение всех двигателей
  runMotors(speed1, speed2, speed3, sequenceTime);

  // Отключение первого двигателя и замедление остальных
  runMotors(0, speed1, speed2, sequenceTime);

  // Отключение второго двигателя и замедление третьего
  runMotors(0, 0, speed1, sequenceTime);

  // Отключение третьего двигателя
  runMotors(0, 0, 0, sequenceTime);

  // Конец цикла, можно добавить дополнительную логику или сделать повтор
  while(true);
}

// Функция для вращения одного двигателя
void runMotor(int pulsePin, int delayTime, int runTime) {
  unsigned long startTime = millis();
  while (millis() - startTime < runTime) {
    digitalWrite(pulsePin, HIGH);
    delayMicroseconds(delayTime / 2);
    digitalWrite(pulsePin, LOW);
    delayMicroseconds(delayTime / 2);
  }
}

// Функция для вращения трех двигателей одновременно
void runMotors(int delayTime1, int delayTime2, int delayTime3, int runTime) {
  unsigned long startTime = millis();
  while (millis() - startTime < runTime) {
    if (delayTime1 > 0) {
      digitalWrite(pulsePin1, HIGH);
      delayMicroseconds(delayTime1 / 2);
      digitalWrite(pulsePin1, LOW);
      delayMicroseconds(delayTime1 / 2);
    }
    if (delayTime2 > 0) {
      digitalWrite(pulsePin2, HIGH);
      delayMicroseconds(delayTime2 / 2);
      digitalWrite(pulsePin2, LOW);
      delayMicroseconds(delayTime2 / 2);
    }
    if (delayTime3 > 0) {
      digitalWrite(pulsePin3, HIGH);
      delayMicroseconds(delayTime3 / 2);
      digitalWrite(pulsePin3, LOW);
      delayMicroseconds(delayTime3 / 2);
    }
  }
}