"""
Readline console for sending commands localy and remotely
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import time,readline,sys,os
try:
	import thread
except ImportError:
	import _thread as thread

class ReadlinePrint(object):
	def __init__(self):
		self.oldout = sys.stdout
		self.flush = sys.stdout.flush
		self.errors = sys.stdout.errors
		self.encoding = sys.stdout.encoding

	def write(self, text):
		if text.rstrip(os.linesep) == '':
			return
		self.oldout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
		self.oldout.write(text + "\n")
		self.oldout.write("> " + readline.get_line_buffer())
		self.oldout.flush()

sys.stdout = ReadlinePrint()

class CursesCommandPlugin:
	def __init__(self, ploader, settings):
		self.event = ploader.requires('Event')
		thread.start_new_thread(self.readthread, ())

	def readthread(self):
		while True:
			s = raw_input('> ')
