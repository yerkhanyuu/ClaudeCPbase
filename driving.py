"""
driving.py — движение базы: езда по гироскопу, упор в стену, ручные манёвры,
движение по линии.

Главная функция — drive(мм). Остальное — для особых случаев.
"""
from pybricks.tools import wait, StopWatch

from config import (
    DRIVE_KP, DRIVE_KI, DRIVE_KD,
    DRIVE_MAX_SPEED, DRIVE_START_SPEED, DRIVE_END_SPEED,
    DRIVE_DECEL_MM, DRIVE_ACCEL_RATE, DRIVE_TIMEOUT_MS
)
from robot import (
    hub, state, drive_base,
    left_drive_motor, right_drive_motor,
    left_color_sensor, right_color_sensor,
    set_heading, mm_to_deg, map_value, wrap180, stop_motors,
    timeout_warn, need_sensor
)

# ==============================================================================
# ЕЗДА ПО ГИРОСКОПУ
# ==============================================================================
def drive_core(
    direction,
    target_heading,
    final_angle,
    start_speed,
    max_speed,
    end_speed,
    decel_start_angle,
    accel_rate,
    kp,
    ki,
    kd,
    stall_stop,
    timeout_ms
):
    """
    Общее ядро езды по гироскопу (используют drive() и старые forward/backward).
    direction: +1 — вперёд, -1 — назад. Скорости передаются как модули (>= 0).
    Углы — в градусах мотора. Гироскоп НЕ сбрасывает.
    """
    state.heading_target = target_heading  # запоминаем, какой курс держим

    left_drive_motor.reset_angle(0)
    right_drive_motor.reset_angle(0)

    left_drive_motor.dc(0)
    right_drive_motor.dc(0)
    wait(10)

    speed = abs(start_speed)
    max_speed = abs(max_speed)
    end_speed = abs(end_speed)
    accel_rate = abs(accel_rate)
    prev_error = 0
    integral = 0

    stopwatch = StopWatch()
    last_movement_time = stopwatch.time()
    moved = False

    while abs(left_drive_motor.angle()) < final_angle:
        now = stopwatch.time()
        if now > timeout_ms:
            timeout_warn("drive")
            break

        left_angle = abs(left_drive_motor.angle())
        remaining_distance = final_angle - left_angle

        if left_angle >= decel_start_angle:
            scale = remaining_distance / max(1, (final_angle - decel_start_angle))
            decel_speed = end_speed + (max_speed - end_speed) * scale
            # на коротких дистанциях скорость не должна скакать вверх
            speed = min(speed, decel_speed)
        elif speed < max_speed:
            speed = min(speed + accel_rate, max_speed)

        error = wrap180(hub.imu.heading() - target_heading)  # кратчайший путь
        integral = max(-100, min(100, integral + error))     # anti-windup
        derivative = error - prev_error
        correction = kp * error + ki * integral + kd * derivative

        if stall_stop:
            # не считаем "упёрся", пока робот ни разу не тронулся
            if abs(left_drive_motor.speed()) > 10:
                last_movement_time = now
                moved = True
            elif (moved or now > 1000) and now - last_movement_time > 200:
                break

        power = direction * speed
        left_drive_motor.dc(power - correction)
        right_drive_motor.dc(power + correction)
        prev_error = error
        wait(5)

    left_drive_motor.hold()
    right_drive_motor.hold()
    wait(50)


def drive(
    mm,
    max_speed=DRIVE_MAX_SPEED,
    start_speed=DRIVE_START_SPEED,
    end_speed=DRIVE_END_SPEED,
    decel_mm=DRIVE_DECEL_MM,
    accel_rate=DRIVE_ACCEL_RATE,
    heading=None,
    reset_gyro=False,
    stall_stop=False,
    timeout_ms=DRIVE_TIMEOUT_MS,
    kp=DRIVE_KP,
    ki=DRIVE_KI,
    kd=DRIVE_KD
):
    """
    ЕДИНАЯ функция езды по прямой с удержанием АБСОЛЮТНОГО курса по гироскопу.

    mm          — расстояние в миллиметрах; ОТРИЦАТЕЛЬНОЕ = назад
    max_speed   — макс. мощность dc (0..100); скорости всегда пиши положительными
    start_speed — мощность на старте
    end_speed   — мощность в конце торможения
    decel_mm    — за сколько мм до цели начинать тормозить
    accel_rate  — прирост мощности за шаг цикла (5 мс)
    heading     — какой курс держать. None (по умолчанию) = целевой курс, который
                  робот помнит (после turn_to — тот, на который повернули, поэтому
                  недоворот автоматически исправится по пути)
    reset_gyro  — True: сначала обнулить курс (режим как в старых заездах)
    stall_stop  — True: остановиться, если упёрся и стоит > 200 мс
    timeout_ms  — максимальное время движения (страховка)

    Примеры:
        drive(500)                     # 50 см вперёд по текущему курсу
        drive(-300, max_speed=50)      # 30 см назад, помедленнее
        drive(400, heading=90)         # ехать, удерживая курс 90 (робот уже смотрит туда)
        drive(200, stall_stop=True)    # ехать до упора (макс. 20 см)
    """
    if reset_gyro:
        set_heading(0)
    if heading is None:
        heading = state.heading_target

    direction = 1 if mm >= 0 else -1
    final_angle = mm_to_deg(abs(mm))
    decel_start_angle = max(0, final_angle - mm_to_deg(decel_mm))
    drive_core(
        direction, heading, final_angle, start_speed, max_speed, end_speed,
        decel_start_angle, accel_rate, kp, ki, kd,
        stall_stop, timeout_ms
    )


