"""
Commands can be sent to spock in the format !command args from ingame chat
"""
__author__ = "Morgan Creekmore"
__copyright__ = "Copyright 2015, The SpockBot Project"
__license__ = "MIT"

from spock.utils import string_types

class ChatCommandPlugin:
	def __init__(self, ploader, settings):
		self.event = ploader.requires('Event')
		ploader.reg_event_handler(
			'PLAY<Chat Message', self.handle_chat_message
		)

	def handle_chat_message(self, name, packet):
		chat_data = packet.data['json_data']
		message = self.parse_chat(chat_data)
		print('Chat:', message)
		try:
			name_pos = message.find(' ')
			if name_pos == -1:
				player_name='???'
			else:
				player_name=' '.join(message[:name_pos].split(' '))
			message=message[name_pos+1:]
			command = message[message.index('!'):]
			args = []
			spacepos = command.find(' ')
			if spacepos == -1: #no arguments
				command = command[1:]
			else: #have arguments
				args = command[spacepos+1:].split(' ')
				command = command[1:spacepos]
			self.command_handle(player_name, command.strip(), args)
		except ValueError: #not a command so just move along
			pass

	def command_handle(self, player_name, command, args):
		if command == '':
			return
		self.event.emit('cmd_' + command, {name:player_name, args:args})

	def parse_chat(self, chat_data):
		message = ''
		if type(chat_data) is dict:
			if 'text' in chat_data:
				message += chat_data['text']
				if 'extra' in chat_data:
					message += self.parse_chat(chat_data['extra'])
			elif 'translate' in chat_data:
				if 'with' in chat_data:
					message += self.parse_chat(chat_data['with'])
		elif type(chat_data) is list:
			for text in chat_data:
				if type(text) is dict:
					message += self.parse_chat(text)
				elif type(text) is string_types:
					message += ' ' + text		
		return message
