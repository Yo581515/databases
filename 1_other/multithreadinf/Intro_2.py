# Prorgam dealing with threading, based on a class and its method

# Importing libraries
from threading import *
from time import *


# Alphabets class
class Alphabets(Thread):
    def run(self):
        for i in range(65, 91):
            print(chr(i))
            sleep(.1)


# Creating the object
t = Alphabets()
t.start()
for i in range(65, 91):
    print(i)
    sleep(.1)
