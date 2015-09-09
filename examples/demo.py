"""
Basic demo example
"""

from demoplugin import DemoPlugin

from spock import Client
from spock.plugins import default_plugins

start_settings = {
    'username': 'your_username',
    'password': 'your_password',
}

plugins = default_plugins
plugins.append(('demo', DemoPlugin))
client = Client(plugins=plugins, start=start_settings)
# client.start() with no arguments will automatically connect to localhost
client.start('localhost', 25565)
