"""
Follow a simple plugin for giving commands for following a
player or walking to a location
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

import logging

from spockbot.mcdata.constants import PLAYER_HEIGHT
from spockbot.plugins.base import PluginBase
from spockbot.vector import Vector3

logger = logging.getLogger('spockbot')


class FollowPlugin(PluginBase):
    requires = ('ClientInfo', 'Entities', 'Movement', 'Interact')
    events = {
        'client_tick': 'client_tick',
        'cmd_follow': 'handle_follow',
        'cmd_unfollow': 'handle_unfollow',
        'PLAY<Spawn Player': 'handle_spawn_player',

    }

    def __init__(self, ploader, settings):
        super(FollowPlugin, self).__init__(ploader, settings)
        self.follow_ent = None
        for e in ('PLAY<Entity Relative Move',
                  'PLAY<Entity Look And Relative Move',
                  'PLAY<Entity Teleport',):
            ploader.reg_event_handler(e, self.handle_on_entity_move)

    def handle_spawn_player(self, name, packet):
        name = "Unknown"
        if packet.data['uuid'] in self.clientinfo.player_list:
            name = self.clientinfo.player_list[packet.data['uuid']].name
        logger.info("Spawn Player: %s %s", packet.data['eid'], name)

    def handle_tp(self, event, data):
        args = data['args']
        self.movement.move_to(int(args[0]), 0, int(args[1]))

    def handle_follow(self, event, data):
        args = data['args']
        for uuid, player in self.clientinfo.player_list.items():
            if args[0].lower() in player.name.lower():
                for ent_id, ent in self.entities.players.items():
                    if ent.uuid == uuid:
                        self.follow_ent = ent_id
                        logger.debug("Following: %s", player.name)

    def handle_unfollow(self, event, data):
        self.follow_ent = None
        self.movement.move_location = None

    def handle_on_entity_move(self, name, packet):
        eid = packet.data['eid']
        entity = self.entities.entities[eid]
        if eid in self.entities.players:
            entity_pos = Vector3(entity).iadd((0, PLAYER_HEIGHT, 0))
            if eid == self.follow_ent:
                self.interact.look_at(entity_pos)

    def client_tick(self, name, data):
        if self.follow_ent is not None:
            if self.follow_ent in self.entities.players:
                ent = self.entities.players[self.follow_ent]
                self.movement.move_to(round(ent.x), round(ent.y), round(ent.z))
            else:
                self.follow_ent = None
                self.movement.move_location = None
