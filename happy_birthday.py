#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from config import config
import datetime


HOME_DIR = config.get('home_dir', 'path')
TOKEN = config.get('TOKEN', 'token')
chat_id = "-1001190912505"
#test_chat_id = "-1001361360883"

api_url = "https://api.telegram.org/bot"


today = datetime.date.today()
day, month = today.day, today.month
now = "%02d.%02d" % (day, month)
message = 'Принимай поздравления от команды!'


def send_message_url(message):
	return api_url + TOKEN + '/sendMessage?chat_id=' + chat_id + '&text=' + message


def send_message(message):
	requests.request("GET", send_message_url(message))


def get_players_bd():
	with open(HOME_DIR + 'players_bd.txt') as players_bd:
		players_bd_dict = {}
		for player in players_bd:
			name = player.split(',')[0]
			b_date = player.split(',')[1]
			players_bd_dict.update({name: b_date.rstrip()})
		return players_bd_dict


def happy_birthday(message):
	for player in get_players:
		if get_players[player] == now:
			send_message('Сегодня день рождения празднует %s! %s' % (player, message))


get_players = get_players_bd()
happy_birthday(message)