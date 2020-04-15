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
    # up.uses_netloc.append("postgres")
    # url = up.urlparse(os.environ["postgres://gcurtgfe:m0WvGKAPOvjJrnmRJNMvwSmhIX5WwAOO@drona.db.elephantsql.com:5432/gcurtgfe"])
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
