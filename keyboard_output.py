from pynput.keyboard import Controller

keyboard = Controller()

def press(key):
    keyboard.press(key)

def release(key):
    keyboard.release(key)