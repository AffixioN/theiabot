import socket
import threading
import urllib2


irc_host = 'deadtheia'
irc_name = 'theiabot'
irc_server = 'irc.twitch.tv'
irc_oath = 'enter_oath_here'


bot_antispam = 0
bot_mods = ''
bot_modlist = []


irc_irc = socket.socket()
irc_irc.connect((irc_server, 6667))
irc_irc.send('PASS ' + irc_oath + '\r\n')
irc_irc.send('USER ' + irc_name + ' 0 * :' + irc_host + '\r\n')
irc_irc.send('NICK ' + irc_name + '\r\n')
irc_irc.send('JOIN #' + irc_host + '\r\n')


def client_message(client_message_reply):
	global bot_antispam
	bot_antispam += 1
	if(bot_antispam < 5):
		irc_irc.send('PRIVMSG #' + irc_host + ' :' + client_message_reply + '\r\n')
	else:
		print('error(bot_antispam) overload')


def client_antispam():
	global bot_antispam
	bot_antispam = 0
	threading.Timer(10, client_antispam).start()


client_enabled = True
client_fetchMods = False
client_antispam()
client_message('Theiabot has entered the channel')


chat_data = ""
chat_message = ""
chat_user = ""
chat_line = ""
chat_command = ""
chat_reply = ""
chat_number = ""


while(client_enabled == True):
	try:
		chat_data = irc_irc.recv(1024)
		try:
			chat_message = chat_data.split('#' + irc_host + ' :')[1]
		except:
			print('Can not find message')
		try:
			chat_user = chat_data.split(':')[1]
			chat_user = chat_user.split('!')[0]
		except:
			print('Can not find user')
		try:
			chat_line = chat_user + ': ' + chat_message
		except:
			print('Can not make chat_data into chat_line')

		#print(chat_data)
		print(chat_line)

		try:
			bot_mods = chat_data.split('The moderators of this room are: ')[1]
			bot_modlist = bot_mods.split(', ')
			bot_modlist[len(bot_modlist) - 1] = bot_modlist[len(bot_modlist) - 1][:-2]
			print(bot_modlist)
		except:
			print('')

		if(client_fetchMods == False):
			client_message("/mods")
			client_fetchMods = True

		if(chat_message.find('!mod_refresh') != -1):
			client_fetchMods = False

		if(chat_message.find('!') != -1):
			with open('commands.txt') as f:
				lines_command = f.readlines()
				lines_command = [line.strip() for line in open('commands.txt')]
				f.close()
			#print(lines_command)
			with open('replies.txt') as f:
				lines_replies = f.readlines()
				lines_replies = [line.strip() for line in open('replies.txt')]
				f.close()
			#print(lines_replies)

			chat_command = chat_message.split("!")[1]
			chat_command = chat_command[:-2]
			print(chat_command)

			if(chat_command in lines_command):
				print("Found command")
				chat_number = lines_command.index(chat_command)
				reply = lines_replies[chat_number]
				client_message(reply)

		if(chat_message.find('!commands') != -1):
			with open('commands.txt') as f:
				lines_command = f.readlines()
				lines_command = [line.strip() for line in open('commands.txt')]
				f.close()

			commands = ', !'.join(lines_command)
			dong = "The current commands are: !uptime, !" + commands
			client_message(dong)

		if(chat_message.find('!uptime') != -1):
			dong = urllib2.urlopen("https://www.nightdev.com/hosted/uptime.php?channel=" + irc_host)
			dongs = dong.read()
			client_message(dongs)

		if(chat_message.find('!addcmd') != -1):
			#print("here")
			if(chat_user in bot_modlist):
				#print("herer")
				with open('commands.txt') as f:
					lines_command = f.readlines()
					f.close()
			#print(lines_command)
				with open('replies.txt') as f:
					lines_replies = f.readlines()
					f.close()
			#print(lines_replies)
				command = chat_message.split('!addcmd ')[1]
				#print(command)
				command = command.split(' ')[0]
				#print("here")
				reply = chat_message.split('!addcmd ' + command + " ")[1]
				reply = reply.split('\n')[0]
				#print(reply)
				reply = reply[:-1]
				#print("herer")
				lines_replies.append(reply + "\n")
				lines_command.append(command + "\n")
				#print(lines_replies)
				#print(lines_command)
				with open('commands.txt', 'a') as f:
					f.write(command + '\n')
					f.close()
				with open('replies.txt', 'a') as f:
					f.write(reply + '\n')
					f.close()
				client_message("Command Added")

		if(chat_message.find('!age') != -1):
			client_message("Sorry " + chat_user + " my age is not available at this moment, please leave a message after the beep")


	except:
		irc_irc = socket.socket()
		irc_irc.connect((irc_server, 6667))
		irc_irc.send('PASS ' + irc_oath + '\r\n')
		irc_irc.send('USER ' + irc_name + ' 0 * :' + irc_host + '\r\n')
		irc_irc.send('NICK ' + irc_name + '\r\n')
		irc_irc.send('JOIN #' + irc_host + '\r\n')

