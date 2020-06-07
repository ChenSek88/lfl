#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
from jinja2 import Template
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import shutil

tournament_stats_url = "http://lfl.ru/?ajax=1&method=tournament_stats_table&tournament_id=5098&club_id=2356&season_id=39"
tournament_calendar_url= "http://lfl.ru/?ajax=1&method=tournament_calendar_table&tournament_id=0&club_id=2356&season_id=39"
tournament_results_url = "http://lfl.ru/?ajax=1&method=tournament_resault_table&tournament_id=0&club_id=2356&season_id=39"
players_stats_url = "http://lfl.ru/?ajax=1&method=tournament_squads_table&tournament_id=5098&club_id=2356&season_id=39"

up = ['pos_1', 'pos_2']
up2 = ['pos_3', 'pos_4']
down = ['pos_15', 'pos_16', 'pos_17', 'pos_18']
down2 = ['pos_19', 'pos_20']

payload  = {}
headers = {}


def get_table(file, url):
	with open(file, 'w') as f:
		stats_table = requests.request("GET", url, headers=headers, data = payload)
		f.write(stats_table.text)


os.mkdir('temp_tables')
get_table('temp_tables/tournament_table', tournament_stats_url)
get_table('temp_tables/calendar_table', tournament_calendar_url)
get_table('temp_tables/results_table', tournament_results_url)
get_table('temp_tables/players_table', players_stats_url)


with open('temp_tables/tournament_table') as table:
	tournament_table = BeautifulSoup(table, 'lxml').find('tbody')
	images = tournament_table.find_all('img')
	for img in images:
		del img['align']
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]
		
	href = tournament_table.find_all('a')
	for i in href:
		i['href'] = 'http://lfl.ru' + i['href']
		i['target'] = '_blank'
		i['class'] = 'text-body'
	
	td = tournament_table.find_all('td')
	for i in td:
		i['class'] = 'text-center'


	pos = 1
	tr = tournament_table.find_all('tr')
	for i in tr:
		td = i.find_all('td')[1]
		td.extract()
		td = i.find_all('td')[1]
		td['class'] = 'text-left'
		
	for i in tr:
		del i['class']
		i['class'] = 'pos_' + str(pos)
		pos = pos + 1
		if i['class'] in up:
			i['class'] = 'table-success'
		elif i['class'] in up2:
			i['class'] = 'table-warning'
		elif i['class'] in down:
			i['class'] = 'table-danger'
		elif i['class'] in down2:
			i['class'] = 'bg-danger'
		else:
			i['class'] = 'table-light'


with open('temp_tables/calendar_table') as table:
	calendar_table = BeautifulSoup(table, 'lxml').find('tbody')

	tr = calendar_table.find_all('tr')
	for i in tr:
		i['class'] = 'table-light'

	images = calendar_table.find_all('img')
	for img in images:
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]

	href = calendar_table.find_all('a')
	for i in href:
		i['href'] = 'http://lfl.ru' + i['href']
		i['class'] = 'text-body'
		i['target'] = '_blank'

	td = calendar_table.find_all('td')
	for i in td:
		del i['class']
		del i['style']
		del i['width']


with open('temp_tables/players_table') as table:
	players_table = BeautifulSoup(table, 'lxml').find('tbody')

	tr = players_table.find_all('tr')
	for i in tr:
		i['class'] = 'table-light'


	href = players_table.find_all('a')
	for i in href:
		i['href'] = 'http://lfl.ru' + i['href']
		i['class'] = 'text-body'
		i['target'] = '_blank'
		
	images = players_table.find_all('img')
	for img in images:
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]
		img['class'] = (img['class'] + ['pr-1'])

	td = players_table.find_all('td')
	for i in td:
		span = i.find_all('span')
		for s in span:
			s.extract()


html = open('template.html').read()
template = Template(html)

#tournament = open('temp_tables/tournament_table').read()
#calendar = open('temp_tables/calendar_table').read()
#results = open('temp_tables/results_table').read()
#players = open('temp_tables/players_table').read()



with open("index.html", "w") as index:
	index.write(template.render(tournament_table=tournament_table, calendar_table=calendar_table,
		players_table=players_table))

shutil.rmtree('temp_tables')