# ==============================================================================
# УПОР В СТЕНУ
# ==============================================================================
def align_wall(speed=-60, time_ms=1000, heading=0):
    """
    Выравнивание по стене задним ходом. Останавливается, когда оба мотора
    упёрлись, а не просто по таймеру.
    speed   — мощность dc (-100..100)
    time_ms — максимальное время (страховка)
    heading — какой курс считать правильным, когда робот встал ровно по стене.
              Это "привязка": копившаяся ошибка курса обнуляется. По умолчанию 0.
              В абсолютном режиме передай реальный курс стены.
    """
    speed = max(-100, min(100, speed))
    timer = StopWatch()
    left_drive_motor.dc(speed)
    right_drive_motor.dc(speed)
    wait(250)  # дать роботу тронуться, иначе упор определится сразу
    while timer.time() < time_ms:
        if abs(left_drive_motor.speed()) < 20 and abs(right_drive_motor.speed()) < 20:
            wait(150)  # ещё чуть-чуть дожать, чтобы робот встал ровно
            break
        wait(10)
    stop_motors()
    set_heading(heading)


# ==============================================================================
# РУЧНЫЕ МАНЁВРЫ (разная мощность на колёса: дуги, разворот, толкание)
# После них курс изменился — вызови sync_heading(), если дальше едешь drive().
# ==============================================================================
def move_by_time(left_power, right_power, ms, brake=True):
    """Ехать ms миллисекунд с заданной мощностью (dc) на каждое колесо."""
    timer = StopWatch()
    while timer.time() < ms:
        left_drive_motor.dc(left_power)
        right_drive_motor.dc(right_power)
        wait(5)
    if brake:
        drive_base.brake()

def move_by_deg(left_power, right_power, deg, brake=True, timeout_ms=5000):
    """Ехать, пока среднее колёс не проедет deg градусов."""
    left_drive_motor.reset_angle(0)
    right_drive_motor.reset_angle(0)
    timer = StopWatch()
    while (abs(left_drive_motor.angle()) + abs(right_drive_motor.angle())) / 2 <= deg:
        if timer.time() > timeout_ms:
            timeout_warn("move_by_deg")
            break
        left_drive_motor.dc(left_power)
        right_drive_motor.dc(right_power)
        wait(5)
    if brake:
        drive_base.brake()


# ==============================================================================
# ДВИЖЕНИЕ ПО ЛИНИИ
# ==============================================================================
def follow_line_deg(
    deg,
    base_speed=100,
    kp=0.9,
    kd=3.5,
    target=60,
    max_correction=400,
    stop=True,
    timeout_ms=8000,
    reset_gyro=False
):
    """
    Движение по линии ПРАВЫМ датчиком; дистанция в градусах мотора.
    target         — значение отражения на границе линии
    max_correction — ограничение поправки (град/с)
    stop           — True: в конце затормозить
    reset_gyro     — True: обнулить курс (как в старых заездах). Сам по себе курс
                     здесь не используется, поэтому по умолчанию курс не трогаем.
    """
    sensor = need_sensor(right_color_sensor, "right (Port D)")

    previous_error = 0
    if reset_gyro:
        set_heading(0)
    left_drive_motor.reset_angle(0)
    right_drive_motor.reset_angle(0)
    timer = StopWatch()

    while abs(left_drive_motor.angle()) < deg:
        if timer.time() > timeout_ms:
            timeout_warn("follow_line")
            break

        reflection = sensor.reflection()
        error = target - reflection
        derivative = error - previous_error
        correction = kp * error + kd * derivative

        if correction > max_correction:
            correction = max_correction
        if correction < -max_correction:
            correction = -max_correction

        base = base_speed - abs(error) * 0.3
        if base < 30:
            base = 30

        left_drive_motor.run(base + correction)
        right_drive_motor.run(base - correction)

        previous_error = error
        wait(5)

    if stop:
        drive_base.brake()


def follow_line(mm, **kwargs):
    """То же, что follow_line_deg, но дистанция в миллиметрах."""
    follow_line_deg(mm_to_deg(mm), **kwargs)


def follow_line_2(
    mm,
    accel_mm=200,
    decel_mm=200,
    low_speed=100,
    high_speed=200,
    end_speed=50,
    kp=1.6,
    kd=0.4,
    brake=True,
    timeout_ms=10000
):
    """
    Движение по линии двумя датчиками с разгоном и торможением (через DriveBase).
    mm                 — дистанция, мм
    accel_mm/decel_mm  — длина разгона и торможения, мм
    low_speed          — скорость на старте, мм/с
    high_speed         — крейсерская скорость, мм/с
    end_speed          — скорость в конце торможения, мм/с
    """
    left_sensor = need_sensor(left_color_sensor, "left (Port C)")
    right_sensor = need_sensor(right_color_sensor, "right (Port D)")

    drive_base.reset()
    prev_error = 0
    timer = StopWatch()

    while drive_base.distance() < mm:
        if timer.time() > timeout_ms:
            timeout_warn("follow_line_2")
            break

        dist = drive_base.distance()

        # профиль скорости: берём минимум из разгона и торможения
        # (на коротких дистанциях они перекрываются — это нормально)
        speed = high_speed
        if accel_mm > 0 and dist < accel_mm:
            speed = min(speed, map_value(dist, 0, accel_mm, low_speed, high_speed))
        if decel_mm > 0 and dist > mm - decel_mm:
            speed = min(speed, map_value(dist, mm - decel_mm, mm, high_speed, end_speed))

        error = left_sensor.reflection() - right_sensor.reflection()
        derivative = error - prev_error
        turn = kp * error + kd * derivative

        drive_base.drive(speed, turn)
        prev_error = error
        wait(5)

    if brake:
        drive_base.brake()
    else:
        drive_base.stop()
