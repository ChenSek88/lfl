#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import telebot
#from telebot import types
from datetime import datetime
import requests
from config import config


TOKEN = config.get('TOKEN', 'token')

#bot = telebot.TeleBot(TOKEN)
#keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#keyboard.row('Расписание')

users = [78623899]
url = 'https://api.telegram.org/bot'
chat_name = '@camelot_test'
#chat_id = '-1001241312381'
test_chat_id = '-1001308984669'

message = 'Внимание! До игры %s \n' % time_left()

game = open('schedule.txt').read()


def time_left():
	date = open('schedule.txt').readlines()[1].strip() + ':00'
	now = datetime.now()
	strp_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
	diff = ((strp_date - now).total_seconds())/60
	hours, minutes = divmod(diff, 60)
	if hours > 24:
		days, hours = divmod(hours, 24)
		return("%02dд %02dч %02dмин"% (days, hours, minutes))
	else:
		return("%02dч %02dмин"% (hours, minutes))


def request_url():
	return url + TOKEN + '/sendMessage?chat_id=' + test_chat_id + '&text=' + message + game


def send_message():
	response = requests.request("GET", request_url())
	assert response.status_code == 200


send_message()


'''@bot.message_handler(commands=['start'])
def start(message):
	if message.from_user.id in users:
		bot.send_message(message.chat.id, 'Привет! Выбери необходимое действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.from_user.id in users:
		if message.text.lower() == 'привет':
			bot.send_message(message.chat.id, 'Привет')
		elif message.text.lower() == 'как дела?':
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDGV8_yLbpXxAEhPKKxrHMjDRX-pK9AAKgAAP3AsgPw0cdAaCbwBobBA')
		elif message.text.lower() == 'пока':
			bot.send_message(message.chat.id, 'Пока!')
		elif message.text.lower() == 'расписание':
			bot.send_message(message.chat.id, open('schedule.txt').read())
		else:
			bot.send_message(message.chat.id, 'Фигню написал, попробуй еще раз.')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
	print(message)

@bot.message_handler(commands=['start'])
def send_text(message):
	if message.chat.id in chat:
		bot.send_message(message.chat.id, open('schedule.txt').read())


bot.polling()'''

