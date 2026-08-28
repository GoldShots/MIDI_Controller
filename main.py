# Library Imports
import mido

# Function Imports
from midi_input import listen
import keyboard_output

# Temporarily getting midi device
device = mido.get_input_names()[1]

# Keyboard Mappings
mappings = {
    60: "w",
    61: "a",
    62: "s",
    63: "d"
}

for message in listen(device):
    # Pressing Key
    if message.type == "note_on":
        key = mappings.get(message.note)

        if key:
            keyboard_output.press(key)

    # Releasing Key
    elif message.type == "note_off":
            key = mappings.get(message.note)
    
            if key:
                keyboard_output.release(key)