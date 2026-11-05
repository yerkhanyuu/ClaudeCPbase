"""Heaven_7.py — заезд №7."""
from Base import *


def run_7():
    """Заезд №7"""
    print_battery()
    drive(360, start_speed=40, max_speed=60, end_speed=40, decel_mm=0, accel_rate=3)
    right_att_run(70, 180)
    wait(1000)
    drive(20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(-20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(-20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(-20, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)
    drive(-500, start_speed=40, max_speed=80, end_speed=40, decel_mm=440, accel_rate=2)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_7()
