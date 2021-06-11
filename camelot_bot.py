#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import telebot
#from telebot import types
from datetime import datetime
import requests
from config import config
import hashlib


TOKEN = config.get('TOKEN', 'token')
greeting = []

#bot = telebot.TeleBot(TOKEN)
#keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#keyboard.row('Расписание')


url = 'https://api.telegram.org/bot'
chat_name = '@camelot_test'
#chat_id = '-1001241312381'
test_chat_id = '-1001308984669'

game = open('schedule.txt').read()

temp_list = []

with open('hash_list.txt') as hash_list:
	for h in hash_list:
		temp_list.append(h.strip())




def time_left():
	date = open('schedule.txt').readlines()[1].strip() + ':00'
	now = datetime.now()
	strp_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
	diff = ((strp_date - now).total_seconds())/60
	hours, minutes = divmod(diff, 60)
	if hours > 24:
		days, hours = divmod(hours, 24)
		return("%02dд %02dч %02dмин"% (days, hours, minutes))
		#print("%02dд %02dч %02dмин"% (days, hours, minutes))
	else:
		return("%02dч %02dмин"% (hours, minutes))
		#print("%02dч %02dмин"% (hours, minutes))


def request_url(message):
	return url + TOKEN + '/sendMessage?chat_id=' + test_chat_id + '&text=' + message


def send_message(message):
	response = requests.request("GET", request_url(message))
	assert response.status_code == 200


first_message = 'Внимание! Новая игра: \n%s' % game
#second_message = 'Внимание!! Игра завтра %s \n%s' % (time_left(), game)
#third_message = 'Внимание!!! До игры %s \n%s' % (time_left(), game)

result = hashlib.md5(first_message.encode('utf-8')).hexdigest()


with open('hash_list.txt', 'a') as hash_list:
	if result in temp_list:
		print('Сообщение было отправлено')
	else:
		send_message(first_message)
		hash_list.write("\n" + result)


#print(result)




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

