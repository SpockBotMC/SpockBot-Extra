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
    defaults = {
        'prefix': '!',
    }
    events = {
        'chat_text': 'handle_chat_message',
    }

    def __init__(self, ploader, settings):
        super(ChatCommandPlugin, self).__init__(ploader, settings)
        self.prefix = self.settings['prefix']

    def handle_chat_message(self, event, data):
        message = data['message']
        try:
            command = message[message.index(self.prefix):]
            args = []
            spacepos = command.find(' ')
            if spacepos == -1:  # no arguments
                command = command[1:]
            else:  # have arguments
                args = command[spacepos+1:].split(' ')
                command = command[1:spacepos]
            self.command_handle(data['name'], command.strip(), args)
        except ValueError:  # not a command so just move along
            pass

    def command_handle(self, name, command, args):
        logger.info("Command: %s Args: %s", command, args)
        if command == '':
            return
        self.event.emit('cmd_' + command, {'name': name, 'args': args})
