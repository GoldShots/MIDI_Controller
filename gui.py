from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QComboBox,
    QSpinBox
)

from PySide6.QtCore import Qt, QTimer
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import mido
import sys
import os

class MainWindow(QWidget):

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

def midi_note_name(note):
    names = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    octave = int(note / 12) - 1

    return f"{names[note % 12]}{octave}"

def edit_mapping(table, mapper):
    row = table.currentRow()

    if row < 0:
        return

    note_item = table.item(row, 0)

    if note_item is None:
        return

    note = note_item.data(Qt.UserRole)

    mapping_type, mapping = mapper.mappings[note]

    dialog = QDialog(table)
    dialog.setWindowTitle("Edit Mapping")
    dialog.resize(300, 200)

    layout = QVBoxLayout(dialog)

    # MIDI Note
    midi_note = QSpinBox()
    midi_note.setRange(0, 127)
    midi_note.setValue(note)

    layout.addWidget(midi_note)

    # Output Type
    output_type = QComboBox()
    output_type.addItems([
        "Keyboard",
        "Mouse Button",
        "Mouse Movement"
    ])
    output_type.setCurrentText(mapping_type)

    layout.addWidget(output_type)

    # Input
    input_label = QLabel()

    layout.addWidget(input_label)

    input_selection = QComboBox()

    layout.addWidget(input_selection)

    sensitivity = QSpinBox()
    sensitivity.setRange(1, 100)
    sensitivity.setValue(mapper.mouse_sens)

    layout.addWidget(sensitivity)

    captured_input = None
    keyboard_listener = None
    mouse_listener = None

    def start_keyboard_listener():
        nonlocal keyboard_listener

        def on_press(key):
            nonlocal captured_input

            captured_input = key

            keyboard_listener.stop()

        keyboard_listener = KeyboardListener(
            on_press = on_press
        )

        keyboard_listener.start()

    def start_mouse_listener():
        nonlocal mouse_listener

        def on_click(x, y, button, pressed):
            nonlocal captured_input

            if pressed:
                captured_input = button

                mouse_listener.stop()

        mouse_listener = MouseListener(
            on_click = on_click
        )

        mouse_listener.start()

    timer = QTimer(dialog)

    def update_captured_input():
        if captured_input is not None:

            input_label.setText(
                f"Selected: {captured_input}"
            )

    timer.timeout.connect(update_captured_input)

    timer.start(50)

    def update_input_options():
        nonlocal keyboard_listener, mouse_listener, captured_input

        if keyboard_listener:
            keyboard_listener.stop()
            keyboard_listener = None

        if mouse_listener:
            mouse_listener.stop()
            mouse_listener = None

        input_selection.clear()
        captured_input = None

        selected_type = output_type.currentText()

        if selected_type == "Keyboard":
            input_label.setText("Press a key...")
            input_selection.hide()

            sensitivity.hide()

            start_keyboard_listener()
        elif selected_type == "Mouse Button":
            input_label.setText("Click a mouse button...")
            input_selection.hide()

            sensitivity.hide()

            start_mouse_listener()
        elif selected_type == "Mouse Movement":
            input_label.setText("Direction:")
            input_selection.addItems([
                "Up",
                "Down",
                "Left",
                "Right"
            ])
            input_selection.show()

            sensitivity.show()

    output_type.currentTextChanged.connect(update_input_options)

    update_input_options()

    # Buttons
    save_button = QPushButton("Save")
    cancel_button = QPushButton("Cancel")

    layout.addWidget(save_button)
    layout.addWidget(cancel_button)

    save_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)

    if dialog.exec():
        new_note = midi_note.value()
        new_type = output_type.currentText()

        # Removing duplicate midi note mappings
        if new_note in mapper.mappings:
            mapper.mappings.pop(new_note)

        # Removing old MIDI mapping if it was changed.
        if new_note != note:
            mapper.mappings.pop(note)

        mapper.mappings[new_note] = (new_type, captured_input)

def create_gui(mapper, connect_callback):
    app = QApplication(sys.argv)

    # Find style.qss path
    style_path = os.path.join(os.path.dirname(__file__), "style.qss")

    with open(style_path, "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.setWindowTitle("MIDI to Controller")
    window.resize(600, 410)

    label = QLabel("MIDI to Controller", parent = window)
    label.move(20, 20)

    # Device Dropdown
    device_dropdown = QComboBox(parent = window)
    device_dropdown.addItems(mido.get_input_names())
    device_dropdown.move(20, 20)
    device_dropdown.resize(300, 30)

    device = mido.get_input_names()[0]

    if device in mido.get_input_names():
        device_dropdown.setCurrentText(device)


    # Connect Button
    connect_button = QPushButton("Connect", parent = window)
    connect_button.move(330, 20)
    connect_button.resize(100, 30)
    connect_button.clicked.connect(
        lambda: connect_callback(device_dropdown.currentText())
    )

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

    # Add Mappings
    for note, mapping_data in mapper.mappings.items():
        mapping_type, mapping = mapping_data

        row = table.rowCount()

        table.insertRow(row)

        note_item = QTableWidgetItem(midi_note_name(note))
        note_item.setData(Qt.UserRole, note)

        table.setItem(
            row,
            0,
            note_item
        )
        table.setItem(
            row,
            1,
            QTableWidgetItem(mapping_type)
        )

        if mapping_type == "Keyboard":
            mapping_text = mapping
        elif mapping_type == "Mouse Button":
            mapping_text = str(mapping)
        elif mapping_type == "Mouse Movement":
            x, y = mapping

            if x > 0:
                mapping_text = "Right"
            elif x < 0:
                mapping_text = "Left"
            elif y > 0:
                mapping_text = "Down"
            else:
                mapping_text = "Up"

        table.setItem(
            row,
            2,
            QTableWidgetItem(mapping_text)
        )

    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setEditTriggers(QTableWidget.NoEditTriggers)

    # Edit Mapping Button
    edit_button = QPushButton("Edit Mapping", parent = window)
    edit_button.move(20, 365)
    edit_button.clicked.connect(
        lambda: edit_mapping(table, mapper)
    )

    window.show()

    return app, window