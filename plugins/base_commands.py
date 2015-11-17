"""
Handful of useful commands
CursesCommand or ChatCommand need to be loaded for this plugin to do anything
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import datetime

import logging
from spockbot.plugins.base import PluginBase
from spockbot.vector import Vector3
import json
logger = logging.getLogger('spockbot')


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
        'cmd_tpa': 'handle_tpa',
        'cmd_tpaccept': 'handle_tpaccept',
    }

    def __init__(self, ploader, settings):
        super(BaseCommandsPlugin, self).__init__(ploader, settings)
        self.tpa_reqs = {}

    def handle_tpa(self, event, data):
        try:
            args = data['args']
            self.tpa_reqs[args[0]] = data['name']
            self.net.push_packet('PLAY>Chat Message', {'message': '/tell ' + ''.join(args[0]) + ' would like to tpa to you, type (!)tpaccept or (!)tpdeny'})
        except IndexError:
            self.net.push_packet('PLAY>Chat Message', {'message': '/tell ' + ''.join(data['name']) + ' Usage: (!)tpa [name]'})
    def handle_tpaccept(self, event, data):
        to_who = data['name']
        try:
            from_who = self.tpa_reqs[to_who]
            self.net.push_packet('PLAY>Chat Message', {'message': '/tp ' + from_who + ' ' + to_who})
            logger.debug(json.dumps(self.tpa_reqs))
            del self.tpa_reqs[to_who] #clear the table.
        except:
            self.net.push_packet('PLAY>Chat Message', {'message': '/tell ' + to_who + ' you have no pending tpa requests.'})
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
        self.interact.place_block(Vector3(*map(int, args)))

    def handle_click(self, event, data):
        args = data['args']
        self.interact.click_block(Vector3(*map(int, args)))

    def handle_break(self, event, data):
        args = data['args']
        self.interact.dig_block(Vector3(*map(int, args)))
