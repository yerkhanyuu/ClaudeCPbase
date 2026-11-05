"""Heaven_2.py — заезд №2."""
from Base import *


def run_2():
    """Заезд №2"""
    print_battery()

    turn_by(53, max_power=80)
    drive(415, start_speed=40, max_speed=60, end_speed=40, decel_mm=35, accel_rate=3)
    right_att_run(20, 120)
    drive(-200, start_speed=10, max_speed=30, end_speed=30, decel_mm=80, accel_rate=3)
    right_att_run(100, 360)
    drive(-200, start_speed=40, max_speed=80, end_speed=40, decel_mm=80, accel_rate=3)
    turn_by(50, max_power=80)
    drive(710, start_speed=40, max_speed=50, end_speed=40, decel_mm=330, accel_rate=3)
    turn_by(-45, max_power=50)
    drive(25, start_speed=40, max_speed=50, end_speed=40, decel_mm=0, accel_rate=3)
    left_att_run(100, -1100)
    turn_by(-20, max_power=50)
    drive(-50, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(-40, max_power=80)
    turn_by(45, max_power=80)
    drive(-800, start_speed=40, max_speed=80, end_speed=40, decel_mm=680, accel_rate=3)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_2()
