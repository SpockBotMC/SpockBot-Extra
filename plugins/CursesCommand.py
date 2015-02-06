"""
Curses console for sending commands local and remote
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

class CursesCommandPlugin:
	def __init__(self, ploader, settings):
		self.event = ploader.requires('Event')
