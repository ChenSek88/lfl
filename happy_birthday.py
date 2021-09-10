#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from config import config
import datetime


TOKEN = config.get('TOKEN', 'camelot_token')
chat_id = "-1001190912505"
#test_chat_id = "-1001361360883"

api_url = "https://api.telegram.org/bot"
#kdk_url = "https://lfl.ru/sever/kdk"
players_url = "https://lfl.ru/club2356/players_list"

headers = {}

today = datetime.date.today()
day, month = today.day, today.month
now = "%02d.%02d" % (day, month)
message = 'С днем рождения тебя, укротитель футбольного мяча. Желаю счастья, любви и достатка в личной жизни, а также ярких матчей на поле с победой, но без травм, с громким криком преданных болельщиков и поддержкой всех близких людей. Достигай успеха во всем, двигайся только вперед и пусть счет в любом деле всегда будет только в твою пользу.'


def send_message_url(message):
	return api_url + TOKEN + '/sendMessage?chat_id=' + chat_id + '&text=' + message


def send_message(message):
	response = requests.request("GET", send_message_url(message))


def get_players():
	with open('/home/ts/Documents/players.txt', 'w') as players:
		table = requests.request("GET", players_url, headers=headers, timeout=60)
		table.encoding = table.apparent_encoding
		players.write(table.text)
		

def get_players_bd():
	with open('/home/ts/Documents/players.txt', 'r') as players_bd:
		soup = BeautifulSoup(players_bd, 'lxml')
		players = soup.find_all(attrs={"class": "player_title"})
		players_dict = {}
		for player in players:
			name = player.select('.player_title > p')[0].get_text()
			b_date = player.select('.player_title > p')[4].get_text().split(':')[1].strip().split('.')
			bd = b_date[0] + '.' + b_date[1]
			players_dict.update({name: bd})
		return players_dict


get_players = get_players_bd()


def happy_birthday(message):
	for player in get_players:
		print(get_players[player])
		if get_players[player] == now:
			send_message('Сегодня день рождения празднует %s! %s' % (player, message)) 


happy_birthday(message)


'''def get_kdk_date():
	kdk_table = requests.request("GET", kdk_url, headers=headers, timeout=60)
	soup = BeautifulSoup(kdk_table.text, 'lxml')
	kdk_date = soup.find_all(attrs={"class":"date"})
	for i in kdk_date:
		date = i.get_text().split('.')
		f_date = (date[2] + '.' + date[1] + '.' +date[0])
		if f_date >= '2021.09.09':
			send_message('New kdk decision! See https://lfl.ru/sever/kdk')'''