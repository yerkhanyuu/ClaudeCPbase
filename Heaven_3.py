"""Heaven_3.py — заезд №3."""
from Base import *


def run_3():
    """Заезд №3"""
    print_battery()
    left_att_run(100, -250)

    drive(250, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(-140, max_power=50)
    drive(-460, start_speed=40, max_speed=80, end_speed=40, decel_mm=340, accel_rate=3)
    turn_by(140, max_power=50)
    left_att_run(100, 250)
    drive(180, start_speed=40, max_speed=60, end_speed=40, decel_mm=0, accel_rate=3)
    left_att_run(100, -170)
    left_att_run(100, 170)
    right_att_run(100, 6800)
    right_att_run(100, -1500)
    left_att_run(100, -120)
    drive(20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(-20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(-20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(-20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    drive(20, start_speed=20, max_speed=40, end_speed=20, decel_mm=0, accel_rate=3)
    right_att_run(100, 1500)
    right_att_run(100, -1500)
    drive(-100, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=3)
    turn_by(45, max_power=80)
    drive(-700, start_speed=70, max_speed=100, end_speed=70, decel_mm=580, accel_rate=3)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_3()
