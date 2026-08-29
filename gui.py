from PySide6.QtWidgets import QApplication, QWidget, QLabel

import sys

class MainWindow(QWidget):

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

def create_gui(device, mapper):

    app = QApplication(sys.argv)

    window = MainWindow()

    window.setWindowTitle("MIDI to Controller")
    window.resize(600, 400)

    label = QLabel("MIDI to Controller", parent=window)
    label.move(20, 20)

    window.show()

    return app, window