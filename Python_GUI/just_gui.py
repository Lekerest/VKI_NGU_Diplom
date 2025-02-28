import flet as ft
import serial

# Установите параметры последовательного порта
SERIAL_PORT = 'COM3'  # Замените на ваш порт
BAUD_RATE = 9600

# Инициализация последовательного порта
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

def start_motor(motor_id):
    ser.write(f'START {motor_id - 1}\n'.encode())  # Изменено на motor_id - 1

def stop_motor(motor_id):
    ser.write(f'STOP {motor_id - 1}\n'.encode())  # Изменено на motor_id - 1

def set_direction(motor_id, direction):
    ser.write(f'DIRECTION {motor_id - 1} {direction}\n'.encode())  # Изменено на motor_id - 1

def set_speed(motor_id, speed):
    try:
        speed_value = int(speed)
        if speed_value > 0:  # Проверка, что скорость больше нуля
            ser.write(f'SPEED {motor_id - 1} {speed_value}\n'.encode())  # Изменено на motor_id - 1
        else:
            print("Speed must be greater than zero.")
    except ValueError:
        print("Invalid speed value.")

def create_motor_control(motor_id):
    speed_input = ft.TextField(label="Скорость: От 250", color=ft.Colors.WHITE)  # Поле для ввода скорости
    return ft.Container(
        content=ft.Column([
            ft.Text(f"Мотор {motor_id}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),  # Белый текст
            ft.Row([
                ft.ElevatedButton("Старт", on_click=lambda e: start_motor(motor_id)),
                ft.ElevatedButton("Стоп", on_click=lambda e: stop_motor(motor_id)),
                ft.ElevatedButton("Влево", on_click=lambda e: set_direction(motor_id, "LEFT")),
                ft.ElevatedButton("Вправо", on_click=lambda e: set_direction(motor_id, "RIGHT")),
            ]),
            ft.Row([
                ft.Container(
                    content=speed_input,
                    padding=5,
                    border=ft.Border(
                        left=ft.BorderSide(2, color=ft.Colors.WHITE),
                        top=ft.BorderSide(2, color=ft.Colors.WHITE),
                        right=ft.BorderSide(2, color=ft.Colors.WHITE),
                        bottom=ft.BorderSide(2, color=ft.Colors.WHITE),
                    )  # Белая рамка вокруг поля со скоростью
                ),
                ft.ElevatedButton("Подтвердить", on_click=lambda e: set_speed(motor_id, speed_input.value))  # Кнопка для установки скорости
            ])
        ]),
        padding=10,
        border=ft.Border(
            left=ft.BorderSide(2, color=ft.Colors.WHITE),
            top=ft.BorderSide(2, color=ft.Colors.WHITE),
            right=ft.BorderSide(2, color=ft.Colors.WHITE),
            bottom=ft.BorderSide(2, color=ft.Colors.WHITE),
        ),  # Белая рамка вокруг управления для каждого мотора
        bgcolor=ft.Colors.BLACK  # Черный фон для контейнера
    )

def main(page: ft.Page):
    page.title = "Step Motor Control"
    page.bgcolor = ft.Colors.BLACK  # Установка цвета фона страницы на черный

    motor_controls = ft.Column([
        create_motor_control(1),
        create_motor_control(2),
        create_motor_control(3),
    ], alignment=ft.MainAxisAlignment.START)

    page.add(motor_controls)

ft.app(target=main)
