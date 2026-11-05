"""Heaven_9.py — заезд №9."""
from Base import *


def run_9():
    """Заезд №9 (пока пустой)"""
    print_battery()
    # TODO: сюда напишешь новый заезд.
    # Ниже — старый код этого заезда, закомментирован, чтобы не потерять:
    # drive(480, start_speed=30, max_speed=60, end_speed=30, decel_mm=100, accel_rate=3)
    # left_att_run(50, 150)
    # left_att_run(50, -140)
    # drive(-500, start_speed=30, max_speed=60, end_speed=30, decel_mm=440, accel_rate=2)
    pass


# Тестовый запуск: работает только если запустить ИМЕННО этот файл
# (из mainHeaven.py этот блок не выполняется).
if __name__ == "__main__":
    set_heading(0)  # задаём нулевой курс перед стартом, как это делает меню
    run_9()
