import mido

print("MIDI devices: ")

for device in mido.get_input_names():
    print(device)