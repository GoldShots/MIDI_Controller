# Library Imports
import mido
import threading
import time
import sys
import os

# File Imports
from midi_input import listen
import keyboard_output
import mouse_output
from mapper import Mapper
from gui import create_gui

# Create Mapper
mapper = Mapper()

# Main MIDI Driver
def midi_loop(device):
    for message in listen(device):
        # Pressing Key
        if message.note in mapper.mappings:
            mapping_type, mapping = mapper.mappings[message.note]

            if message.type == "note_on":
                if mapping_type == "Keyboard":
                    keyboard_output.press(mapping)
                elif mapping_type == "Mouse Button":
                    mouse_output.press(mapping)
                elif mapping_type == "Mouse Movement":
                    with held_mouse_inputs_lock:
                        held_mouse_inputs.add(message.note)
            elif message.type == "note_off":
                if mapping_type == "Keyboard":
                    keyboard_output.release(mapping)
                elif mapping_type == "Mouse Button":
                    mouse_output.release(mapping)
                elif mapping_type == "Mouse Movement":
                    with held_mouse_inputs_lock:
                        held_mouse_inputs.discard(message.note)

# Function to connect midi
def connect_midi(device):
    midi_thread = threading.Thread(
        target = midi_loop,
        args = (device,),
        daemon = True
    )

    midi_thread.start()

# Held Mouse Inputs
held_mouse_inputs = set()
held_mouse_inputs_lock = threading.Lock()

def mouse_movement_loop():
    while True:
        with held_mouse_inputs_lock:
            held_notes = list(held_mouse_inputs)

        for note in held_notes:
            mapping_type, movement = mapper.mappings[note]

            if movement:
                x, y = movement
                mouse_output.move(x, y)

        time.sleep(0.01) # Update every 100 times/second

# Start mouse thread
mouse_thread = threading.Thread(target = mouse_movement_loop, daemon = True)
mouse_thread.start()

# Create GUI
app, window = create_gui(mapper, connect_midi)
sys.exit(app.exec())
