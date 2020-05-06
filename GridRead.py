#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from LineSensor import LineSensor

def getEdgeOfLine(colorSensor, sensorName = ""):
    insideOfLineAmbience = 0
    outsideOfLineAmbience = 0
    while (insideOfLineAmbience >= outsideOfLineAmbience ):
        print(sensorName + " color sensor: ")
        insideOfLineAmbience = calibrateColorSensor(colorSensor = colorSensor, 
            sensorName = sensorName, position = "center of line")
        print("--- line: " + str(insideOfLineAmbience))
        outsideOfLineAmbience = calibrateColorSensor(colorSensor = colorSensor, 
            sensorName = sensorName, position = "white section")
        print("--- white: " + str(outsideOfLineAmbience))
        edgeOfLineAmbience = ((insideOfLineAmbience + outsideOfLineAmbience) / 2)
        print("--- edge: " + str(edgeOfLineAmbience))
    return edgeOfLineAmbience

def calibrateColorSensor(colorSensor, sensorName = "", position = ""):
    while not any (brick.buttons()):
        brick.display.text("Place so that ",  (5, 50))
        brick.display.text(sensorName + " color")
        brick.display.text("sensor hovers over")
        brick.display.text(position)
        brick.display.text("then press")
        brick.display.text("any button")
        wait(100)
    ambienceDetected = colorSensor.ambient()
    wait(200)
    brick.display.clear()
    wait(100)
    # if (rightColorSensor.color() == Color.BLACK):
    #     print("Sees black R")
    # if (leftColorSensor.color() == Color.BLACK):
    #     print("Sees black L")
    return ambienceDetected

def getPositioned():
    while not any (brick.buttons()):
        brick.display.text("position over edge", (5, 50))
        brick.display.text("of line and")
        brick.display.text("press any button")
        wait(100) 


# issue - 
# lineFollowingSensor etc still uses leftSpeed and rightSpeed... 
# if its going to be truly ready to switch use of motors we need this method to just know
def inchWorm(lineCrossingModule, lineFollowingModule, direction):
    brick.light(Color.GREEN)
    lineFollowingModuleAmbience = lineFollowingModule.ambient()
    lineCrossingModuleColor = lineCrossingModule.color()
    lineCrossingModuleAmbience = lineCrossingModule.ambient()
    lineCrossingModuleSeesLine = False
    if lineFollowingModuleAmbience  > lineFollowingModule.getEdgeOfLineAmbience(): # lighter
        lineFollowingModule.run(speedFactor = (1/2 * direction))
        lineCrossingModule.run(speedFactor = direction)
    elif lineFollowingModuleAmbience <= lineFollowingModule.getEdgeOfLineAmbience(): # darker
        if lineCrossingModuleColor == Color.BLACK:
            print("line cross sees line is black")
            lineCrossingModuleSeesLine = True
            brick.light(Color.RED)
            lineCrossingModule.run(speedFactor = (1/2 * direction))
            lineFollowingModule.run(speedFactor = (1/2 * direction))
        if lineCrossingModuleAmbience < lineCrossingModule.getEdgeOfLineAmbience(): 
            print("line cross sees darker than average")
            lineCrossingModuleSeesLine = True
            brick.light(Color.RED)
            lineCrossingModule.run(speedFactor = (1/2 * direction))
            lineFollowingModule.run(speedFactor = (1/2 * direction))
        else:
            lineCrossingModule.run(speedFactor = (1/2 * direction))
            lineFollowingModule.run(speedFactor = direction)
    return lineCrossingModuleSeesLine

def moveForward(lineCrossingModule, lineFollowingModule, linesToCross, direction):
    linesCrossed = 0
    lineSpottedCurrent = False
    lineSpotted1Previous = False
    lineSpotted2Previous = False
    while ( linesCrossed < linesToCross ) :
        lineSpotted3Previous = lineSpotted2Previous
        lineSpotted2Previous = lineSpotted1Previous
        lineSpotted1Previous = lineSpottedCurrent
        lineSpottedCurrent = inchWorm(lineCrossingModule, lineFollowingModule, direction)
        if ((lineSpotted2Previous and lineSpotted3Previous) 
        and not (lineSpottedCurrent or lineSpotted1Previous) ): 
            lineCrossingModule.stop()
            lineFollowingModule.stop()
            linesCrossed = linesCrossed + 1
            brick.sound.beep()
            print("Lines crossed: " + str(linesCrossed))
    brick.sound.beep()

# have it back up, then follow the edge of the line

def turnRight(lineCrossingModule, lineFollowingModule): 
    turnTime = 65
    currTime = 0
    while (currTime < turnTime):
        lineFollowingModule.run(1)
        lineCrossingModule.run(-1)
        wait(1)
        currTime = currTime + 1
    lineCrossingModule.stop()
    lineFollowingModule.stop()



leftColorSensor = ColorSensor(Port.S2)
leftEdgeOfLineAmbience = getEdgeOfLine(colorSensor = leftColorSensor, sensorName = "LEFT")
leftMotor = Motor(Port.A)
leftSpeed = 100
leftModule = LineSensor(leftMotor, leftColorSensor, leftSpeed, leftEdgeOfLineAmbience)

