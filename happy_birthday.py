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
message = 'Пусть каждый момент вашей жизни будет наполнен радостью и успехами, а игра на поле приносит только победы и удовлетворение. Пусть ваше мастерство на футбольном поле будет выше небес, а ваша страсть к этому прекрасному виду спорта никогда не угаснет. Желаем вам здоровья, силы, удачи и безграничного вдохновения для достижения новых вершин в футбольной карьере. Пусть каждая игра становится для вас не только испытанием, но и возможностью продемонстрировать ваш талант и профессионализм. Пусть ваши голы радуют болельщиков, а ваши ассисты воодушевляют напарников. С чистым сердцем выходите на поле и дарите нам эмоции, которые надолго запомнятся. С днем рождения! Верьте в себя и свои силы, и успех обязательно будет на вашей стороне!'


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