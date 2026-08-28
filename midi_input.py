import mido
import pynput

print("MIDI devices: ")

for device in mido.get_input_names():
    print(device)

device = mido.get_input_names()[1]

with mido.open_input(device) as port:
    print(f"Listening to {device}...")

    for message in port:
        print(message)