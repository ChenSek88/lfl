#!/usr/bin/env python3
import telebot
from telebot import types
from config import config


TOKEN = config.get('TOKEN', 'token')
bot = telebot.TeleBot(TOKEN)
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Расписание')
users = ['78623899']


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Привет! Выбери необходимое действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
	#if message.from_user.id in users:
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


bot.polling()