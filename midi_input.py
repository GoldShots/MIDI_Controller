import mido

def listen(device):
    print(f"Listening to {device}...")
    
    with mido.open_input(device) as port:
        for message in port:
            yield message