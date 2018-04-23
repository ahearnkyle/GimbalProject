import pygame
import time
import os.path
from gimbalController import GimbalController

#global variables
CONTROLLER_DEVICE_PATH = "/dev/input/js0"

# buttons
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
# axis
LEFT_TRIGGER = 5
RIGHT_TRIGGER = 4
#LEFT_STICK = 1 and 0
LEFT_STICK_UP_DOWN = 0
LEFT_STICK_LEFT_RIGHT = 1
#RIGHT_STICK = 3 and 2
RIGHT_STICK_UP_DOWN = 2
RIGHT_STICK_LEFT_RIGHT = 3

# hats
'''
DOWN    [0][-1]
RIGHT   [1][0]
UP      [0][1]
LEFT    [-1][0]
'''


def startControllerListener():

    CONTROLLER_INPUT_ACTIVE = False
    START_IS_PRESSED = False  # button 11
    LEFT_BUMPER_PRESSED = False  # button 6
    RIGHT_BUMPER_PRESSED = False  # button 7

    LEFT_TRIGGER_PRESSED = 0
    RIGHT_TRIGGER_PRESSED = 0
    PAN = 0
    PAN_SPEED = 0
    PAN_PRESSED = 0
    TILT = 0
    TILT_SPEED = 0
    TILT_PRESSED = 0

    # Grab and initialize controller
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()

    gimbal = GimbalController('192.168.0.36', 10001)

    
    while controllerConnected():
        while not CONTROLLER_INPUT_ACTIVE and controllerConnected():
            # listen for events (button presses)
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
            gimbal.getStatusJog(0, 0, 0, 0, 4, 0, 0)
        # set and moveto preset code
        pygame.event.pump()
        if controller.get_button(LEFT_BUMPER):
            if controller.get_button(A):
                gimbal.saveCurrentPositionAsPreset(A)
            if controller.get_button(B):
                gimbal.saveCurrentPositionAsPreset(B)
            if controller.get_button(X):
                gimbal.saveCurrentPositionAsPreset(X)
            if controller.get_button(Y):
                gimbal.saveCurrentPositionAsPreset(Y)
            continue
        elif controller.get_button(RIGHT_BUMPER):
            if controller.get_button(A):
                gimbal.moveToPreset(A)
            if controller.get_button(B):
                gimbal.moveToPreset(B)
            if controller.get_button(X):
                gimbal.moveToPreset(X)
            if controller.get_button(Y):
                gimbal.moveToPreset(Y)
            continue
        else:
            # code for speed    
            LEFT_TRIGGER_PRESSED = controller.get_axis(LEFT_TRIGGER)
            RIGHT_TRIGGER_PRESSED = controller.get_axis(RIGHT_TRIGGER)
            print(LEFT_TRIGGER_PRESSED)
            print(RIGHT_TRIGGER_PRESSED)

            '''
            it is needed to set speed to 0 since 0 speed indicated no movement 
            0 direction is still a direction so we can not use this to mean that there is no movement
            '''
            if LEFT_TRIGGER_PRESSED == 0.0 or LEFT_TRIGGER_PRESSED == -1.0: # if no input set speed to 0
                PAN_SPEED = 0
                TILT_SPEED = 0
            if RIGHT_TRIGGER_PRESSED == 0.0 or RIGHT_TRIGGER_PRESSED == -1.0: # if no input set speed to 0
                PAN_SPEED = 0
                TILT_SPEED = 0
            '''
            this will get the axises
            these indicate what direction the gimbal is to move

            NOTE
            this code also has the code for setting the speed in the packet
            this is so that the gimbal can only move in one direction at a time
            if this needs to be changed simple change elif to if 
            '''
            PAN_PRESSED = controller.get_axis(LEFT_STICK_LEFT_RIGHT)
            TILT_PRESSED = controller.get_axis(LEFT_STICK_UP_DOWN)
            print(PAN_PRESSED)
            print(TILT_PRESSED)
            if PAN_PRESSED == 0.0 and TILT_PRESSED == 0.0:
                PAN = 0
                TILT = 0
                gimbal.getStatusJog(0, 0, 0, 0, 4, 0, 0)
            elif TILT_PRESSED > -.6 and TILT_PRESSED < .6:
                if PAN_PRESSED < 0: # basically sets the direction of the tilt
                    TILT = 64 # this is 64 as this bit is tilt 
                else:
                    TILT = 0
                if TILT_SPEED == 0:
                    TILT_SPEED = 1
                if LEFT_TRIGGER_PRESSED != -1.0 and LEFT_TRIGGER_PRESSED != 0.0: # -1 and 0 are what the controller gives for resting ie no input note that these are floats
                    TILT_SPEED = 2
                if RIGHT_TRIGGER_PRESSED != -1.0 and RIGHT_TRIGGER_PRESSED != 0.0: # -1 and 0 are what the controller gives for resting ie no input note that these are floats
                    TILT_SPEED = 3
            elif PAN_PRESSED > -.7 and PAN_PRESSED < .7:
                if TILT_PRESSED < 0: # basically sets the direction of the pan
                    PAN = 128 # this is 128 as this bit is pan
                else:
                    PAN = 0
                if PAN_SPEED == 0:
                    PAN_SPEED = 1
                if LEFT_TRIGGER_PRESSED != -1.0 and LEFT_TRIGGER_PRESSED != 0.0: # -1 and 0 are what the controller gives for resting ie no input note that these are floats
                    PAN_SPEED = 2
                if RIGHT_TRIGGER_PRESSED != -1.0 and RIGHT_TRIGGER_PRESSED != 0.0: # -1 and 0 are what the controller gives for resting ie no input note that these are floats
                    PAN_SPEED = 3
            # print(event)
            # gimbal.getStatusJog(0,0,0,0,4,0,0)
            print(PAN, TILT, PAN_SPEED, TILT_SPEED)
            gimbal.getStatusJog(PAN, TILT, PAN_SPEED, TILT_SPEED, 4, 0, 0)

    # Must disconnect the controller if it is to be used again
    controller.quit()
    CONTROLLER_INPUT_ACTIVE = False
    START_IS_PRESSED = False  # button 11
    LEFT_BUMPER_PRESSED = False  # button 6
    RIGHT_BUMPER_PRESSED = False  # button 7


def controllerConnected():
    return os.path.exists(CONTROLLER_DEVICE_PATH)


def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((1, 1))
    while True:
        while not controllerConnected():
            print("no controller found")
            time.sleep(15)
        else:
            startControllerListener()


if __name__ == '__main__':
    main()
