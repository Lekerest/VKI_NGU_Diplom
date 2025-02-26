// Пины для управления шаговыми двигателями
const int motorPins[3][2] = {
  {2, 3},  // Мотор 1: DIR = D2, STEP = D3
  {4, 5},  // Мотор 2: DIR = D4, STEP = D5
  {6, 7}   // Мотор 3: DIR = D6, STEP = D7
};

// Пины для ультразвукового датчика
const int trigPin = 8;  // Trig = D8
const int echoPin = 9;  // Echo = D9

// Переменные для хранения состояния моторов
int motorSteps[3] = {0, 0, 0};  // Счетчик шагов для каждого мотора
int motorSpeed[3] = {1000, 1000, 1000};  // Задержка между шагами (скорость)
bool motorDirection[3] = {true, true, true};  // Направление вращения (true = вправо)
bool motorRunning[3] = {false, false, false};  // Состояние мотора (работает/остановлен)

// Переменные для ультразвукового датчика
float distance = 0;  // Текущее расстояние

void setup() {
  // Инициализация последовательного порта
  Serial.begin(9600);

  // Настройка пинов для моторов
  for (int i = 0; i < 3; i++) {
    pinMode(motorPins[i][0], OUTPUT);  // DIR
    pinMode(motorPins[i][1], OUTPUT);  // STEP
  }

  // Настройка пинов для ультразвукового датчика
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Обработка команд от интерфейса
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }

  // Управление моторами
  for (int i = 0; i < 3; i++) {
    if (motorRunning[i]) {
      stepMotor(i);
    }
  }

  // Чтение расстояния с датчика
  distance = readDistance();
  Serial.println("DISTANCE:" + String(distance));
}

// Функция для обработки команд от интерфейса
void processCommand(String command) {
  if (command.startsWith("MOTOR")) {
    int motorIndex = command.charAt(5) - '0';  // Номер мотора (0, 1, 2)
    if (command.startsWith("MOTOR_DIR")) {
      // Установка направления
      motorDirection[motorIndex] = command.charAt(9) == '1';
      digitalWrite(motorPins[motorIndex][0], motorDirection[motorIndex] ? HIGH : LOW);
    } else if (command.startsWith("MOTOR_SPEED")) {
      // Установка скорости
      motorSpeed[motorIndex] = command.substring(11).toInt();
    } else if (command.startsWith("MOTOR_STOP")) {
      // Остановка мотора
      motorRunning[motorIndex] = false;
    } else if (command.startsWith("MOTOR_START")) {
      // Запуск мотора
      motorRunning[motorIndex] = true;
    }
  }
}

// Функция для выполнения шага мотора
void stepMotor(int motorIndex) {
  digitalWrite(motorPins[motorIndex][1], HIGH);
  delayMicroseconds(motorSpeed[motorIndex]);
  digitalWrite(motorPins[motorIndex][1], LOW);
  delayMicroseconds(motorSpeed[motorIndex]);
  motorSteps[motorIndex]++;
}

// Функция для чтения расстояния с ультразвукового датчика
float readDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;  // Расстояние в см
}