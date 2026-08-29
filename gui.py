from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QComboBox
)

from PySide6.QtCore import Qt
from pynput.mouse import Button
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

    dialog = QDialog(table)
    dialog.setWindowTitle("Edit Mapping")

    layout = QVBoxLayout(dialog)

    output_type = QComboBox()
    output_type.addItems([
        "Keyboard",
        "Mouse Button",
        "Mouse Movement"
    ])

    layout.addWidget(output_type)

    save_button = QPushButton("Save")
    layout.addWidget(save_button)

    save_button.clicked.connect(dialog.accept)

    if dialog.exec():
        selected_type = output_type.currentText()

        if selected_type == "Keyboard":
            mapper.mappings[note] = ("Keyboard", "w")
        elif selected_type == "Mouse Button":
            mapper.mappings[note] = ("Mouse Button", Button.left)
        elif selected_type == "Mouse Movement":
            mapper.mappings[note] = ("Mouse Movement", (0, -mapper.mouse_sens))

        table.item(row, 1).setText(selected_type)

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

    edit_button = QPushButton("Edit Mapping", parent = window)
    edit_button.move(20, 365)
    edit_button.clicked.connect(
        lambda: edit_mapping(table, mapper)
    )

    window.show()

    return app, window