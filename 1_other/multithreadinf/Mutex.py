# Program dealing with multi-threading, specifically multi-threading

# Importing libraries
from threading import *
from time import *


# Function display
def display(str1):
    l.acquire()
    for x in str1:
        print(x)
    l.release()


l = Lock()

# Creating and calling object
t1 = Thread(target=display, args=('HELLO WORLD ',))
t2 = Thread(target=display, args=('You are welcome',))

t1.start()
t2.start()

t1.join()
t2.join()
