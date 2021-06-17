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


url = 'https://api.telegram.org/bot'
#chat_name = '@camelot_test'
chat_id = '-1001241312381'
#test_chat_id = '-1001308984669'


schedule = {}
statuses = {}
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def request_url(message):
	return url + TOKEN + '/sendMessage?chat_id=' + chat_id + '&text=' + message


def send_message(message):
	response = requests.request("GET", request_url(message))
	assert response.status_code == 200


def do_send_message(hash, game, state):
	if state == 1:
		send_message('Внимание! Новая игра: \n%s' % game)
	elif state == 2:
		send_message('Внимание!! Завтра игра: \n%s' % game)
	elif state == 3:
		send_message('Внимание!!! Игра через %s\n%s' % (left, game))
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
	time_left = (datetime.strptime(sch[1], "%d.%m.%Y %H:%M") - datetime.now()).total_seconds()/60
	hours, minutes = divmod(time_left, 60)
	left = "%02dч %02dмин"% (hours, minutes)
	if not hash in statuses or statuses[hash] == '0':
		do_send_message(hash, game, 1)
	elif statuses[hash] == '1' and hours <= 24:
		do_send_message(hash, game, 2)
	elif statuses[hash] == '2' and hours <= 3:
		do_send_message(hash, game, 3)
 

'''def make_hash():
	date = open('schedule.txt').readlines()[1].strip() + ':00'
	now = datetime.now()
	strp_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
	diff = ((strp_date - now).total_seconds())/60
	hours, minutes = divmod(diff, 60)
	if hours <= 24:
		print(hashlib.md5(second_message.encode('utf-8')).hexdigest())
		return hashlib.md5(second_message.encode('utf-8')).hexdigest()
		#days, hours = divmod(hours, 24)
		#return("%02dч %02dмин"% (hours, minutes))
	elif hours <= 3:
		print(hashlib.md5(third_message.encode('utf-8')).hexdigest())
		return hashlib.md5(third_message.encode('utf-8')).hexdigest()
		#return("%02dч %02dмин"% (hours, minutes))


with open('hash_list.txt', 'a') as hash_list:
	if make_hash() in temp_list:
		print('Сообщение было отправлено')
	else:
		send_message(second_message) or send_message(third_message)
		hash_list.write("\n" + make_hash())'''


'''bot = telebot.TeleBot(TOKEN)
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Расписание')


@bot.message_handler(commands=['start'])
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