"""
Handful of useful commands
CursesCommand or ChatCommand need to be loaded for this plugin to do anything
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import datetime

from spock.plugins.base import PluginBase
from spock.vector import Vector3


class BaseCommandsPlugin(PluginBase):
    requires = ('Net', 'Physics', 'Interact', 'Inventory')
    events = {
        'cmd_jump': 'handle_jump',
        'cmd_say': 'handle_say',
        'cmd_date': 'handle_date',
        'cmd_command': 'handle_command',
        'cmd_hold': 'handle_hold',
        'cmd_place': 'handle_place',
        'cmd_break': 'handle_break',
        'cmd_click': 'handle_click',
    }

    def __init__(self, ploader, settings):
        super(BaseCommandsPlugin, self).__init__(ploader, settings)

    def handle_jump(self, event, data):
        self.physics.jump()

    def handle_say(self, event, data):
        self.interact.chat(' '.join(data['args']))

    def handle_date(self, event, data):
        self.net.push_packet('PLAY>Chat Message',
                             {'message': 'Current Date: ' +
                              str(datetime.datetime.now())})

    def handle_command(self, event, data):
        self.net.push_packet('PLAY>Chat Message',
                             {'message': '/' + ' '.join(data['args'])})

    def handle_hold(self, event, data):
        args = data['args']
        slot = self.inventory.find_slot(int(args[0]),
                                        self.inventory.window.hotbar_slots)
        if slot is not None:
            self.inventory.select_active_slot(slot)

    def handle_place(self, event, data):
        args = data['args']
        self.interact.place_block(Vector3(int(args[0]),
                                          int(args[1]),
                                          int(args[2])))

    def handle_click(self, event, data):
        args = data['args']
        self.interact.click_block(Vector3(int(args[0]),
                                          int(args[1]),
                                          int(args[2])))

    def handle_break(self, event, data):
        args = data['args']
        self.interact.dig_block(Vector3(int(args[0]),
                                        int(args[1]),
                                        int(args[2])))
