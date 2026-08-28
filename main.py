# Library Imports
import mido

# Function Imports
from midi_input import listen
import keyboard_output
import mouse_output
from pynput.mouse import Button

# Temporarily getting midi device
device = mido.get_input_names()[1]

# Keyboard Mappings
key_mappings = {
    60: "w",
    61: "a",
    62: "s",
    63: "d",
}

mouse_mappings = {
    64: Button.left
}

for message in listen(device):
    # Pressing Key
    if message.type == "note_on":
        # If it is keyboard input
        if message.note in key_mappings:
            key = key_mappings.get(message.note)

            if key:
                keyboard_output.press(key)
    elif message.type == "note_off":
        # If it is keyboard input
        if message.note in key_mappings:
            key = key_mappings.get(message.note)

            if key:
                keyboard_output.release(key)