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
        ...

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

    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setEditTriggers(QTableWidget.NoEditTriggers)

    edit_button = QPushButton("Edit Mapping", parent = window)
    edit_button.move(20, 365)

    edit_button.clicked.connect(
        lambda: edit_mapping(table, mapper)
    )

    window.show()

    return app, window