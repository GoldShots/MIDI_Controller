# Library Imports
import mido
import threading
import time
import sys

# Function Imports
from midi_input import listen
import keyboard_output
import mouse_output
from mapper import Mapper
from gui import create_gui

# Temporarily getting midi device
device = mido.get_input_names()[1]

# Create Mapper
mapper = Mapper()

# Held Mouse Inputs
held_mouse_inputs = set()

# Create GUI
app, window = create_gui(device, mapper)

sys.exit(app.exec())

def mouse_movement_loop():
    while True:
        for note in held_mouse_inputs:
            movement = mapper.mouse_mappings[note]

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
        if message.note in mapper.key_mappings:
            key = mapper.key_mappings.get(message.note)

            if key:
                keyboard_output.press(key)
        # If it is mouse button input
        if message.note in mapper.mouse_button_mappings:
            button = mapper.mouse_button_mappings.get(message.note)

            if button:
                mouse_output.press(button)

        # If it is mouse movement input
        if message.note in mapper.mouse_mappings:
            held_mouse_inputs.add(message.note)

    elif message.type == "note_off":
        # If it is keyboard input
        if message.note in mapper.key_mappings:
            key = mapper.key_mappings.get(message.note)

            if key:
                keyboard_output.release(key)
        # If it is mouse button input
        if message.note in mapper.mouse_button_mappings:
            button = mapper.mouse_button_mappings.get(message.note)

            if button:
                mouse_output.release(button)

        # If it is mouse movement input
        if message.note in mapper.mouse_mappings:
            held_mouse_inputs.discard(message.note)