"""Heaven_8.py — заезд №8."""
from Base import *


def run_8():
    """Заезд №8"""
    print_battery()
    drive(800, start_speed=30, max_speed=60, end_speed=30, decel_mm=0, accel_rate=2)


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_8()
