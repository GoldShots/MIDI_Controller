from pynput.mouse import Button

class Mapper:

    def __init__(self):

        # Sensitivity of Mouse Looping
        self.mouse_sens = 5

        # Keyboard Mappings
        self.key_mappings = {
            60: "w",
            61: "a",
            62: "s",
            63: "d",
        }

        # Mouse Button Mappings
        self.mouse_button_mappings = {
            64: Button.left,
            65: Button.right
        }

        # Mouse Mappings
        self.mouse_mappings = {
            66: (0, -self.mouse_sens), # Up
            67: (0, self.mouse_sens),  # Down
            68: (-self.mouse_sens, 0), # Left
            69: (self.mouse_sens, 0),  # Right
        }