rightColorSensor = ColorSensor(Port.S3)
rightEdgeOfLineAmbience = getEdgeOfLine(colorSensor = rightColorSensor, sensorName = "RIGHT")
rightMotor = Motor(Port.D)
rightSpeed = 100
rightModule = LineSensor(rightMotor, rightColorSensor, rightSpeed, rightEdgeOfLineAmbience)

lineFollowingModule = leftModule
lineCrossingModule = rightModule

getPositioned()

# def rerun():
#     while not any (brick.buttons()):
#         brick.display.text("press a button", (5, 50))
#         brick.display.text("to run again")
#     return True


# while True: 
#     moveForward(lineCrossingModule, lineFollowingModule, linesToCross = 3, direction = 1)
#     turnRight(lineCrossingModule, lineFollowingModule)

def navigate(lineCrossingModule, 
    lineFollowingModule, 
    currentCoordinates, 
    destinationCoordinates):
    print("from " + str(currentCoordinates) + " to " + str(destinationCoordinates))
    
    i = 0
    while currentCoordinates != destinationCoordinates:
        if currentCoordinates[i] != destinationCoordinates[i]:
            turnRight(lineCrossingModule, lineFollowingModule)
            coordDifference = destinationCoordinates[i] - currentCoordinates[i]
            linesToCross = abs(coordDifference) + 1
            moveForward(lineCrossingModule, lineFollowingModule, linesToCross, direction = 1)
            currentCoordinates[i] = currentCoordinates[i] + coordDifference
            print(str(i))
        i = (i + 1) % 2

    print("->arrived at " + str(currentCoordinates))
    return currentCoordinates

initialCoordinates = [0, 0]

currentCoordinates = navigate(lineCrossingModule, lineFollowingModule, currentCoordinates = initialCoordinates, destinationCoordinates = [0,0])

currentCoordinates = navigate(lineCrossingModule, lineFollowingModule, currentCoordinates, destinationCoordinates = [0,2])

currentCoordinates = navigate(lineCrossingModule, lineFollowingModule, currentCoordinates, destinationCoordinates = [2,2])


# def backup(lineCrossingModule, lineFollowingModule):
#     # print("starting reverse traverse")
#     # traverseGrid(lineCrossingModule, lineFollowingModule, linesToCross = 1, direction = -1)
#     # print("reverse traverse done, starting while loop")
#     # i = 0
#     lineCrossingModuleAmbience = lineCrossingModule.ambient()
#     lineFollowingModuleAmbience = lineFollowingModule.ambient()
#     while lineCrossingModuleAmbience <= lineCrossingModule.edgeOfLineAmbience: 
#         print(str(lineFollowingModuleAmbience) + "   " + str(lineCrossingModuleAmbience))
#         lineFollowingModule.run(-1)
#         lineCrossingModule.run(-1)
#         # if (lineFollowingModuleAmbience < lineFollowingModuleAmbience): # darker
#         #     lineFollowingModule.run(-1/2)
#         #     lineCrossingModule.stop()
#         # elif (lineFollowingModuleAmbience > lineFollowingModuleAmbience): 
#         #     lineCrossingModule.run(-1/2)
#         #     lineFollowingModule.stop()
#         # else:
#         #     lineFollowingModule.run(-1/2)
#         #     lineCrossingModule.run(-1/2)
#         lineCrossingModuleAmbience = lineCrossingModule.ambient()
#         lineFollowingModuleAmbience = lineFollowingModule.ambient()
#     lineCrossingModule.stop()
#     lineFollowingModule.stop()
#     print("while loop done")

#     # print("in backup")
#     # brick.sound.beep()
#     # print("--->line following ambience: " + str(innerModule.ambient()))
#     # print("--->line crossing ambience: " + str(outerModule.ambient()))
#     # speedFactor = -1/2

    
#     # # lighter
#     # innerModuleAmbience = innerModule.ambient()
#     # outerModuleAmbience = outerModule.ambient()
#     # outerModuleColor = outerModule.color()
#     # while outerModuleColor == Color.BLACK():
#     #     outerModule.run(speedFactor)
#     #     if (innerModuleAmbience >= innerModule.getEdgeOfLineAmbience()):
#     #         innerModule.run(speedFactor)
        
#     #     # print("-----> beyond the line")
#     #     # if (innerModuleAmbience <= innerModule.getEdgeOfLineAmbience()):
#     #     #     innerModule.run(speedFactor)
#     #     #     print("-----> inner moving back")
#     #     # if (outerModuleAmbience < outerModule.getEdgeOfLineAmbience()):
#     #     #     outerModule.run(speedFactor)
#     #     #     # if (innerModuleAmbience > innerModule.getEdgeOfLineAmbience()): 
#     #     #     #     innerModule.run(speedFactor)
#     #     #     print("-----> outer moving back")
#     #     innerModuleAmbience = innerModule.ambient()
#     #     outerModuleAmbience = outerModule.ambient()
#     #     outerModuleColor = outerModule.color()

