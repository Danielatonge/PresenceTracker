from pynput.keyboard import Key, Listener as keyboardlistener
from pynput.mouse import Listener as mouselistener
import time
import csv

f = open('userpresence.csv', 'a+')

with f:
    
    fnames = ['count', 'Idletime']
    writer = csv.DictWriter(f, fieldnames=fnames)    
    writer.writeheader()
    print("Running presence tracker")
    
    def getcurrenttime():
        return time.time()

    count = 0
    starttime = time.time()
    # Keyboard
    def on_release(key):
        global count, starttime, writer
        idletime = round(time.time() - starttime, 1)
        if (idletime > 0.0):
            count += 1
            writer.writerow({'count': count, 'Idletime': idletime})
        starttime = getcurrenttime()
        

    # Mouse
    def on_move(x, y):
        global count, starttime
        idletime = round(time.time() - starttime, 1)
        if (idletime > 0.0):
            count += 1
            writer.writerow({'count': count, 'Idletime': idletime})
        starttime = getcurrenttime()

    def on_click(x, y, button, pressed):
        global count, starttime
        idletime = round(time.time() - starttime, 1)
        if (idletime > 0.0):
            count += 1
            writer.writerow({'count': count, 'Idletime': idletime})
        starttime = getcurrenttime()

    def on_scroll(x, y, dx, dy):
        global count, starttime
        idletime = round(time.time() - starttime, 1)
        if (idletime > 0.0):
            count += 1
            writer.writerow({'count': count, 'Idletime': idletime})
        starttime = getcurrenttime()

    # Collect keyboard events
    with keyboardlistener( on_release=on_release) as listener:
        # Collect mouse events
        with mouselistener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()

#Inn0pOl1s$2020