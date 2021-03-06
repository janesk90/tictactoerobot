#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
arm_motor = Motor(Port.A)

wheel_diameter = 56
axle_track = 114
robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

def Arm ():
    arm_motor.run_angle(100, 45)
    wait(1000)
    arm_motor.run_angle(100, -45)
    wait(1000)

def WriteSymbol ():
    left_motor.run_angle(75, 150)
    right_motor.run_angle(75, 180)
    left_motor.run_angle(75, 150)