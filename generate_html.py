#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from jinja2 import Template
import os
import shutil

HOME_DIR = '/home/ts/lfl/'
os.mkdir(HOME_DIR + 'temp_tables/')
TEMP_DIR = HOME_DIR + 'temp_tables/'

tournament_stats_url = "http://lfl.ru/?ajax=1&method=tournament_stats_table&tournament_id=5098&club_id=2356&season_id=39"
tournament_calendar_url= "http://lfl.ru/?ajax=1&method=tournament_calendar_table&tournament_id=0&club_id=2356&season_id=39"
tournament_results_url = "http://lfl.ru/?ajax=1&method=tournament_resault_table&tournament_id=0&club_id=2356&season_id=39"
players_stats_url = "http://lfl.ru/?ajax=1&method=tournament_squads_table&tournament_id=5098&club_id=2356&season_id=39"
disqualifications_url= "http://lfl.ru/?ajax=1&mode=new_format&method=tournament_disqualifications_table&tournament_id=5098&club_id=2356&season_id=39"

up = ['pos_1', 'pos_2']
up2 = ['pos_3', 'pos_4']
down = ['pos_15', 'pos_16', 'pos_17', 'pos_18']
down2 = ['pos_19', 'pos_20']

payload  = {}
headers = {}

images_url = 'http://lfl.ru/images-thumbs/100x100/'

def get_table(file, url):
	with open(file, 'w') as f:
		stats_table = requests.request("GET", url, headers=headers, data = payload)
		f.write(stats_table.text)


get_table(TEMP_DIR + 'tournament_table', tournament_stats_url)
get_table(TEMP_DIR + 'calendar_table', tournament_calendar_url)
get_table(TEMP_DIR + 'players_table', players_stats_url)
get_table(TEMP_DIR + 'results_table', tournament_results_url)
get_table(TEMP_DIR + 'disqual_table', disqualifications_url)


with open(TEMP_DIR + 'tournament_table') as table:
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


with open(TEMP_DIR + 'calendar_table') as table:
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
	tour_list = ''
	desktop_class = 'd-sm-none d-md-block d-none'
	tablet_class = 'd-none d-sm-block d-md-none'
	mobile_class = 'col-12 d-block d-sm-none text-center'
	for i in tr:
		tour = i.find_all('td')[0].get_text()
		tour_th = """<th class="col-1 %s">%s</th>""" % (desktop_class, tour)
		owners = i.find_all('td')[3].get_text()
		owners_img = i.find_all('img')[0]['src'].split('16x16/')[1]
		owners_tablet_image = """<td class="col-2 %s text-center"><img class="club-logo-big" src="%s%s"></td>"""%(tablet_class, images_url, owners_img)
		owners_desktop = """<td class="col-3 %s text-right">%s<img class="club-logo" src="%s%s"></td>"""%(desktop_class, owners, images_url, owners_img)
		guests = i.find_all('td')[5].get_text()
		guests_img = i.find_all('img')[1]['src'].split('16x16/')[1]
		guests_tablet_image = """<td class="col-2 %s text-center"><img class="club-logo-big" src="%s%s"><br></td>"""%(tablet_class, images_url, guests_img)
		guests_desktop = """<td class="col-3 %s"><img class="club-logo" src="%s%s">%s</td>""" %(desktop_class, images_url, guests_img, guests)
		br_tag = soup.new_tag('br')
		date = i.find_all('td')[1].get_text() + ' ' + i.find_all('td')[7].get_text() + ', ' + i.find_all('td')[2].get_text()
		date_desktop = """<td class="col-5 %s"><span class="place">%s</span></td>""" % (desktop_class, date)
		date_tablet = """<td class="col-8 %s text-center">
             <span class="badge badge-success">Тур %s</span><br>
             <b>%s – %s</b><br>
             <span class="place">%s</span></td>""" % (tablet_class, tour, owners, guests, date)
		#date.insert(4, new_tag)
		mobile_td = """<td class="%s">
             <span class="badge badge-success">Тур %s</span><br>
             <img class="club-logo-small" src="%s%s"> <b>%s – %s</b> <img class="club-logo-small" src="%s%s"><br>
             <span class="place">%s</span>
           </td>""" %(mobile_class, tour, images_url, owners_img, owners, guests, images_url, guests_img, date)
		tour_list += """<tr class="row">%s %s %s %s %s %s %s %s</tr>""" % (tour_th, owners_desktop, guests_desktop, date_desktop, owners_tablet_image, date_tablet, guests_tablet_image, mobile_td)	


with open(TEMP_DIR + 'players_table') as table:
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

with open(TEMP_DIR + 'disqual_table') as table:
	soup = BeautifulSoup(table, 'lxml')
	disqual_table = soup.find('div').get_text()


html = open(HOME_DIR + 'template.html').read()
template = Template(html)


with open(HOME_DIR + "index.html", "w") as index:
	index.write(template.render(tournament_table=tournament_table, calendar_table=tour_list,
		players_table=players_table, disqual_table=disqual_table))

shutil.rmtree(HOME_DIR + 'temp_tables')