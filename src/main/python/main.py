# Filename: run.py
# Author: Daniel Atonge

import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

# Imports for writing to the remote server
from pynput.keyboard import Key, Listener as keyboardlistener
from pynput.mouse import Listener as mouselistener
import time
import csv

# Imports for writing to the remote server
import os
import urllib.parse as up
import psycopg2

objective = 'development'

def getconnection():
    # up.uses_netloc.append("postgres")
    # url = up.urlparse(os.environ["postgres://gcurtgfe:m0WvGKAPOvjJrnmRJNMvwSmhIX5WwAOO@drona.db.elephantsql.com:5432/gcurtgfe"])
    try:
        connection = psycopg2.connect(database='gcurtgfe',
                                user='gcurtgfe',
                                password= 'm0WvGKAPOvjJrnmRJNMvwSmhIX5WwAOO',
                                host='drona.db.elephantsql.com',
                                port= 5432
                                )
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    return connection

def closeconnection(connection, cursor):
    #closing database connection.
    if(connection):
        connection.commit()
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def insert(cursor, documents, objective='development'):
    query = "INSERT INTO {}(idletime) Values ".format(objective)
    for document in documents:
        cursor.execute(query + '({});'.format(document))
    documents.clear()

# Global variables
starttime = time.time()
idlelist = list()


class MainApp(QMainWindow):
    
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Presence Tracker')
        self.setFixedSize(235, 180)
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        layout = self.vboxWidget()
        self.setCentralWidget(layout)
        # Collect mouse events
        self.mlistener = mouselistener( on_move=on_move, on_click=on_click, on_scroll=on_scroll )

        # Collect keyboard events
        self.klistener = keyboardlistener( on_release=on_release )
    
    def vboxWidget(self):
        layout = QVBoxLayout()

        self.combobox = QComboBox()
        self.combobox.addItem('Development')
        self.combobox.addItem('Reading')
        self.combobox.addItem('Others')
        self.combobox.currentIndexChanged.connect(self.updateObjective)
        
        self.startbtn = QPushButton('Start')
        self.startbtn.setCheckable(True)
        self.startbtn.clicked.connect(self.startbtnChangeState)
        self.startbtn.clicked.connect(self.startTracking)

        self.stopbtn = QPushButton('Stop')
        self.stopbtn.setCheckable(True)
        self.stopbtn.setEnabled(False)
        self.stopbtn.clicked.connect(self.stopbtnChangeState)
        self.stopbtn.clicked.connect(self.stopTracking)

        layout.addWidget(self.combobox)
        layout.addWidget(self.startbtn)
        layout.addWidget(self.stopbtn)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        #self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        #tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        global objective
        status = QStatusBar()
        status.showMessage(objective)
        self.setStatusBar(status)

    def startbtnChangeState(self):
        if self.startbtn.isEnabled():
            self.startbtn.setEnabled(False)
            self.stopbtn.setEnabled(True)
    
    def stopbtnChangeState(self):
        if self.stopbtn.isEnabled():
            self.stopbtn.setEnabled(False)
            self.startbtn.setEnabled(True)
        
    def updateObjective(self):
        global objective
        objective = self.combobox.currentText().lower()
        status = QStatusBar()
        status.showMessage(objective)
        self.setStatusBar(status)

    def startTracking(self):
        global connection, cursor
        connection = getconnection()
        cursor = connection.cursor()

        self.mlistener.start()
        #self.klistener.start()
    
    def stopTracking(self):
        global connection, cursor
        self.mlistener.stop()
        #self.klistener.stop()
        closeconnection(connection, cursor)
        connection = None
        cursor = None


# Returns the current time
def getcurrenttime():
    return time.time()

# Keyboard
def on_release(key):
    global starttime, idlelist, cursor, objective
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        idlelist.append(idletime)
    if (len(idlelist) > 100):
        insert(cursor, idlelist, objective)
    starttime = getcurrenttime()

# Mouse
def on_move(x, y):
    global starttime, idlelist, cursor, objective
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        idlelist.append(idletime)
    if (len(idlelist) > 100):
        insert(cursor, idlelist, objective)
    starttime = getcurrenttime()

def on_click(x, y, button, pressed):
    global starttime, idlelist, cursor, objective
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        idlelist.append(idletime)
        print(idletime)
    if (len(idlelist) > 5):
        insert(cursor, idlelist, objective)
    starttime = getcurrenttime()

def on_scroll(x, y, dx, dy):
    global starttime, idlelist, cursor, objective
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        idlelist.append(idletime)
    if (len(idlelist) > 100):
        insert(cursor, idlelist, objective)
    starttime = getcurrenttime()


if __name__ == '__main__':
    # Create an instance of QApplication
    appctxt = ApplicationContext()
    dlg = MainApp()

    # Show your application's GUI
    dlg.show()

    print("Running presence tracker")

    # Run your application's event loop (or main loop)
    appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