#     # # print("--->line following ambience: " + str(innerModule.ambient()))
#     # # print("--->line crossing ambience: " + str(outerModule.ambient()))
#     # # while innerModule.ambient() == innerModule.getEdgeOfLineAmbience() or outerModule.ambient() == outerModule.getEdgeOfLineAmbience(): 
#     # #     print("within the line")
#     # #     if (innerModule.ambient() <= innerModule.getEdgeOfLineAmbience()):
#     # #         innerModule.run(speedFactor)
#     # #         print("inner moving back")
#     # #     if (outerModule.ambient() <= outerModule.getEdgeOfLineAmbience()):
#     # #         outerModule.run(speedFactor)
#     # #         print('outter moving back')
    
#     # # print("should be on the line")
#     # # innerModule.stop()
#     # # outerModule.stop()
#     # # brick.light(Color.YELLOW)
#     # # brick.sound.beep()
#     # # wait(100)
#     # # #darker
#     # # print("--->line following ambience: " + str(innerModule.ambient()))
#     # # print("--->line crossing ambience: " + str(outerModule.ambient()))

#     # # while innerModule.ambient() > innerModule.getEdgeOfLineAmbience() or outerModule.ambient() > outerModule.getEdgeOfLineAmbience():  
#     # #     if (innerModule.ambient() > innerModule.getEdgeOfLineAmbience()):
#     # #         innerModule.run(speedFactor)
#     # #         print("-----> inner moving back")
#     # #     if (outerModule.ambient() > outerModule.getEdgeOfLineAmbience()):
#     # #         outerModule.run(speedFactor)
#     # #         print("-----> outer moving back")
#     # # print("in front of the line")
#     # # brick.color(Color.RED)
#     # innerModule.stop()
#     # outerModule.stop()





# innerModule = lineFollowingModule 
# outerModule = lineCrossingModule
# i = 0
# while (i <= 3): 
#     innerModule.run(-1)
#     outerModule.run(-1)
#     print(i)
#     i = i + 1
#     wait(1)
# print ("done")





# def turn(innerModule = lineFollowingModule, outerModule = lineCrossingModule):
#     aligned = False
#     while (innerModule.color() == Color.BLACK) : 
#         while (outerModule.color() == Color.BLACK): 
#             innerModule.run(1/2)
#             outerModule.run(-1/2)
#             print("both black")
#     while not aligned : 
#         if ( innerModule.color() == Color.BLACK ) :
#             if ( outerModule.color() == Color.BLACK) :
#                 innerModule.stop()
#                 outerModule.stop()
#             else : 
#                 print("inner aligned")
#                 aligned = align(stopModule = innerModule, 
#                     alignModule = outerModule)
#         elif (outerModule.color() == Color.BLACK) : 
#             print("outer aligned")
#             aligned = align(stopModule = outerModule, alignModule = innerModule)
#         else : 
#             innerModule.run(1/3)
#             outerModule.run(-1/2)
#             print("not aligned")

            

# def align(stopModule, alignModule): 
#     stopModule.run(1/4)
#     alignModule.run(-1/2)
#     aligned = (stopModule.color() == Color.BLACK) and (alignModule.color() == Color.BLACK)
#     return aligned
    



# #reverses back in a -90 degree swoop to line up with the perpendicular line
# def turn(edgeOfLine, lineCrossingModule = rightModule, lineFollowingModule = leftModule): 
#     linesDetected = 0
#     lineSpottedCurrent = False
#     lineSpotted1Previous = False
#     lineSpotted2Previous = False
#     while linesDetected < 1: 
#         lineSpotted3Previous = lineSpotted2Previous
#         lineSpotted2Previous = lineSpotted1Previous
#         lineSpotted1Previous = lineSpottedCurrent
#         lineSpottedCurrent = (lineCrossingModule.ambient >= edgeOfLine)  and (lineFollowingModule.ambient >= edgeOfLine)
#         if ((lineSpotted2Previous and lineSpotted3Previous) 
#         and not (lineSpottedCurrent or lineSpotted1Previous) ): 
#             linesCrossed = linesCrossed + 1
#             print("Lines crossed: " + str(linesCrossed))
#             lineCrossingModule.run(-1/2)
#             lineFollowingModule.run(-1/2)

#     lineSpottedCurrent = False
#     lineSpotted1Previous = False
#     lineSpotted2Previous = False
#     while linesDetected < 2: 
#         lineSpotted3Previous = lineSpotted2Previous
#         lineSpotted2Previous = lineSpotted1Previous
#         lineSpotted1Previous = lineSpottedCurrent
#         lineSpottedCurrent = (lineCrossingModule.ambient >= edgeOfLine)  and (lineFollowingModule.ambient >= edgeOfLine)
    



# edgeOfLine = init(lineFollowingModule = lineFollowingModule)
#getPositioned()
#turn()

#traverseGrid(linesToCross = 2, lineCrossingModule = lineCrossingModule, lineFollowingModule = lineFollowingModule)
