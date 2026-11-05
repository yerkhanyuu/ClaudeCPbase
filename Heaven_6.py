"""Heaven_6.py — заезд №6."""
from Base import *


def run_6():
    """Заезд №6"""
    print_battery()
    drive(310, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=3)
    left_att_run(50, 100)
    drive(-150, start_speed=30, max_speed=60, end_speed=30, decel_mm=90, accel_rate=2)
    turn_by(7, max_power=30)
    left_att_run(50, -150)
    turn_by(10, max_power=30)
    drive(-150, start_speed=30, max_speed=60, end_speed=30, decel_mm=90, accel_rate=2)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_6()
