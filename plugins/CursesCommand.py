"""
Curses console for sending commands local and remote in the format `l command args` or `r command args`
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import curses,os,sys

import logging
logger = logging.getLogger('spock')

class Screen:
	def __init__(self, stdscr, processor):
		self.timer = 0
		self.statusText = "SpockBot"
		self.searchText = '> '
		self.stdscr = stdscr
		self.cmdprocessor = processor

		# set screen attributes
		self.stdscr.nodelay(1) # this is used to make input calls non-blocking
		curses.cbreak()
		self.stdscr.keypad(1)
		curses.curs_set(0)     # no annoying mouse cursor

		self.rows, self.cols = self.stdscr.getmaxyx()
		self.lines = []

		curses.start_color()

		# create color pair's 1 and 2
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

		self.paintStatus(self.statusText)

	def connectionLost(self, reason):
		self.close()

	def addLine(self, text):
		""" add a line to the internal list of lines"""

		self.lines.append(text)
		self.redisplayLines()

	def redisplayLines(self):
		""" method for redisplaying lines 
			based on internal list of lines """

		self.stdscr.clear()
		self.paintStatus(self.statusText)
		try:
			i = 0
			index = len(self.lines) - 1
			while i < (self.rows - 3) and index >= 0:
				self.stdscr.addstr(self.rows - 3 - i, 0, self.lines[index], 
								   curses.color_pair(2))
				i = i + 1
				index = index - 1
		except:
			pass
		self.stdscr.refresh()

	def paintStatus(self, text):
		if len(text) > self.cols: raise TextTooLongError
		self.stdscr.addstr(self.rows-2,0,text + ' ' * (self.cols-len(text)), 
						   curses.color_pair(1))
		# move cursor to input line
		self.stdscr.move(self.rows-1, self.cols-1)

	def doRead(self):
		""" Input is ready! """
		curses.noecho()
		self.timer = self.timer + 1
		c = self.stdscr.getch() # read a character

		if c == curses.KEY_BACKSPACE:
			if len(self.searchText) > 2:
				self.searchText = self.searchText[:-1]

		elif c == curses.KEY_ENTER or c == 10:
			self.cmdprocessor.process_command(self.searchText[2:])
			self.stdscr.refresh()
			self.searchText = '> '

		else:
			if len(self.searchText) == self.cols-2: return
			try:
				self.searchText = self.searchText + chr(c)
			except:
				pass

		self.stdscr.addstr(self.rows-1, 0, 
						   self.searchText + (' ' * (
						   self.cols-len(self.searchText)-2)))
		self.stdscr.move(self.rows-1, len(self.searchText))
		self.paintStatus(self.statusText)
		self.stdscr.refresh()

	def close(self):
		""" clean up """
		curses.nocbreak()
		self.stdscr.keypad(0)
		curses.echo()
		curses.endwin()

class CommandProcessor:
	def __init__(self, event, net):
		self.event = event
		self.net = net
	
	def process_command(self, line):
		msg = line.split(' ')
		if len(msg) < 3:
			logger.info("Command: Not enough arguments")
			return
		loc = msg[0]
		command = msg[1]
		args = msg[2:]
		logger.info("Command: %s", command)
		if loc == 'l':
			self.event.emit('cmd_'+command, {'args': args})
		elif loc == 'r':
			self.net.push_packet('PLAY>Chat Message', {'message': command + ' ' + ' '.join(args)})


class CursesHandler(logging.Handler):
		def __init__(self, screen):
			logging.Handler.__init__(self)
			self.screen = screen
		def emit(self, record):
			msg = self.format(record)
			self.screen.addLine(msg)

class CursesCommandPlugin:
	def __init__(self, ploader, settings):
		self.event = ploader.requires('Event')
		self.net = ploader.requires('Net')
		stdscr = curses.initscr() # initialize curses
		cmd = CommandProcessor(self.event, self.net)
		self.screen = Screen(stdscr,cmd)   # create Screen object
		stdscr.refresh()
		logger.addHandler(CursesHandler(self.screen))

		ploader.reg_event_handler('event_tick', self.tick)
		ploader.reg_event_handler('kill', self.kill)

	def tmp(self, *args, **kargs):
		self.screen.addLine(' '.join(args))

	def tick(self, event, data):
		self.screen.doRead()

	def kill(self, event, data):
		self.screen.close()
