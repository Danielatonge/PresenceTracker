# Filename: run.py
# Author: Daniel Atonge
"""Simple Hello World example with PyQt5."""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Presence Tracker')
layout = QVBoxLayout()
combobox = QComboBox()
combobox.addItem('Reading')
combobox.addItem('Development')
combobox.addItem('Others')
layout.addWidget(combobox)
layout.addWidget(QPushButton('Start'))
layout.addWidget(QPushButton('Stop'))
window.setLayout(layout)

# Show your application's GUI
window.show()

# Run your application's event loop (or main loop)
sys.exit(app.exec_())