"""
Offline connection demo
"""

from demoplugin import DemoPlugin

from spock import Client
from spock.plugins import default_plugins

settings = {
    'start': {
        'username': 'Bot',
    },
    'auth': {
        'authenticated': False,
    },
}

plugins = default_plugins
plugins.append(('demo', DemoPlugin))
client = Client(plugins=plugins, settings=settings)
# client.start() with no arguments will automatically connect to localhost
client.start('localhost', 25565)
