"""Heaven_5.py — заезд №5."""
from Base import *


def run_5():
    """Заезд №5"""
    print_battery()

    left_att_run(50, -35, block=False)
    drive(660, start_speed=40, max_speed=70, end_speed=40, decel_mm=280, accel_rate=3)
    turn_by(-90, max_power=80)
    drive(300, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(135, max_power=60)
    drive(90, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=3)
    drive(50, start_speed=10, max_speed=30, end_speed=10, decel_mm=0, accel_rate=3)
    left_att_run(100, -200)
    drive(70, start_speed=10, max_speed=30, end_speed=10, decel_mm=0, accel_rate=3)
    drive(-150, start_speed=40, max_speed=80, end_speed=40, decel_mm=30, accel_rate=3)
    turn_by(49, max_power=60)
    left_att_run(50, 235, block=False)
    drive(400, start_speed=40, max_speed=80, end_speed=40, decel_mm=20, accel_rate=3)
    drive(100, start_speed=10, max_speed=30, end_speed=10, decel_mm=0, accel_rate=3)
    left_att_run(100, -150)
    drive(-100, start_speed=10, max_speed=30, end_speed=10, decel_mm=0, accel_rate=3)
    turn_by(-31, max_power=30)
    drive(90, start_speed=10, max_speed=30, end_speed=10, decel_mm=0, accel_rate=3)
    right_att_run(20, -500)
    right_att_run(100, 360)
    turn_by(30, max_power=30)
    drive(-75, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(-90, max_power=80)
    drive(-700, start_speed=40, max_speed=100, end_speed=100, decel_mm=580, accel_rate=3)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_5()
