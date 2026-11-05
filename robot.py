"""
robot.py — железо робота и общее состояние.

Здесь создаются хаб, моторы, датчики и DriveBase, а также лежат мелкие
утилиты и учёт курса (set_heading / sync_heading).
Остальные модули берут устройства ОТСЮДА, поэтому они всегда общие.
"""
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Direction, Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from umath import pi

from config import (
    TIRE_DIAMETER, AXLE_TRACK,
    STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL
)

# ==============================================================================
# УСТРОЙСТВА
# ==============================================================================
hub = PrimeHub()
hub.system.set_stop_button(Button.BLUETOOTH)

# ВАЖНО: порядок создания моторов не менять (правый привод создаётся первым).
right_drive_motor = Motor(Port.B, Direction.CLOCKWISE)
left_drive_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

right_att_motor = Motor(Port.E)
left_att_motor = Motor(Port.A)

try:
    left_color_sensor = ColorSensor(Port.C)
    right_color_sensor = ColorSensor(Port.D)
except Exception:
    left_color_sensor = None
    right_color_sensor = None

drive_base = DriveBase(left_drive_motor, right_drive_motor,
                       wheel_diameter=TIRE_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)
drive_base.settings(STRAIGHT_SPEED, STRAIGHT_ACCEL, TURN_RATE, TURN_ACCEL)

# ==============================================================================
# ОБЩЕЕ СОСТОЯНИЕ (одно на все модули)
# ==============================================================================
class _State:
    heading_target = 0   # курс, который держит drive() и от которого считает turn_by()

state = _State()

# ==============================================================================
# УТИЛИТЫ
# ==============================================================================
def print_battery():
    """Печатает заряд аккумулятора в консоль (вызывается в начале каждого заезда)."""
    battery_mv = hub.battery.voltage()
    print("Заряд аккумулятора:", battery_mv, "мВ (", battery_mv / 1000.0, "В )")

def mm_to_deg(mm, wheel_diameter=TIRE_DIAMETER):
    """Миллиметры пути -> градусы поворота мотора."""
    return int((mm / (pi * wheel_diameter)) * 360)

def clamp(value, low, high):
    return max(low, min(high, value))

def map_value(value, from_low, from_high, to_low, to_high):
    """Линейное преобразование диапазона (без деления на ноль)."""
    if from_high == from_low:
        return to_high
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

def wrap180(angle):
    """Приводит разницу углов к диапазону [-180, 180)."""
    return (angle + 180) % 360 - 180

def heading_180():
    """Текущий курс гироскопа, приведённый к диапазону [-180, 180]."""
    heading = hub.imu.heading() % 360
    if heading > 180:
        heading -= 360
    return heading

def stop_motors():
    """Выключить моторы привода (без торможения)."""
    left_drive_motor.dc(0)
    right_drive_motor.dc(0)

def timeout_warn(name):
    """Сообщает в консоль, что функция вышла по таймауту, а не по цели."""
    print("ТАЙМАУТ:", name)

def need_sensor(sensor, name):
    """Громко падает, если датчика нет (вместо молчаливой подстановки значения)."""
    if sensor is None:
        raise RuntimeError("Нет датчика цвета: " + name)
    return sensor

# ==============================================================================
# КУРС
# ==============================================================================
def set_heading(angle=0):
    """
    Задаёт текущий курс робота (обычно 0 в начале заезда) и делает его целевым.
    Вызывай ОДИН РАЗ в начале заезда, когда робот стоит неподвижно на старте.
    Курс: + по часовой стрелке. Также используется для "привязки" к стене.
    """
    left_drive_motor.dc(0)
    right_drive_motor.dc(0)
    hub.imu.reset_heading(angle)
    state.heading_target = angle
    wait(80)  # пауза, чтобы IMU зафиксировал курс до движения

def sync_heading():
    """
    Считать ТЕКУЩИЙ курс целевым. Вызывай после ручных манёвров (move_by_time,
    move_by_deg, ...), которые повернули робота, иначе следующий drive()
    будет пытаться вернуться к старому курсу.
    """
    state.heading_target = hub.imu.heading()
