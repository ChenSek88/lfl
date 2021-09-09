#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from config import config


TOKEN = config.get('TOKEN', 'chensek_token')
chat_id = "-1001361360883"

api_url = 'https://api.telegram.org/bot'
kdk_url = "https://lfl.ru/sever/kdk"

headers = {}
payload = {}


def send_message_url(message):
	return api_url + TOKEN + '/sendMessage?chat_id=' + chat_id + '&text=' + message


def send_message(message):
	response = requests.request("GET", send_message_url(message))


def get_kdk_date():
	kdk_table = requests.request("GET", kdk_url, headers=headers, data=payload, timeout=60)
	soup = BeautifulSoup(kdk_table.text, 'lxml')
	kdk_date = soup.find_all(attrs={"class":"date"})
	for i in kdk_date:
		date = i.get_text().split('.')
		f_date = (date[2] + '.' + date[1] + '.' +date[0])
		if f_date >= '2021.09.09':
			send_message('New kdk decision! See https://lfl.ru/sever/kdk')


get_kdk_date()

