from pynput.keyboard import Key, Listener as keyboardlistener
from pynput.mouse import Listener as mouselistener
import time
import csv

# Global variables
count = 0
starttime = time.time()
f = open('userpresence.csv', 'a+')

# Returns the current time
def getcurrenttime():
    return time.time()

# Keyboard
def on_release(key):
    global count, starttime, writer
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        count += 1
        writer.writerow([count,idletime])
    starttime = getcurrenttime()
    if key == Key.esc:
        return exit()
# Mouse
def on_move(x, y):
    global count, starttime
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        count += 1
        writer.writerow([count,idletime])
    starttime = getcurrenttime()

def on_click(x, y, button, pressed):
    global count, starttime
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        count += 1
        writer.writerow([count,idletime])
    starttime = getcurrenttime()

def on_scroll(x, y, dx, dy):
    global count, starttime
    idletime = round(time.time() - starttime, 1)
    if (idletime > 0.0):
        count += 1
        writer.writerow([count,idletime])
    starttime = getcurrenttime()


def run():
    # Collect mouse events
    with mouselistener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        # Collect keyboard events
        with keyboardlistener( on_release=on_release) as listener:
            listener.join()

with f:
    writer = csv.writer(f)
    writer.writerow(['count', 'idletime'])
    print("Running presence tracker")
    run()