#!/usr/bin/env python

'''
This is a wrapper script that imports all the pictureframe classes, and fires each off in it's own thread.
'''

import sys
from threading import Thread

def startAPI():
	pass

def startCache():
	pass

def startPygame():
	pass

t1 = threading.Thread(target=someFunc)
t1.start()
t1.join()
