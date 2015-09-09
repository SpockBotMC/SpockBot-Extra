"""
Just send the animation packet every 5min
"""
__author__ = "Nick Gamberini, Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

from spock.plugins.base import PluginBase

AFK_TIME = 5


class AntiAFKPlugin(PluginBase):
    requires = ('Net', 'Physics', 'Timers')

    def __init__(self, ploader, settings):
        super(AntiAFKPlugin, self).__init__(ploader, settings)
        self.timers.reg_event_timer(AFK_TIME*60, self.avoid_afk)

    def avoid_afk(self):
        self.physics.jump()
        self.net.push_packet('PLAY>Animation', '')
