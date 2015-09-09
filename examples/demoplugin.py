"""
Sample plugin
"""

import logging

from spock.plugins.base import PluginBase

logger = logging.getLogger('spock')


class DemoPlugin(PluginBase):
    events = {
        'LOGIN<Login Success': 'print_packets',
        'PLAY<Chat Message': 'print_packets',
        'PLAY<Player List Item': 'print_packets'
    }

    def __init__(self, ploader, settings):
        # Used to init the PluginBase
        super(DemoPlugin, self).__init__(ploader, settings)

    def print_packets(self, name, packet):
        logger.info(name, str(packet))
