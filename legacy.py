"""
legacy.py — СТАРЫЕ ИМЕНА для совместимости со старыми заездами (Heaven_*.py).

Всё здесь работает как раньше (старые названия и порядок параметров), но внутри
вызывает новые функции. В новых заездах это НЕ использовать.
Когда все заезды переведены на новый API — удали строку
"from legacy import *" в Base.py и этот файл.

Соответствие старых имён новым:

  leftDriveMotor / rightDriveMotor      -> left_drive_motor / right_drive_motor
  leftAttachmentMotor / rightAttachment -> left_att_motor / right_att_motor
  leftColorSensor / rightColorSensor    -> left_color_sensor / right_color_sensor
  Drive_base                            -> drive_base
  left / right                          -> LEFT / RIGHT
  bc_stop()                             -> stop_motors()
  Gyro()                                -> heading_180()
  reset_gyro_safe()                     -> set_heading(0)
  left_att / right_att                  -> left_att_run / right_att_run
  arm_pd(sigma=)                        -> left_att_pd(forward=)
  grabber_pd(sigma=)                    -> right_att_pd(forward=)
  move_time / move_deg                  -> move_by_time / move_by_deg
  forward / backward                    -> drive(+мм) / drive(-мм)
  sigma_Drive / PidDrive / GyroDrive    -> drive(мм)
  LQR_povorot / Pid_povorot / GyroTurn  -> turn_to(угол) / turn_by(угол)
  LQR_pivot(direction=)                 -> turn_to(угол, pivot=)
  LPD                                   -> follow_line / follow_line_deg
  line_follow_2_sensors_acc             -> follow_line_2
"""
from pybricks.parameters import Stop
from pybricks.tools import wait, StopWatch

from config import (
    RIGHT, LEFT, STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL,
    DRIVE_KP, DRIVE_KI, DRIVE_KD, TURN_K1, TURN_K2
)
from robot import (
    hub, state, drive_base,
    left_drive_motor, right_drive_motor, left_att_motor, right_att_motor,
    left_color_sensor, right_color_sensor,
    set_heading, stop_motors, heading_180, timeout_warn
)
from driving import drive_core, move_by_time, move_by_deg, follow_line_deg, follow_line_2
from turning import turn_to
from attachments import left_att_run, right_att_run, left_att_pd, right_att_pd

# ==============================================================================
# СТАРЫЕ ИМЕНА ОБЪЕКТОВ (те же самые объекты)
# ==============================================================================
leftDriveMotor = left_drive_motor
rightDriveMotor = right_drive_motor
leftAttachmentMotor = left_att_motor
rightAttachmentMotor = right_att_motor
leftColorSensor = left_color_sensor
rightColorSensor = right_color_sensor
Drive_base = drive_base
right = RIGHT
left = LEFT
timer_move = StopWatch()

# ==============================================================================
# СТАРЫЕ ИМЕНА ФУНКЦИЙ — простые псевдонимы
# ==============================================================================
bc_stop = stop_motors
Gyro = heading_180
reset_gyro_safe = lambda: set_heading(0)

# ==============================================================================
# НАСАДКИ
# ==============================================================================
def left_att(Power, Deg, is_wait=True):
    left_att_run(Power, Deg, is_wait)

def right_att(Power, Deg, is_wait=True):
    right_att_run(Power, Deg, is_wait)

def arm_pd(deg, sigma=True, kp=2, kd=1.2, timeout_ms=2000, tolerance=1, min_power=20):
    left_att_pd(deg, sigma, kp, kd, timeout_ms, tolerance, min_power)

def grabber_pd(deg, speed, sigma=True, kp=2, kd=1.2, timeout_ms=2000, tolerance=1, min_speed=60):
    right_att_pd(deg, speed, sigma, kp, kd, timeout_ms, tolerance, min_speed)

# ==============================================================================
# ПРОСТОЕ ДВИЖЕНИЕ БАЗЫ
# ==============================================================================
def move_time(Power_B, Power_C, ms, Brake=True):
    # Power_B — левый мотор (порт F), Power_C — правый (порт B)
    move_by_time(Power_B, Power_C, ms, Brake)

def move_deg(Power_B, Power_C, Deg, Brake=True, timeout_ms=5000):
    move_by_deg(Power_B, Power_C, Deg, Brake, timeout_ms)

