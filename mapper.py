from pynput.mouse import Button

class Mapper:
    def __init__(self):
        # Sensitivity of Mouse Looping
        self.mouse_sens = 5

        # Mappings
        self.mappings = {
            60: ("Keyboard", "w"),
            61: ("Keyboard", "a"),
            62: ("Keyboard", "s"),
            63: ("Keyboard", "d"),

            64: ("Mouse Button", Button.left),
            65: ("Mouse Button", Button.right),

            66: ("Mouse Movement", (0, -self.mouse_sens)), # Up
            67: ("Mouse Movement", (0, self.mouse_sens)),  # Down
            68: ("Mouse Movement", (-self.mouse_sens, 0)), # Left
            69: ("Mouse Movement", (self.mouse_sens, 0)),  # Right
        }