# Program that deals with Inter-Process Communication with queue

# Importing libraries
from threading import *
from time import *
from queue import *

# Queue module object
q = Queue()


# Functions for producing and consuming
def producer(que):
    i = 1
    while True:
        que.put(i)
        print('Producer: ', i)
        sleep(1)
        i += 1


def consumer(que):
    while True:
        x = que.get()
        #sleep(1)
        print('Consumer: ', x)


# Creating and calling objects
t1 = Thread(target=lambda: producer(q))
t2 = Thread(target=lambda: consumer(q))

t1.start()
t2.start()

t1.join()
t2.join()