def pd_Drive(Power, Kp, Kd, last_error, is_wait=True):
    angle_B = left_drive_motor.angle() - 2   # -2: подгонка под разницу моторов
    angle_C = right_drive_motor.angle()
    error = angle_B - angle_C

    P = Kp * error
    D = Kd * (error - last_error)
    pid_adj = P + D

    left_drive_motor.dc(Power - pid_adj)
    right_drive_motor.dc(Power + pid_adj)

    wait(10)
    return error

def sigma_Drive(Power, Kp, Kd, Deg, Brake=True, timeout_ms=5000):
    """Без гироскопа, держит только равенство колёс. Используй drive()."""
    last_error = 0
    left_drive_motor.reset_angle(0)
    right_drive_motor.reset_angle(0)
    timer = StopWatch()

    while (abs(left_drive_motor.angle()) + abs(right_drive_motor.angle())) / 2 <= Deg:
        if timer.time() > timeout_ms:
            timeout_warn("sigma_Drive")
            break
        last_error = pd_Drive(Power, Kp, Kd, last_error)

    # При Brake=False моторы специально не трогаем (для сцепки движений).
    if Brake:
        drive_base.brake()

# ==============================================================================
# ЕЗДА ПО ГИРОСКОПУ СО СБРОСОМ КУРСА (старый стиль)
# ==============================================================================
def forward(
    target_heading,
    final_angle,
    start_speed,
    max_speed,
    end_speed,
    decel_start_angle,
    accel_rate,
    kp_base=DRIVE_KP,
    ki_base=DRIVE_KI,
    kd_base=DRIVE_KD,
    reset_gyro=True,
    stall_stop=False,
    timeout_ms=6000
):
    """Используй drive(+мм). Углы здесь в градусах мотора."""
    if reset_gyro:
        set_heading(0)
    drive_core(
        1, target_heading, final_angle, start_speed, max_speed, end_speed,
        decel_start_angle, accel_rate, kp_base, ki_base, kd_base,
        stall_stop, timeout_ms
    )

def backward(
    target_heading,
    final_angle,
    start_speed,
    max_speed,
    end_speed,
    decel_start_angle,
    accel_rate,
    kp_base=DRIVE_KP,
    ki_base=DRIVE_KI,
    kd_base=DRIVE_KD,
    reset_gyro=True,
    stall_stop=False,
    timeout_ms=6000
):
    """Используй drive(-мм). Углы здесь в градусах мотора."""
    if reset_gyro:
        set_heading(0)
    drive_core(
        -1, target_heading, final_angle, start_speed, max_speed, end_speed,
        decel_start_angle, accel_rate, kp_base, ki_base, kd_base,
        stall_stop, timeout_ms
    )

def PidDrive(distance, speed=600, Kp=1.5, Ki=0, Kd=0.05, Mp=3.1, Mi=0.005, Md=0.45, stop=Stop.BRAKE, timeout_ms=3000):
    """Используй drive(). distance здесь в мм."""
    set_heading(0)
    drive_base.reset()
    left_drive_motor.reset_angle(0)
    right_drive_motor.reset_angle(0)

    integral = 0
    last_error = 0
    disI = 0
    lastDisE = 0

    stopwatch = StopWatch()
    stopwatch.reset()

    while True:
        dis = drive_base.distance()
        error = 0 - hub.imu.heading()
        integral += error
        derivative = error - last_error
        correction = Kp * error + Ki * integral + Kd * derivative
        last_error = error

        disE = -dis + distance
        disI += disE
        disD = disE - lastDisE
        mSpeed = Mp * disE + Mi * disI + Md * disD
        lastDisE = disE

        if mSpeed > speed:
            mSpeed = speed
        elif mSpeed < -speed:
            mSpeed = -speed

        left_drive_motor.run(mSpeed + correction)
        right_drive_motor.run(mSpeed - correction)

        if abs(dis - distance) <= 5:
            break
        if stopwatch.time() > timeout_ms:
            timeout_warn("PidDrive")
            break
        wait(10)

    if stop == Stop.HOLD:
        left_drive_motor.hold()
        right_drive_motor.hold()
    elif stop == Stop.BRAKE:
        drive_base.brake()
    else:
        left_drive_motor.stop()
        right_drive_motor.stop()

