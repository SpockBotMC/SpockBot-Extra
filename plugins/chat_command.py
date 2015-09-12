"""
Commands can be sent to spock in the format !command args from ingame chat
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import logging

from spock.plugins.base import PluginBase

logger = logging.getLogger('spock')


class ChatCommandPlugin(PluginBase):
    requires = ('Event', 'Chat')
    events = {
        'chat_message': 'handle_chat_message',
    }

    def __init__(self, ploader, settings):
        super(ChatCommandPlugin, self).__init__(ploader, settings)

    def handle_chat_message(self, event, data):
        message = data['message']
        try:
            name_pos = message.find(' ')
            if name_pos == -1:
                player_name = '???'
            else:
                player_name = ' '.join(message[:name_pos].split(' '))
            message = message[name_pos+1:]
            command = message[message.index('!'):]
            args = []
            spacepos = command.find(' ')
            if spacepos == -1:  # no arguments
                command = command[1:]
            else:  # have arguments
                args = command[spacepos+1:].split(' ')
                command = command[1:spacepos]
            self.command_handle(player_name, command.strip(), args)
        except ValueError:  # not a command so just move along
            pass

    def command_handle(self, player_name, command, args):
        logger.info("Command: %s Args: %s", command, args)
        if command == '':
            return
        self.event.emit('cmd_' + command, {'name': player_name, 'args': args})
