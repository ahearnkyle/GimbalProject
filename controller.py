import pygame
import time
import os.path
from gimbalController import GimbalController

#global variables 
CONTROLLER_DEVICE_PATH = "/dev/input/js0"

#buttons
START = 11
LEFT_BUMPER = 6
RIGHT_BUMPER = 7
A = 0
B = 1
Y = 4
X = 3

'''
For the triggers any value besides 0 should be considered input
For the sticks well have to figure out how to take input from
them and what we want to use them for.

It looks like that 3 is left and right on right stick and 2 is up and down
on the right stick 

On the left stick 1 is left and right and 0 is up and down 
'''
#axis
LEFT_TRIGGER = 5
RIGHT_TRIGGER = 4
#LEFT_STICK = 1 and 0
LEFT_STICK_UP_DOWN = 0
LEFT_STICK_LEFT_RIGHT = 1
#RIGHT_STICK = 3 and 2
RIGHT_STICK_UP_DOWN = 2
RIGHT_STICK_LEFT_RIGHT = 3

#hats
'''
DOWN    [0][-1]
RIGHT   [1][0]
UP      [0][1]
LEFT    [-1][0]
'''

def startControllerListener():
    
    CONTROLLER_INPUT_ACTIVE = False
    START_IS_PRESSED = False #button 11
    LEFT_BUMPER_PRESSED = False #button 6 
    RIGHT_BUMPER_PRESSED = False #button 7
    
    LEFT_TRIGGER_PRESSED = 0
    RIGHT_TRIGGER_PRESSED = 0
    PAN = 0
    PAN_SPEED = 0
    PAN_PRESSED = 0
    TILT = 0
    TILT_SPEED = 0
    TILT_PRESSED = 0

    #Grab and initialize controller
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()

    gimbal = GimbalController('192.168.0.36', 10001)
 
    #listen for events (button presses)
    while controllerConnected():
        while not CONTROLLER_INPUT_ACTIVE and controllerConnected():
            for event in pygame.event.get():
                if not CONTROLLER_INPUT_ACTIVE:
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == LEFT_BUMPER:
                            LEFT_BUMPER_PRESSED = True
                        elif event.button == RIGHT_BUMPER:
                            RIGHT_BUMPER_PRESSED = True
                        elif event.button == START:
                            START_IS_PRESSED = True
                    if START_IS_PRESSED and RIGHT_BUMPER_PRESSED and LEFT_BUMPER_PRESSED:
                        CONTROLLER_INPUT_ACTIVE = True
            gimbal.getStatusJog(0,0,0,0,4,0,0)    
        # get speed
        pygame.event.pump()
        LEFT_TRIGGER_PRESSED = controller.get_axis(LEFT_TRIGGER)
        RIGHT_TRIGGER_PRESSED = controller.get_axis(RIGHT_TRIGGER)
        print(LEFT_TRIGGER_PRESSED)
        print(RIGHT_TRIGGER_PRESSED)
        if LEFT_TRIGGER_PRESSED == 0 and RIGHT_TRIGGER_PRESSED == 0 or LEFT_TRIGGER_PRESSED == -1.0 and RIGHT_TRIGGER_PRESSED == -1.0 :
            PAN_SPEED = 0
            TILT_SPEED = 0   
        
        # get axis
        PAN_PRESSED = controller.get_axis(LEFT_STICK_LEFT_RIGHT)
        TILT_PRESSED = controller.get_axis(LEFT_STICK_UP_DOWN)   
        print(PAN_PRESSED)
        print(TILT_PRESSED)
        if PAN_PRESSED == 0.0 and TILT_PRESSED == 0.0:
            PAN = 0
            TILT = 0
            gimbal.getStatusJog(0,0,0,0,4,0,0)  
        elif TILT_PRESSED > -.6 and TILT_PRESSED < .6:
            if PAN_PRESSED < 0:
                TILT = 64
            else:
                TILT = 0
            if TILT_SPEED == 0:
                TILT_SPEED = 1
            if LEFT_TRIGGER_PRESSED != -1.0:
                TILT_SPEED = 2
            if RIGHT_TRIGGER_PRESSED != -1.0:
                TILT_SPEED = 3
        elif PAN_PRESSED > -.7 and PAN_PRESSED < .7:
            if TILT_PRESSED < 0:
                PAN = 128
            else:
                PAN = 0
            if PAN_SPEED == 0:
                PAN_SPEED = 1
            if LEFT_TRIGGER_PRESSED != -1.0:
                PAN_SPEED = 2
            if RIGHT_TRIGGER_PRESSED != -1.0:
                PAN_SPEED = 3
        # print(event)
        # gimbal.getStatusJog(0,0,0,0,4,0,0)
        print(PAN,TILT,PAN_SPEED,TILT_SPEED)
        gimbal.getStatusJog(PAN,TILT,PAN_SPEED,TILT_SPEED,4,0,0)
    
    #Must disconnect the controller if it is to be used again
    controller.quit()

def controllerConnected():
    return os.path.exists(CONTROLLER_DEVICE_PATH)

def main():
    pygame.init()
    while True:
        while not controllerConnected():
            print("no controller found")
            time.sleep(15)
        else:
            startControllerListener()

if __name__ == '__main__':
    main()