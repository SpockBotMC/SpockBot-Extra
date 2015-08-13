"""
Basic demo example
"""

from spock import Client
from spock.plugins import DefaultPlugins

#bad
import sys; import os
sys.path.insert(0, os.path.abspath('..'))
from plugins.EchoPacket import EchoPacketPlugin

start_settings = {
    'username': 'your_username',
    'password': 'your_password',
}

plugins = DefaultPlugins
plugins.append(('echo', EchoPacketPlugin))
client = Client(plugins = plugins, start = start_settings)
#client.start() with no arguments will automatically connect to localhost
client.start('localhost', 25565)
