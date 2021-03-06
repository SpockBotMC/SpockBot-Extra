"""
Curses console for sending commands local and remote in the format `command args` or `/command args`
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import curses
import logging
import sys

from spockbot.mcp.mcdata import (
    GM_ADVENTURE, GM_CREATIVE, GM_SPECTATOR, GM_SURVIVAL
)

from spockbot.plugins.base import PluginBase

logger = logging.getLogger('spockbot')

PROMPT = '> '


class Screen:
    def __init__(self, stdscr, processor):
        self.timer = 0
        self.statusText = "SpockBot"
        self.searchText = PROMPT
        self.commands = []
        self.commandindex = 0
        self.cursorpos = len(self.searchText)
        self.stdscr = stdscr
        self.cmdprocessor = processor
        self.ignorekeys = [curses.KEY_MOUSE]

        # set screen attributes
        self.stdscr.nodelay(1)  # this is used to make input calls non-blocking
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(1)     # no annoying mouse cursor

        self.rows, self.cols = self.stdscr.getmaxyx()
        self.lines = []

        curses.start_color()

        # create color pair's 1 and 2
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.paint_status(self.statusText)

    def connection_lost(self, reason):
        self.close()

    def add_line(self, text):
        """ add a line to the internal list of lines"""

        self.lines.append(text)
        self.redisplay_lines()

    def redisplay_lines(self):
        """ method for redisplaying lines
            based on internal list of lines """

        self.stdscr.clear()
        self.paint_status(self.statusText)
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

    def paint_status(self, text):
        if len(text) > self.cols:
            text = text[self.cols:]
        self.stdscr.addstr(self.rows-2, 0, text + ' ' * (self.cols-len(text)),
                           curses.color_pair(1))
        # move cursor to input line
        self.stdscr.move(self.rows-1, self.cursorpos)

    def set_search_text(self, text):
        self.searchText = text
        self.cursorpos = len(self.searchText)

    def do_read(self):
        """ Input is ready! """
        curses.noecho()
        self.timer = self.timer + 1
        c = self.stdscr.getch()  # read a character
        if c in self.ignorekeys:
            pass

        elif c == curses.KEY_BACKSPACE or c == 127:
            if len(self.searchText) > len(PROMPT):
                if self.cursorpos == len(self.searchText):
                    self.set_search_text(self.searchText[:-1])
                elif self.cursorpos < len(self.searchText):
                    self.searchText = self.searchText[:self.cursorpos-1] + self.searchText[self.cursorpos:]
                    self.cursorpos -= 1

        elif c == curses.KEY_ENTER or c == 10:
            self.cmdprocessor.process_command(self.searchText[2:])
            self.commands.append(self.searchText[2:])
            self.commandindex = len(self.commands)
            self.stdscr.refresh()
            self.set_search_text(PROMPT)
        elif c == curses.KEY_UP:
            if self.commandindex-1 >= 0:
                self.commandindex -= 1
                self.set_search_text(PROMPT + self.commands[self.commandindex])
        elif c == curses.KEY_DOWN:
            if self.commandindex+1 < len(self.commands):
                self.commandindex += 1
                self.set_search_text(PROMPT + self.commands[self.commandindex])
        elif c == curses.KEY_LEFT:
            self.cursorpos -= 1
            if self.cursorpos < len(PROMPT):
                self.cursorpos = len(PROMPT)
        elif c == curses.KEY_RIGHT:
            self.cursorpos += 1
            if self.cursorpos > len(self.searchText):
                self.cursorpos = len(self.searchText)
        else:
            if len(self.searchText) == self.cols-2:
                return
            try:
                if self.cursorpos == len(self.searchText):
                    self.set_search_text(self.searchText + chr(c))
                elif self.cursorpos < len(self.searchText):
                    self.searchText = self.searchText[:self.cursorpos] + chr(c) + self.searchText[self.cursorpos:]
                    self.cursorpos += 1
            except:
                pass

        self.stdscr.addstr(self.rows-1, 0,
                           self.searchText + (' ' * (
                           self.cols-len(self.searchText)-2)))
        self.stdscr.move(self.rows-1, self.cursorpos)
        self.paint_status(self.statusText)
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
        if line[0] == '/':
            self.net.push_packet('PLAY>Chat Message', {'message': line})
        else:
            msg = line.split(' ')
            command = msg[0]
            args = msg[1:]
            logger.info("Command: %s Args: %s", command, args)
            self.event.emit('cmd_'+command, {'args': args})


class CursesHandler(logging.Handler):
        def __init__(self, screen):
            logging.Handler.__init__(self)
            self.screen = screen

        def emit(self, record):
            msg = self.format(record)
            self.screen.add_line(msg)


class CursesCommandPlugin(PluginBase):
    requires = ('Event', 'Net', 'ClientInfo')
    events = {
        'event_tick': 'tick',
        'event_kill': 'kill',
    }

    def __init__(self, ploader, settings):
        super(CursesCommandPlugin, self).__init__(ploader, settings)
        stdscr = curses.initscr()  # initialize curses
        cmd = CommandProcessor(self.event, self.net)
        self.screen = Screen(stdscr, cmd)   # create Screen object
        stdscr.refresh()
        curses_handler = CursesHandler(self.screen)
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        curses_handler.setFormatter(formatter)
        logger.addHandler(curses_handler)

        self.set_uncaught_exc_handler()

    def tick(self, event, data):
        c = self.clientinfo
        gamemode = ""
        gm = c.game_info.gamemode
        if gm == GM_CREATIVE:
            gamemode = "Creative"
        elif gm == GM_SURVIVAL:
            gamemode = "Survival"
        elif gm == GM_ADVENTURE:
            gamemode = "Adventure"
        elif gm == GM_SPECTATOR:
            gamemode = "Spectator"
        pos = "({:.2f}, {:.2f}, {:.2f})".format(c.position.x, c.position.y, c.position.z)
        self.screen.statusText = "%s Mode:%s Pos:%s Health:%s Food:%s" % (c.name, gamemode, pos, c.health.health, c.health.food)
        self.screen.do_read()

    def kill(self, event, data):
        self.screen.close()

    # try exiting curses and restore console before printing stack and crashing
    def set_uncaught_exc_handler(self):
        """ Call this function to setup the `sys.excepthook` to exit curses and
        restore the terminal before printing the exception stack trace. This
        way your application does not mess up the users terminal if it crashes.
        (And you can use assertions for debugging, etc...)"""
        def handle(exec_type, exec_value, exec_traceback):
            try:
                self.screen.close()
            except Exception:
                pass
            sys.__excepthook__(exec_type, exec_value, exec_traceback)
        sys.excepthook = handle
