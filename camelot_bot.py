#!/usr/bin/env python3
from datetime import datetime
import requests
from config import config
import hashlib
import random
import json


TOKEN = config.get('TOKEN', 'camelot_token')


api_url = 'https://api.telegram.org/bot'
#chat_name = '@camelot_test'
chat_id = '-1001190912505'
#test_chat_id = '-1001361360883'
message_id = ''


schedule = {}
statuses = {}
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
greetings2 = ['Мужчины!', 'Парни!', 'Рыцари!', 'Пацаны!', 'Машины!']
greetings3 = ['Але!', 'Про игру не забыл?', 'На игру собрался?', 'Пссс, парень!', 'Махаться будешь?']


def pin_url(message_id):
	return api_url + TOKEN + '/pinChatMessage?chat_id=' + chat_id + '&message_id=' + str(message_id)


def pin_message(message_id):
	response = requests.request("GET", pin_url(message_id))


def unpin_all_messages():
	response = requests.request("GET", api_url + TOKEN + '/unpinChatMessage?chat_id=' + chat_id)


def send_message_url(message):
	return api_url + TOKEN + '/sendMessage?chat_id=' + chat_id + '&text=' + message


def send_message(message):
	global message_id
	response = requests.request("GET", send_message_url(message))
	result = json.loads(response.text)
	message_id = result['result']['message_id']


def do_send_message(hash, game, state):
	if state == 1:
		send_message('Внимание! Новая игра: \n%s' % game)
	elif state == 2:
		send_message('%s Завтра игра: \n%s' % (random.choice(greetings2), game))
	elif state == 3:
		send_message('%s Игра через %s\n%s' % (random.choice(greetings3), time_left, game))
	open("statuses.txt", "a+").write("%s\t%s\n" % (hash, state))


with open("schedule.txt") as sch:
	for s in sch:
		hash  = hashlib.md5(s.encode('utf-8')).hexdigest()
		schedule[hash] = s.strip().split('\t')


with open("statuses.txt") as st:
	for s in st:
		hash, state =  s.strip().split('\t')
		statuses[hash] = state


for hash, sch in schedule.items():
	index = datetime.strptime(sch[1], "%d.%m.%Y %H:%M").weekday()
	weekday = days_of_week[index]
	game = sch[0] + '\n' + weekday + ' ' + sch[1] + '\n' + sch[2]
	minutes_left = (datetime.strptime(sch[1], "%d.%m.%Y %H:%M") - datetime.now()).total_seconds()/60 - 180
	hours, minutes = divmod(minutes_left, 60)
	time_left = "%02dч %02dмин"% (hours, minutes)
	if not hash in statuses or statuses[hash] == '0':
		do_send_message(hash, game, 1)
	elif statuses[hash] == '1' and minutes_left <= 1440:
		#unpin_all_messages()
		do_send_message(hash, game, 2)
		pin_message(message_id)
	elif statuses[hash] == '2' and minutes_left <= 180:
		#unpin_all_messages()
		do_send_message(hash, game, 3)
		pin_message(message_id)


print('The work is completed' + '	' +  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
