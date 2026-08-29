# Library Imports
import mido
import threading
import time
from pynput.mouse import Button, Controller

# Function Imports
from midi_input import listen
import keyboard_output
import mouse_output

# Temporarily getting midi device
device = mido.get_input_names()[1]

# Sensitivity of Mouse Looping
mouse_sens = 5

# Keyboard Mappings
key_mappings = {
    60: "w",
    61: "a",
    62: "s",
    63: "d",
}

mouse_button_mappings = {
    64: Button.left,
    65: Button.right
}

mouse_mappings = {
    66: (0, -mouse_sens), # Up
    67: (0, mouse_sens), # Down
    68: (-mouse_sens, 0), # Left
    69: (mouse_sens, 0), # Right
}

held_mouse_inputs = set()

def mouse_movement_loop():
    while True:
        for note in held_mouse_inputs:
            movement = mouse_mappings[note]

            if movement:
                x, y = movement
                mouse_output.move(x, y)

        time.sleep(0.01) # Update every 100 times/second

# Start mouse thread
mouse_thread = threading.Thread(target = mouse_movement_loop, daemon = True)

mouse_thread.start()


# Main MIDI Driver
for message in listen(device):
    # Pressing Key
    if message.type == "note_on":
        # If it is keyboard input
        if message.note in key_mappings:
            key = key_mappings.get(message.note)

            if key:
                keyboard_output.press(key)
        # If it is mouse button input
        if message.note in mouse_button_mappings:
            button = mouse_button_mappings.get(message.note)

            if button:
                mouse_output.press(button)
        # If it is a mouse movement
        if message.note in mouse_mappings:
            held_mouse_inputs.add(message.note)
    elif message.type == "note_off":
        # If it is keyboard input
        if message.note in key_mappings:
            key = key_mappings.get(message.note)

            if key:
                keyboard_output.release(key)
        # If it is mouse button input
        if message.note in mouse_button_mappings:
            button = mouse_button_mappings.get(message.note)

            if button:
                mouse_output.release(button)
        # If it is a mouse movement
        if message.note in mouse_mappings:
            movement = mouse_mappings.get(message.note)

            if movement:
                held_mouse_inputs.remove(movement)