"""
Offline connection demo
"""

from spock import Client
from spock.plugins import DefaultPlugins
from demoplugin import DemoPlugin

start_settings = {
    'username': 'a_username',
    'authenticated': False,
}

plugins = DefaultPlugins
plugins.append(DemoPlugin)
client = Client(plugins = plugins, settings = start_settings)
#client.start() with no arguments will automatically connect to localhost
client.start('localhost', 25565)
