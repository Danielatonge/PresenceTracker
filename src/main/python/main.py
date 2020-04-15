# Filename: run.py
# Author: Daniel Atonge

from PyQt5.QtCore import QThread

# Imports for writing to the remote server
import os
import psycopg2

# Imports for writing to the remote server
from pynput.keyboard import Key, Listener as keyboardlistener
from pynput.mouse import Listener as mouselistener
import time

class MHook(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.starttime = time.time()
        self.idlelist = list()
        self.objective = 'development'
        self.connection = None
        self.cursor = None
        
    
    # Returns the current time
    def getcurrenttime(self):
        return time.time()

    def run(self):
        self.Listen()

    def connect(self):
        self.connection = self.getconnection()
        self.cursor = self.connection.cursor()
        
    def getconnection(self):
        try:
            connection = psycopg2.connect(database='gcurtgfe',
                                    user='gcurtgfe',
                                    password= 'm0WvGKAPOvjJrnmRJNMvwSmhIX5WwAOO',
                                    host='drona.db.elephantsql.com',
                                    port= 5432
                                    )
            connection.autocommit = True
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        return connection

    def commitChanges(self):
        self.connection.commit()
        

    def closeconnection(self):
        #closing database connection.
        if(self.connection):
            self.connection.close()
            print("Connection is closed")

    def insert(self):
        all_docs = [{'idletime': doc} for doc in self.idlelist]
        query = "INSERT INTO {}(idletime) Values ".format(self.objective)
        try:
            self.cursor.executemany( query + "(%(idletime)s);", all_docs)
        except Exception as e:
            print(e)
        self.idlelist.clear()

    # Keyboard
    def on_release(self, key):
        idletime = round(time.time() - self.starttime, 1)
        if (idletime > 0.0):
            self.idlelist.append(idletime)
            print(str(key))
        if (len(self.idlelist) > 100):
            self.insert()
        self.starttime = self.getcurrenttime()

    # Mouse
    def on_move(self, x, y):
        idletime = round(time.time() - self.starttime, 1)
        if (idletime > 0.0):
            self.idlelist.append(idletime)
        if (len(self.idlelist) > 100):
            self.insert()
        self.starttime = self.getcurrenttime()

    def on_click(self, x, y, button, pressed):
        idletime = round(time.time() - self.starttime, 1)
        if (idletime > 0.0):
            self.idlelist.append(idletime)
        if (len(self.idlelist) > 5):
            print(self.idlelist)
            self.insert()
        self.starttime = self.getcurrenttime()

    def on_scroll(self, x, y, dx, dy):
        idletime = round(time.time() - self.starttime, 1)
        if (idletime > 0.0):
            self.idlelist.append(idletime)
        if (len(self.idlelist) > 100):
            self.insert()
        self.starttime = self.getcurrenttime()

    def Listen(self):
            # Collect mouse events
        with mouselistener(on_move=self.on_move,on_click=self.on_click,on_scroll=self.on_scroll) as listener:
            # Collect keyboard events
            with keyboardlistener(on_release=self.on_release) as listener:
                listener.join()

import sys
#from MHook import MHook

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
        self.hook_thread = None
        self.statusbartxt = "start tracking"

    def closeEvent(self, event):
        self.hook_thread.closeconnection()
        event.accept()

    def vboxWidget(self):
        layout = QVBoxLayout()

        self.objective = 'development'

        self.combobox = QComboBox()
        self.combobox.addItem('Development')
        self.combobox.addItem('Reading')
        self.combobox.addItem('Others')
        self.combobox.currentIndexChanged.connect(self.updateObjective)
        
        self.startbtn = QPushButton('Start')
        self.startbtn.pressed.connect(self.startbtnChangeState)
        self.startbtn.pressed.connect(self.startTracking)

        self.stopbtn = QPushButton('Stop')
        self.stopbtn.setEnabled(False)
        self.stopbtn.pressed.connect(self.stopbtnChangeState)
        self.stopbtn.pressed.connect(self.stopTracking)

        layout.addWidget(self.combobox)
        layout.addWidget(self.startbtn)
        layout.addWidget(self.stopbtn)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _createMenu(self):
        pass
        #self.menu = self.menuBar().addMenu("&Menu")
        #self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        #tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("start tracking")
        self.setStatusBar(self.status)

    def updateStatusBar(self):
        self.status.showMessage(self.statusbartxt)

    def startbtnChangeState(self):
        if self.startbtn.isEnabled():
            self.startbtn.setEnabled(False)
            self.stopbtn.setEnabled(True)
    
    def stopbtnChangeState(self):
        if self.stopbtn.isEnabled():
            self.stopbtn.setEnabled(False)
            self.startbtn.setEnabled(True)
        
    def updateObjective(self):
        self.objective = self.combobox.currentText().lower()
        self.statusbartxt = self.objective
        self.updateStatusBar()
        

    def startTracking(self):
        self.combobox.setEnabled(False)
        self.hook_thread = MHook(self)
        self.hook_thread.objective = self.objective
        self.hook_thread.connect()
        self.hook_thread.start()
        self.statusbartxt = 'Process started'
        self.updateStatusBar()
    
    def stopTracking(self):
        self.hook_thread.quit()
        self.hook_thread.commitChanges()
        self.combobox.setEnabled(True)
        self.statusbartxt = 'Process stop'
        self.updateStatusBar()


if __name__ == '__main__':
    # Create an instance of QApplication
    #appctxt = QApplication(sys.argv)
    appctxt = ApplicationContext()
    dlg = MainApp()

    # Show your application's GUI
    dlg.show()

    print("Running presence tracker")

    # Run your application's event loop (or main loop)
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
    #sys.exit(appctxt.exec_())