import flet as ft
import serial
import threading

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)


def update_button_styles(button_group, active_button):
    for btn in button_group:
        btn.bgcolor = ft.Colors.BLUE if btn == active_button else None
        btn.update()


def start_motor(motor_id, buttons):
    ser.write(f'START {motor_id - 1}\n'.encode())
    update_button_styles(buttons, buttons[0])


def stop_motor(motor_id, buttons):
    ser.write(f'STOP {motor_id - 1}\n'.encode())
    update_button_styles(buttons, buttons[1])


def set_direction(motor_id, direction, buttons):
    ser.write(f'DIRECTION {motor_id - 1} {direction}\n'.encode())
    update_button_styles(buttons, buttons[0] if direction == "LEFT" else buttons[1])


def set_speed(motor_id, speed):
    try:
        speed_value = int(speed)
        if speed_value > 0:
            ser.write(f'SPEED {motor_id - 1} {speed_value}\n'.encode())
    except ValueError:
        print("Invalid speed value.")


def set_threshold(threshold):
    try:
        threshold_value = int(threshold)
        ser.write(f'THRESHOLD {threshold_value}\n'.encode())
    except ValueError:
        print("Invalid threshold value.")


def create_motor_control(motor_id):
    speed_input = ft.TextField(label="Скорость", color=ft.Colors.WHITE, border=ft.InputBorder.OUTLINE)
    confirm_btn = ft.ElevatedButton("Подтвердить", on_click=lambda e: set_speed(motor_id, speed_input.value))

    start_btn = ft.ElevatedButton("Старт", on_click=lambda e: start_motor(motor_id, start_stop_buttons))
    stop_btn = ft.ElevatedButton("Стоп", on_click=lambda e: stop_motor(motor_id, start_stop_buttons))
    left_btn = ft.ElevatedButton("Влево", on_click=lambda e: set_direction(motor_id, "LEFT", direction_buttons))
    right_btn = ft.ElevatedButton("Вправо", on_click=lambda e: set_direction(motor_id, "RIGHT", direction_buttons))

    start_stop_buttons = [start_btn, stop_btn]
    direction_buttons = [left_btn, right_btn]

    return ft.Container(
        content=ft.Column([
            ft.Text(f"Мотор {motor_id}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(ft.Row(start_stop_buttons, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                         border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                                          right=ft.BorderSide(2, ft.Colors.WHITE),
                                          bottom=ft.BorderSide(2, ft.Colors.WHITE)), border_radius=5, padding=5),
            ft.Container(ft.Row(direction_buttons, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                         border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                                          right=ft.BorderSide(2, ft.Colors.WHITE),
                                          bottom=ft.BorderSide(2, ft.Colors.WHITE)), border_radius=5, padding=5),
            ft.Container(ft.Row([speed_input, confirm_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                         border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                                          right=ft.BorderSide(2, ft.Colors.WHITE),
                                          bottom=ft.BorderSide(2, ft.Colors.WHITE)), border_radius=5, padding=5)
        ], spacing=5),
        padding=10,
        border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                         right=ft.BorderSide(2, ft.Colors.WHITE), bottom=ft.BorderSide(2, ft.Colors.WHITE)),
        border_radius=10,
        bgcolor=ft.Colors.BLACK
    )


def read_serial_data(label):
    while True:
        try:
            data = ser.readline().decode().strip()
            if data.startswith("DISTANCE"):
                distance = data.split(" ")[1]
                label.value = f"Расстояние: {distance} см"
                label.update()
        except:
            continue


def main(page: ft.Page):
    page.title = "Step Motor Control"
    page.bgcolor = ft.Colors.BLACK

    distance_label = ft.Text("Расстояние: -- см", size=20, color=ft.Colors.WHITE)
    threshold_input = ft.TextField(label="Пороговое расстояние", color=ft.Colors.WHITE, border=ft.InputBorder.OUTLINE)
    threshold_button = ft.ElevatedButton("Задать порог", on_click=lambda e: set_threshold(threshold_input.value))

    threshold_container = ft.Container(
        content=ft.Column([
            threshold_input,
            threshold_button
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        padding=10,
        border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                         right=ft.BorderSide(2, ft.Colors.WHITE), bottom=ft.BorderSide(2, ft.Colors.WHITE)),
        border_radius=10,
        bgcolor=ft.Colors.GREY_900
    )

    motor_controls = ft.Row([
        create_motor_control(1),
        create_motor_control(2),
        create_motor_control(3),
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Container(
            content=ft.Column([
                motor_controls,
                distance_label,
                threshold_container
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            border=ft.Border(left=ft.BorderSide(2, ft.Colors.WHITE), top=ft.BorderSide(2, ft.Colors.WHITE),
                             right=ft.BorderSide(2, ft.Colors.WHITE), bottom=ft.BorderSide(2, ft.Colors.WHITE)),
            border_radius=15,
            bgcolor=ft.Colors.GREY_900,
            alignment=ft.alignment.center
        )
    )

    threading.Thread(target=read_serial_data, args=(distance_label,), daemon=True).start()


ft.app(target=main)
