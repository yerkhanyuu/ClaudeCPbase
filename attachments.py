"""
attachments.py — моторы насадок (механизмов): левая насадка (порт A), правая (порт E).
"""
from pybricks.tools import wait, StopWatch

from config import ATT_POWER_TO_SPEED
from robot import left_att_motor, right_att_motor, timeout_warn


# ==============================================================================
# ПОВОРОТ НА УГОЛ (встроенный контроллер мотора)
# ==============================================================================
def left_att_run(power, deg, block=True):
    """Левая насадка на deg градусов. power — "мощность" в процентах (знак = направление)."""
    left_att_motor.run_angle(power * ATT_POWER_TO_SPEED, deg, wait=block)

def right_att_run(power, deg, block=True):
    """Правая насадка на deg градусов. power — "мощность" в процентах (знак = направление)."""
    right_att_motor.run_angle(power * ATT_POWER_TO_SPEED, deg, wait=block)


# ==============================================================================
# УДАР / ПРЯМАЯ МОЩНОСТЬ (dc)
# ==============================================================================
def left_att_dc(power, deg, timeout_ms=2000):
    """Прямая мощность на левую насадку, пока не пройдёт deg градусов."""
    left_att_motor.reset_angle(0)
    timer = StopWatch()
    while abs(left_att_motor.angle()) < deg:
        if timer.time() > timeout_ms:
            timeout_warn("left_att_dc")
            break
        left_att_motor.dc(power)
        wait(2)
    left_att_motor.brake()

def right_att_dc(power, deg, timeout_ms=2000):
    """Прямая мощность на правую насадку, пока не пройдёт deg градусов."""
    right_att_motor.reset_angle(0)
    timer = StopWatch()
    while abs(right_att_motor.angle()) < deg:
        if timer.time() > timeout_ms:
            timeout_warn("right_att_dc")
            break
        right_att_motor.dc(power)
        wait(2)
    right_att_motor.brake()


# ==============================================================================
# ПЛАВНОЕ ДВИЖЕНИЕ ДО УГЛА (PD)
# ==============================================================================
def left_att_pd(deg, forward=True, kp=2, kd=1.2, timeout_ms=2000, tolerance=1, min_power=20):
    """
    Левая насадка до угла deg по PD (мощность dc).
    forward=True — в положительную сторону, False — в отрицательную.
    min_power — минимальная мощность, чтобы мотор не залипал у цели.
    """
    left_att_motor.reset_angle(0)
    last_error = deg
    timer = StopWatch()
    while True:
        error = deg - abs(left_att_motor.angle())
        if error <= tolerance:
            break
        if timer.time() > timeout_ms:
            timeout_warn("left_att_pd")
            break
        derivative = error - last_error
        last_error = error
        correction = (kp * error) + (kd * derivative)
        correction = max(min_power, min(100, correction))
        left_att_motor.dc(correction if forward else -correction)
        wait(10)
    left_att_motor.brake()

def right_att_pd(deg, max_speed, forward=True, kp=2, kd=1.2, timeout_ms=2000, tolerance=1, min_speed=60):
    """
    Правая насадка до угла deg по PD со скоростью.
    max_speed — МАКСИМАЛЬНАЯ скорость (град/с), у цели насадка замедляется.
                Если двигается слишком медленно — увеличь kp.
    forward   — True: в положительную сторону, False: в отрицательную.
    """
    right_att_motor.reset_angle(0)
    max_speed = abs(max_speed)
    min_speed = min(min_speed, max_speed)
    last_error = deg
    timer = StopWatch()
    while True:
        error = deg - abs(right_att_motor.angle())
        if error <= tolerance:
            break
        if timer.time() > timeout_ms:
            timeout_warn("right_att_pd")
            break
        derivative = error - last_error
        last_error = error
        cmd = (kp * error) + (kd * derivative)
        cmd = max(min_speed, min(max_speed, cmd))
        right_att_motor.run(cmd if forward else -cmd)
        wait(10)
    right_att_motor.brake()
