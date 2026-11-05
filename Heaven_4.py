"""Heaven_4.py — заезд №4."""
from Base import *


def run_4():
    """Заезд №4"""
    print_battery()

    drive(530, start_speed=30, max_speed=60, end_speed=30, decel_mm=150, accel_rate=3)
    turn_by(93, max_power=60)
    drive(500, start_speed=40, max_speed=80, end_speed=40, decel_mm=120, accel_rate=3)
    drive(100, start_speed=60, max_speed=80, end_speed=60, decel_mm=0, accel_rate=3)
    drive(-100, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(-55, max_power=60)
    drive(300, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(55, max_power=60)
    drive(200, start_speed=40, max_speed=80, end_speed=40, decel_mm=0, accel_rate=3)
    turn_by(60, max_power=60)
    drive(1500, start_speed=40, max_speed=80, end_speed=40, decel_mm=1120, accel_rate=3)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_4()
