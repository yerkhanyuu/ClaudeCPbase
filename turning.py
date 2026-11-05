"""
turning.py — повороты по гироскопу: turn_to (абсолютный курс) и turn_by
(относительно целевого курса).
"""
from pybricks.tools import wait, StopWatch

from config import (
    RIGHT, TURN_K1, TURN_K2, TURN_MAX_POWER,
    TURN_MIN_POWER_SPOT, TURN_MIN_POWER_PIVOT,
    TURN_TOLERANCE, TURN_TIMEOUT_MS
)
from robot import (
    hub, state, drive_base,
    left_drive_motor, right_drive_motor,
    set_heading, wrap180, timeout_warn
)


def turn_core(goal, pivot, k1, k2, max_power, min_power, tolerance, timeout_ms):
    """
    Ядро поворота (LQR: ошибка угла + скорость вращения).
    goal — НЕПРЕРЫВНЫЙ целевой курс в шкале hub.imu.heading() (может быть > 360).
    """
    if min_power is None:
        min_power = TURN_MIN_POWER_SPOT if pivot is None else TURN_MIN_POWER_PIVOT

    timer = StopWatch()
    timer.reset()

    while True:
        err = goal - hub.imu.heading()
        gyro_z = hub.imu.angular_velocity()[2]
        in_tolerance = abs(err) < tolerance

        if in_tolerance:
            # внутри допуска не толкаем мотор min_power-ом — просто тормозим
            left_drive_motor.brake()
            right_drive_motor.brake()
        else:
            power = k1 * err + k2 * gyro_z
            power = max(-max_power, min(max_power, power))
            if abs(power) < min_power:
                power = min_power if power > 0 else -min_power

            if pivot is None:
                left_drive_motor.dc(power)
                right_drive_motor.dc(-power)
            elif pivot == RIGHT:
                left_drive_motor.dc(power)
                right_drive_motor.hold()
            else:
                left_drive_motor.hold()
                right_drive_motor.dc(-power)

        if in_tolerance and abs(gyro_z) < 2.0:
            break
        if timer.time() > timeout_ms:
            timeout_warn("turn")
            break

        wait(5)

    if pivot is None:
        left_drive_motor.hold()
        right_drive_motor.hold()
    else:
        drive_base.brake()
    wait(50)  # гашение инерции корпуса

    # запоминаем ЦЕЛЬ (а не фактический курс): недоворот исправит следующий drive()
    state.heading_target = goal


def turn_to(
    angle,
    pivot=None,
    k1=TURN_K1,
    k2=TURN_K2,
    max_power=TURN_MAX_POWER,
    min_power=None,
    tolerance=TURN_TOLERANCE,
    timeout_ms=TURN_TIMEOUT_MS,
    reset_gyro=False
):
    """
    Поворот на АБСОЛЮТНЫЙ курс по кратчайшему пути.

    angle      — курс в градусах (+ по часовой). 0 = направление, заданное
                 set_heading(0) в начале заезда. 270 и -90 — одно и то же.
                 Ровно 180° от текущего — крутит по часовой.
    pivot      — None: на месте. RIGHT / LEFT: вокруг этого колеса (оно стоит)
    min_power  — минимальная мощность (по умолчанию из config)
    tolerance  — допустимая ошибка в градусах
    reset_gyro — True: СТАРЫЙ режим — обнулить курс и повернуть на angle градусов
                 от текущего направления, без поиска кратчайшего пути

    Примеры:
        set_heading(0)                # один раз в начале заезда
        turn_to(90)                   # смотреть на 90°
        turn_to(0)                    # вернуться на исходный курс
        turn_to(90, pivot=RIGHT)      # на 90° вокруг правого колеса
    """
    if reset_gyro:
        set_heading(0)
        goal = angle
    else:
        current = hub.imu.heading()
        delta = (angle - current) % 360
        if delta > 180:
            delta -= 360
        goal = current + delta

    turn_core(goal, pivot, k1, k2, max_power, min_power, tolerance, timeout_ms)


def turn_by(
    delta,
    pivot=None,
    k1=TURN_K1,
    k2=TURN_K2,
    max_power=TURN_MAX_POWER,
    min_power=None,
    tolerance=TURN_TOLERANCE,
    timeout_ms=TURN_TIMEOUT_MS
):
    """
    Поворот НА delta градусов от целевого курса (а не от фактического).
    + по часовой, - против; знак delta соблюдается, так что turn_by(180) всегда
    идёт по часовой, а turn_by(-180) — против.
    Ошибки не копятся: четыре turn_by(90) подряд дают ровно один оборот.

    Примеры:
        turn_by(90)      # повернуть направо
        turn_by(-90)     # повернуть налево
    """
    current = hub.imu.heading()
    base = current + wrap180(state.heading_target - current)  # ближайший "виток" цели
    turn_core(base + delta, pivot, k1, k2, max_power, min_power, tolerance, timeout_ms)