def GyroDrive(distance, speed=STRAIGHT_SPEED, then=Stop.COAST_SMART, wait=True, accel=200):
    """Езда через DriveBase. Используй drive()."""
    if speed > 540:
        speed = 540
    if speed < -540:
        speed = -540
    drive_base.settings(speed, accel, TURN_RATE, TURN_ACCEL)
    drive_base.straight(distance, then, wait)
    drive_base.settings(STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL)

def GyroTurn(angle, then=Stop.COAST, wait=True, speed=TURN_RATE):
    """Поворот через DriveBase. Используй turn_to()."""
    drive_base.settings(STRAIGHT_SPEED, STRAIGHT_ACCEL, speed, TURN_ACCEL)
    drive_base.turn(angle, then, wait)
    drive_base.settings(STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL)

def Curve(radius, angle, stop=Stop.BRAKE, wait=True, speed=STRAIGHT_SPEED):
    drive_base.settings(speed, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL)
    drive_base.curve(radius, angle, stop, wait)
    drive_base.settings(STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL)

# ==============================================================================
# ПОВОРОТЫ СО СБРОСОМ КУРСА (старый стиль)
# ==============================================================================
def LQR_povorot(
    target_angle,
    k1=TURN_K1,
    k2=TURN_K2,
    max_power=65,
    min_power=16,
    tolerance=1.0,
    timeout_ms=1200
):
    """Используй turn_to(angle)."""
    turn_to(target_angle, None, k1, k2, max_power, min_power, tolerance, timeout_ms, reset_gyro=True)

def LQR_pivot(
    target_angle,
    k1=TURN_K1,
    k2=TURN_K2,
    max_power=65,
    min_power=18,
    direction=right,
    tolerance=1.0,
    timeout_ms=1200
):
    """Используй turn_to(angle, pivot=RIGHT / LEFT)."""
    turn_to(target_angle, direction, k1, k2, max_power, min_power, tolerance, timeout_ms, reset_gyro=True)

def _pid_turn(target, Kp, Ki, Kd, Tp, timeout_ms):
    """Общий PID-поворот на месте. target — курс после сброса гироскопа (+ по часовой)."""
    set_heading(0)

    integral = 0.0
    last_error = hub.imu.heading() - target  # без "пинка" производной на первом шаге
    timer = StopWatch()

    while True:
        angle = hub.imu.heading()
        error = angle - target

        # интеграл сбрасывается при пересечении цели
        if error * last_error < 0:
            integral = 0.0
        integral += error
        integral = max(-200, min(200, integral))

        derivative = error - last_error
        correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
        power = correction * Tp

        left_drive_motor.run(-power)
        right_drive_motor.run(power)
        last_error = error

        # выходим, только когда робот почти не вращается
        if abs(error) < 1 and abs(hub.imu.angular_velocity()[2]) < 5:
            break
        if timer.time() > timeout_ms:
            timeout_warn("pid_turn")
            break
        wait(5)

    left_drive_motor.stop()
    right_drive_motor.stop()
    wait(50)
    state.heading_target = target  # чтобы последующий drive() держал этот курс

def Pid_povorot(angle1, Tp=1, timeout_ms=2500):
    """Используй turn_to(angle)."""
    _pid_turn(angle1, 4.4, 0.2, 4, Tp, timeout_ms)

def Pid_povorot_left(angle1, Tp=1, timeout_ms=2500):
    """Используй turn_to(-angle). angle1 здесь положительный = влево."""
    _pid_turn(-angle1, 4.1, 0.1, 4, Tp, timeout_ms)

# ==============================================================================
# ДВИЖЕНИЕ ПО ЛИНИИ
# ==============================================================================
def LPD(final_angle, base_speed=100, kp=0.9, kd=3.5, TARGET=60, MAX_CORRECTION=400, block=True, timeout_ms=8000, reset_gyro=True):
    """Используй follow_line(мм) или follow_line_deg(градусы)."""
    follow_line_deg(final_angle, base_speed, kp, kd, TARGET, MAX_CORRECTION, block, timeout_ms, reset_gyro)

def line_follow_2_sensors_acc(distance, Acc=200, Dec=200, LowPower=100, HighPower=200, EndPower=50, Kp=1.6, Kd=0.4, Brake=True, timeout_ms=10000):
    """Используй follow_line_2."""
    follow_line_2(distance, Acc, Dec, LowPower, HighPower, EndPower, Kp, Kd, Brake, timeout_ms)
