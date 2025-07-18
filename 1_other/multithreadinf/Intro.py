# Program introduction to multithreading

# Importing libraries
from threading import *
from time import *


# Creating the target function
def display():
    for x in range(65, 91):
        print(chr(x))
        sleep(0.1)


# Creating threading object and calling the desired target
t = Thread(target=display, name='Alphabets')
t.start()
for i in range(65, 91):
    print(i)
t.join()