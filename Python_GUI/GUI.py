import flet as ft
import serial
import threading
import time

class MotorControlApp:
    def __init__(self, page: ft.Page):
        # Инициализация главной страницы приложения
        self.page = page
        self.page.title = "Управление Nema17"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.padding = 20

        # Состояние приложения
        self.distance_value = 0              # Текущее расстояние с датчика
        self.motor_steps = [0, 0, 0]         # Счетчик шагов для каждого мотора
        self.stop_distance_threshold = 0     # Порог остановки по расстоянию
        self.logs = []                       # История логов
        self.motor_directions = [True, True, True]  # Направления моторов (True - вправо)

        # Конфигурация пинов Arduino для моторов (Pulse, Direction)
        self.motor_pins = [
            ("D2", "D3"),  # Мотор 1
            ("D4", "D5"),  # Мотор 2
            ("D6", "D7")   # Мотор 3
        ]

        # Подключение к Arduino
        self.arduino_connected = False
        try:
            self.arduino = serial.Serial('COM3', 9600, timeout=1)
            self.arduino_connected = True
        except serial.SerialException:
            self.logs.append(ft.Text("Arduino не подключен. Проверьте соединение."))

        # Инициализация элементов интерфейса
        self.distance = ft.Text("Расстояние: Н/Д", size=18, weight=ft.FontWeight.BOLD)
        self.stop_distance = ft.TextField(label="Остановить на расстоянии (см)", width=300)
        self.log_output = ft.Column(scroll="always", height=200)  # Контейнер для логов
        self.chart = ft.LineChart()          # График расстояния
        self.motor_frames = []               # Контейнеры для блоков моторов

        # Построение интерфейса
        self.init_ui()

        # Запуск потока для чтения данных с Arduino
        if self.arduino_connected:
            self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.serial_thread.start()

    def init_ui(self):
        # Создание интерфейсных блоков для каждого мотора
        for i in range(3):
            motor_frame = ft.Container(
                content=ft.Column(
                    [
                        # Заголовок с пинами
                        ft.Text(f"Мотор {i+1} (Pulse: {self.motor_pins[i][0]}, Dir: {self.motor_pins[i][1]})", 
                               size=16, weight=ft.FontWeight.BOLD),
                        
                        # Блок управления направлением
                        ft.Row(
                            [
                                ft.Text("Направление:", size=14),
                                # Кнопки направления с цветовой индикацией
                                ft.ElevatedButton(
                                    "Вправо",
                                    on_click=lambda e, i=i: self.toggle_motor(e, i, True),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE if self.motor_directions[i] else None)
                                ),
                                ft.ElevatedButton(
                                    "Влево",
                                    on_click=lambda e, i=i: self.toggle_motor(e, i, False),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE if not self.motor_directions[i] else None)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        
                        # Блок управления скоростью
                        ft.Row(
                            [
                                ft.Text("Скорость:", size=14),
                                ft.TextField(
                                    label="Шагов/сек", 
                                    width=100, 
                                    on_change=lambda e, i=i: self.set_speed(e, i, e.control.value)
                                ),
                                ft.ElevatedButton(
                                    "Стоп", 
                                    on_click=lambda e, i=i: self.stop_motor(e, i)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        
                        # Счетчик шагов
                        ft.Text(f"Шаги: {self.motor_steps[i]}", size=14),
                    ],
                    spacing=10,
                ),
                padding=10,
                border=ft.border.all(2, ft.Colors.BLUE),
                border_radius=10,
                width=300,
            )
            self.motor_frames.append(motor_frame)

        # Настройка графика расстояния
        self.chart.data = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i, 0) for i in range(20)],
                color=ft.Colors.BLUE,
                stroke_width=2,
                curved=True
            )
        ]
        self.chart.height = 300
        self.chart.width = 800
        self.chart.bottom_axis = ft.ChartAxis(title=ft.Text("Время"), title_size=14, labels_size=12)
        self.chart.left_axis = ft.ChartAxis(title=ft.Text("Расстояние (см)"), title_size=14, labels_size=12)

        # Сборка всех элементов на странице
        self.page.add(
            ft.Column(
                [
                    ft.Text("Управление моторами", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row(self.motor_frames, spacing=20),
                    ft.Divider(height=20),
                    ft.Text("Управление расстоянием", size=20, weight=ft.FontWeight.BOLD),
                    self.distance,
                    self.stop_distance,
                    ft.ElevatedButton("Установить порог остановки", on_click=self.set_stop_distance),
                    ft.Divider(height=20),
                    ft.Text("График расстояния", size=20, weight=ft.FontWeight.BOLD),
                    self.chart,
                    ft.Divider(height=20),
                    ft.Text("Логи", size=20, weight=ft.FontWeight.BOLD),
                    self.log_output,
                ],
                spacing=10,
            )
        )

    # Отправка команд на Arduino
    def send_command(self, command):
        if self.arduino_connected:
            try:
                self.arduino.write((command + "\n").encode())
                self.add_log(f"Отправлено: {command}")
            except serial.SerialException as e:
                self.add_log(f"Ошибка отправки: {e}")
        else:
            self.add_log("Arduino не подключен!")

    # Добавление записи в лог
    def add_log(self, message):
        self.logs.append(ft.Text(f"{time.strftime('%H:%M:%S')}: {message}"))
        self.log_output.controls = self.logs.copy()
        self.page.update()

    # Чтение данных из последовательного порта
    def read_serial(self):
        while self.arduino_connected:
            try:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode().strip()
                    if line.startswith("DISTANCE:"):
                        # Обновление значения расстояния
                        self.distance_value = float(line.split(':')[1])
                        self.distance.value = f"Расстояние: {self.distance_value} см"
                        self.update_chart(self.distance_value)
                        self.check_stop_condition()
                        self.page.update()
            except Exception as e:
                self.add_log(f"Ошибка чтения: {e}")
                break

    # Обновление точек на графике
    def update_chart(self, value):
        if len(self.chart.data[0].data_points) > 20:
            self.chart.data[0].data_points.pop(0)
        self.chart.data[0].data_points.append(
            ft.LineChartDataPoint(len(self.chart.data[0].data_points), value)
        )
        self.page.update()

    # Проверка условия остановки по расстоянию
    def check_stop_condition(self):
        if self.stop_distance_threshold > 0 and self.distance_value <= self.stop_distance_threshold:
            for i in range(3):
                self.send_command(f"MOTOR_STOP{i}")
            self.add_log("Все моторы остановлены по достижению порога")

    # Изменение направления мотора
    def toggle_motor(self, e, motor_index, direction):
        self.motor_directions[motor_index] = direction
        self.send_command(f"MOTOR_DIR{motor_index} {1 if direction else 0}")
        self.add_log(f"Мотор {motor_index+1}: направление {'вправо' if direction else 'влево'}")
        self.update_motor_ui(motor_index)

    # Установка скорости мотора
    def set_speed(self, e, motor_index, speed):
        try:
            speed = int(speed)
            self.send_command(f"MOTOR_SPEED{motor_index} {speed}")
            self.add_log(f"Мотор {motor_index+1}: скорость {speed}")
        except ValueError:
            self.add_log("Ошибка! Введите целое число")

    # Экстренная остановка мотора
    def stop_motor(self, e, motor_index):
        self.send_command(f"MOTOR_STOP{motor_index}")
        self.add_log(f"Мотор {motor_index+1}: экстренная остановка")

    # Установка порога остановки
    def set_stop_distance(self, e):
        try:
            self.stop_distance_threshold = float(self.stop_distance.value)
            self.add_log(f"Порог остановки: {self.stop_distance_threshold} см")
        except ValueError:
            self.add_log("Ошибка! Введите число")

    # Обновление цвета кнопок направления
    def update_motor_ui(self, motor_index):
        # Синий цвет для активного направления
        self.motor_frames[motor_index].content.controls[1].controls[1].style = ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE if self.motor_directions[motor_index] else None
        )
        self.motor_frames[motor_index].content.controls[1].controls[2].style = ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE if not self.motor_directions[motor_index] else None
        )
        self.page.update()

# Запуск приложения
ft.app(target=MotorControlApp)
