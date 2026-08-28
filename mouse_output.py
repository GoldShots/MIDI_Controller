from pynput.mouse import Button, Controller

mouse = Controller()

def move(x, y):
    mouse.move(x, y)

def press(button):
    mouse.press(button)

def release(button):
    mouse.release(button)