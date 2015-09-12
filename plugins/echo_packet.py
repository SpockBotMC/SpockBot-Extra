"""
A plugin that just echos every packet other than the chunk data
and player position
"""
__author__ = "Nick Gamberini, Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import logging

from spock.mcp.mcdata import hashed_structs

logger = logging.getLogger('spock')

BLACKLIST = ['PLAY<Map Chunk Bulk', 'PLAY<Chunk Data', 'PLAY>Player Position']


class EchoPacketPlugin:
    def __init__(self, ploader, settings):
        for i in list(hashed_structs.keys()):
            ploader.reg_event_handler(i, self.echopacket)

    def echopacket(self, name, packet):
        # Dont print Chunk Data and Map Chunk Bulk
        if packet.str_ident not in BLACKLIST:
            logger.info(str(packet))
