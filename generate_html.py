#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from jinja2 import Template
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
	soup = BeautifulSoup(table, 'lxml')
	tournament_table = soup.find('tbody')
	images = tournament_table.find_all('img')
	for img in images:
		del img['align']
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]

	a = tournament_table.find_all('a')
	for i in a:
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
		td['class'] = 'team text-left'	
		del i['class']
		i['class'] = 'pos_' + str(pos)
		pos += 1
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
	soup = BeautifulSoup(table, 'lxml')
	calendar_table = soup.find('tbody')
	images = calendar_table.find_all('img')
	for img in images:
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]

	a = calendar_table.find_all('a')
	for i in a:
		i['href'] = 'http://lfl.ru' + i['href']
		i['class'] = 'text-body'
		i['target'] = '_blank'

	td = calendar_table.find_all('td')
	for i in td:
		i['class'] = 'align-middle'
		del i['style']
		del i['width']

	tr = calendar_table.find_all('tr')
	tour_list = ""
	for i in tr:
		tour = i.find_all('td')[0]
		owners = i.find_all('td')[3]
		new_tag = soup.new_tag('br')
		date = i.find_all('td')[4]
		date.append(i.find_all('td')[1].get_text())
		date.insert(4, new_tag)
		date.append(i.find_all('td')[7].get_text() + ', ' + i.find_all('td')[2].get_text())
		guests = i.find_all('td')[5]
		tour_list += """<tr class="table-light text-center">%s %s %s %s</tr>""" % (tour, owners, date, guests)	


with open('temp_tables/players_table') as table:
	soup = BeautifulSoup(table, 'lxml')
	players_table = soup.find('tbody')

	tr = players_table.find_all('tr')
	for i in tr:
		i['class'] = 'table-light'
		del i['data-division-id']
		del i['data-tournament-id']

	tour_header = players_table.find_all(attrs={"class":"tour-header"})
	for i in tour_header:
		i['class'] = 'amplua text-center font-weight-bold'

	a = players_table.find_all('a')
	for i in a:
		i['href'] = 'http://lfl.ru' + i['href']
		i['class'] = 'text-body'
		i['target'] = '_blank'
	
	images = players_table.find_all('img')
	for img in images:
		img['src'] = ('http://lfl.ru' + img['src']).split('?')[0]
		img['class'] = (img['class'] + ['pr-1'])
		del img['align']

	td = players_table.find_all('td')
	for i in td:
		if not i.has_attr('class'):
			i['class'] = 'text-center align-middle'
		span = i.find_all('span')
		for s in span:
			s.extract()	

html = open('template.html').read()
template = Template(html)


with open("index.html", "w") as index:
	index.write(template.render(tournament_table=tournament_table, calendar_table=tour_list,
		players_table=players_table))

shutil.rmtree('temp_tables')