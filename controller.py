import pygame
import time
import os.path

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
#RIGHT_STICK = 3 and 2

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

    #Grab and initialize controller
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()

    #listen for events (button presses)
    while controllerConnected():
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
            elif CONTROLLER_INPUT_ACTIVE:
                print(event)
    
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