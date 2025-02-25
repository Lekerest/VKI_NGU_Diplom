const int stepPin = 2; // Пин, к которому подключен PUL
const int dirPin = 3;  // Пин, к которому подключен DIR (если он используется
void setup() {
  pinMode(stepPin, OUTPUT); // Устанавливаем пин как выход
  pinMode(dirPin, OUTPUT);  // Устанавливаем пин DIR как выход

void loop() {
  // Вращение в одну сторону
  digitalWrite(dirPin, HIGH); // Устанавливаем направление вращения
  for (int i = 0; i < 5000; i++) { // Генерируем 5000 импульсов
    digitalWrite(stepPin, HIGH); // Устанавливаем HIGH для импульса
    delayMicroseconds(1000); // Длительность импульса
    digitalWrite(stepPin, LOW); // Устанавливаем LOW
    delayMicroseconds(1000); // Задержка перед следующим импульсом
  }
  delay(1000); // Задержка на 1 секунду
  // Вращение в другую сторону
  digitalWrite(dirPin, LOW); // Меняем направление вращения
  for (int i = 0; i < 5000; i++) { // Генерируем 5000 импульсов
    digitalWrite(stepPin, HIGH); // Устанавливаем HIGH для импульса
    delayMicroseconds(1000); // Длительность импульса
    digitalWrite(stepPin, LOW); // Устанавливаем LOW
    delayMicroseconds(1000); // Задержка перед следующим импульсом
  }
  delay(1000); // Задержка на 1 секунду
  // Остановка
  while (true); // Останавливаем выполнение программы
}