# Library Imports
import mido

# Function Imports
from midi_input import listen

# Temporarily getting midi device
device = mido.get_input_names()[1]

for message in listen(device):
    print(message)