"""
Readline console for sending commands localy and remotely
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import time,readline,thread,sys

class CustomPrint(object):
	def __init__(self):
		self.out=sys.stdout

	def write(self, text):
		self.out.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
		self.out.write(text)
		self.out.write('> ' + readline.get_line_buffer())
		self.out.flush()

sys.stdout = CustomPrint()

class ReadLinePlugin:
	def __init__(self, ploader, settings):
		self.event = ploader.requires('Event')
		thread.start_new_thread(self.readthread, ())

	def readthread(self):
		while True:
			s = input('> ')
