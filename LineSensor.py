#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

class LineSensor:
    def __init__(self, motor, colorSensor, speed, edgeOfLineAmbience):
        self.motor = motor
        self.colorSensor = colorSensor
        self.speed = speed
        self.edgeOfLineAmbience = edgeOfLineAmbience
    def run(self, speedFactor = 1): 
        self.motor.run(self.speed * speedFactor)
    def stop(self):
        self.motor.stop()
    def ambient(self):
        return self.colorSensor.ambient()
    def color(self):
        return self.colorSensor.color()
    def getEdgeOfLineAmbience(self):
        return self.edgeOfLineAmbience
    
        