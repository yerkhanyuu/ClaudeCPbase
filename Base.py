"""
Base.py — точка входа базы робота команды Heaven.

Заезды подключают базу как раньше:   from Base import *
Запускать нужно mainHeaven.py.

Структура (всё лежит в одном проекте Pybricks):
  config.py       — все константы и настройки
  robot.py        — хаб, моторы, датчики, DriveBase, курс (set_heading), утилиты
  driving.py      — drive(), align_wall(), ручные манёвры, движение по линии
  turning.py      — turn_to(), turn_by()
  attachments.py  — моторы насадок
  legacy.py       — СТАРЫЕ имена (forward, LQR_povorot, leftDriveMotor, ...)
                    для старых заездов; в новых заездах не используется

Новый заезд пишется так:
    set_heading(0)         # один раз в начале
    drive(500)
    turn_to(90)
    align_wall(heading=90)
"""
# Эти имена раньше экспортировались из Base — оставляем, чтобы заезды не ломались
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from umath import pi

from config import *
from robot import *
from driving import *
from turning import *
from attachments import *
from legacy import *   # убери эту строку, когда все заезды переведены на новый API
