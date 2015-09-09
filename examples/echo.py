"""
Basic demo example
"""

import os
import sys

from spock import Client
from spock.plugins import default_plugins

# Bad but needed to import extra plugins from examples
sys.path.insert(0, os.path.abspath('..'))
from plugins.EchoPacket import EchoPacketPlugin

start_settings = {
    'username': 'your_username',
    'password': 'your_password',
}

plugins = default_plugins
plugins.append(('echo', EchoPacketPlugin))
client = Client(plugins=plugins, start=start_settings)
# client.start() with no arguments will automatically connect to localhost
client.start('localhost', 25565)
