from PySide6.QtWidgets import QApplication, QWidget, QLabel, QTableWidgetItem, QTableWidget

import sys

class MainWindow(QWidget):

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

def midi_note_name(note):
    names = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    octave = (int)(note / 12) - 1

    return f"{names[note % 12]}{octave}"

def create_gui(device, mapper):

    app = QApplication(sys.argv)

    window = MainWindow()

    window.setWindowTitle("MIDI to Controller")
    window.resize(600, 400)

    label = QLabel("MIDI to Controller", parent = window)
    label.move(20, 20)

    # Mapping Table
    table = QTableWidget(parent = window)

    table.setColumnCount(3)
    table.setHorizontalHeaderLabels([
        "MIDI Note",
        "Output Type", 
        "Mapping"
    ])

    table.move(20, 60)
    table.resize(560, 300)

    # Add Keyboard Mappings
    for note, key in mapper.key_mappings.items():
        row = table.rowCount()
        table.insertRow(row)

        table.setItem(
            row,
            0,
            QTableWidgetItem(midi_note_name(note))
        )

        table.setItem(
            row,
            1,
            QTableWidgetItem("Keyboard")
        )

        table.setItem(
            row,
            2,
            QTableWidgetItem(key)
        )

    # Add mouse button mappings
    for note, button in mapper.mouse_button_mappings.items():
        row = table.rowCount()
        table.insertRow(row)

        table.setItem(
            row,
            0,
            QTableWidgetItem(midi_note_name(note))
        )

        table.setItem(
            row,
            1,
            QTableWidgetItem("Mouse Button")
        )

        table.setItem(
            row,
            2,
            QTableWidgetItem(str(button))
        )

    # Add mouse movement mappings
    for note, movement in mapper.mouse_mappings.items():
        row = table.rowCount()
        table.insertRow(row)

        table.setItem(
            row,
            0,
            QTableWidgetItem(midi_note_name(note))
        )

        table.setItem(
            row,
            1,
            QTableWidgetItem("Mouse")
        )

        x, y = movement

        if x > 0:
            mapping = "Right"

        elif x < 0:
            mapping = "Left"

        elif y > 0:
            mapping = "Down"

        else:
            mapping = "Up"

        table.setItem(
            row,
            2,
            QTableWidgetItem(mapping)
        )

    window.show()

    return app, window