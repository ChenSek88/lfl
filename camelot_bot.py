#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types


TOKEN = '1398876177:AAGgwj9haR0umKX5qffGrQMep1wFssNRtNk'
bot = telebot.TeleBot(TOKEN)
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Расписание', 'Таблица')


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Привет! Выбери необходимое действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'привет':
		bot.send_message(message.chat.id, 'Привет')
	elif message.text.lower() == 'как дела?':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDGV8_yLbpXxAEhPKKxrHMjDRX-pK9AAKgAAP3AsgPw0cdAaCbwBobBA')
	elif message.text.lower() == 'пока':
		bot.send_message(message.chat.id, 'Пока!')
	elif message.text.lower() == 'расписание':
		bot.send_message(message.chat.id, 'Водник – Камелот\n22.08.2020(сб) Новый Стадион Север, 15:40')
	elif message.text.lower() == 'таблица':
		bot.send_message(message.chat.id, 'Понадобится немного времени')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
	print(message)


bot.polling()