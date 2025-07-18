# Program dealing with semaphores

# Importing libraries
from threading import *
from time import *


# Display function
def display(str1):
    l.acquire()
    for x in str1:
        print(x)
        sleep(.01)
    l.release()


# Assigning semaphore
l = Semaphore(1)

# Creating and calling objects
t1 = Thread(target=display, args=('HELLO WORLD',))
t2 = Thread(target=display, args=('you are welcome',))
t3 = Thread(target=display, args=('0123456789',))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
