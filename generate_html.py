#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib.request
from jinja2 import Template
import os
import shutil
from config import config
import sys
from datetime import datetime
import re


HOME_DIR = config.get('home_dir', 'path')
os.mkdir(HOME_DIR + 'temp_tables/')
TEMP_DIR = HOME_DIR + 'temp_tables/'

tournament_stats_url = "https://lfl.ru/?ajax=1&method=tournament_stats_table&tournament_id=5098&club_id=2356&season_id=39"
tournament_calendar_url= "https://lfl.ru/?ajax=1&method=tournament_calendar_table&tournament_id=0&club_id=2356&season_id=39"
tournament_results_url = "https://lfl.ru/?ajax=1&method=tournament_resault_table&tournament_id=0&club_id=2356&season_id=39"
players_stats_url = "https://lfl.ru/?ajax=1&method=tournament_squads_table&tournament_id=5098&club_id=2356&season_id=39"
disqualifications_url= "https://lfl.ru/?ajax=1&mode=new_format&method=tournament_disqualifications_table&tournament_id=5098&club_id=2356&season_id=39"
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'

up = ['pos_1', 'pos_2']
up2 = ['pos_3', 'pos_4']
down = ['pos_15', 'pos_16', 'pos_17', 'pos_18']
down2 = ['pos_19', 'pos_20']

payload  = {}
headers = {}


def catch_exception(func):
	def wrapper(*args):
		try:
			return func(*args)
		except:
			print('Something went wrong!' + '	' +  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
			shutil.rmtree(HOME_DIR + 'temp_tables')
			sys.exit()
	return wrapper


@catch_exception
def get_table(file, url):
	with open(file, 'w') as f:
		stats_table = requests.request("GET", url, headers=headers, data = payload, timeout=60)
		f.write(stats_table.text)


get_table(TEMP_DIR + 'tournament_table', tournament_stats_url)
get_table(TEMP_DIR + 'calendar_table', tournament_calendar_url)
get_table(TEMP_DIR + 'players_table', players_stats_url)
get_table(TEMP_DIR + 'results_table', tournament_results_url)
get_table(TEMP_DIR + 'disqual_table', disqualifications_url)


#generate tournament table
@catch_exception
def tournament_table():
	with open(TEMP_DIR + 'tournament_table') as table:
		soup = BeautifulSoup(table, 'lxml')
		table = soup.find('tbody')
		images = table.find_all('img') 
		for img in images:
			del img['align']

		a = table.find_all('a')
		for i in a:
			i['href'] = 'https://lfl.ru' + i['href']
			i['target'] = '_blank'
			i['class'] = 'text-body'

		td = table.find_all('td')
		for i in td:
			i['class'] = 'col text-center'

		pos = 1
		tr = table.find_all('tr')
		for i in tr:
			td = i.find_all('td')[1]
			td.extract()
			td = i.find_all('td')[1]
			td['class'] = 'col-3 team text-left'	
			del i['class']
			i['class'] = 'pos_' + str(pos)
			pos += 1
			if i['class'] in up:
				i['class'] = 'row table-success'
			elif i['class'] in up2:
				i['class'] = 'row table-warning'
			elif i['class'] in down:
				i['class'] = 'row table-danger'
			elif i['class'] in down2:
				i['class'] = 'row bg-danger'
			else:
				i['class'] = 'row table-light'
			td_6 = i.find_all('td')[6]
			td_6['class'] = 'col d-sm-none d-md-block d-none text-center'
			td_7= i.find_all('td')[7]
			td_7['class'] = 'col d-sm-none d-md-block d-none text-center'
			td_8= i.find_all('td')[8]
			td_8['class'] = 'col d-sm-none d-md-block d-none text-center'
		return table


def parse_schedule_for_bot():
	with open(TEMP_DIR + 'calendar_table') as table:
		with open(HOME_DIR + "schedule.txt", "w") as schedule:
			soup = BeautifulSoup(table, 'lxml')
			table = soup.find('tbody')
			tr = table.find_all('tr')
			for i in tr:
				if len(i.find_all('td')[1].get_text()) > 1:
					date = (i.find_all('td')[1].get_text() + ' ' + i.find_all('td')[7].get_text() + ', ' + i.find_all('td')[2].get_text()).strip()
					teams = i.find_all('td')[3].get_text().strip() + ' - ' + i.find_all('td')[5].get_text().strip()
					game = date + '\n' +  teams
					schedule.write(game)


parse_schedule_for_bot()


#generate calendar
@catch_exception
def calendar_table():
	with open(TEMP_DIR + 'calendar_table') as table:
		soup = BeautifulSoup(table, 'lxml')
		table = soup.find('tbody')

		a = table.find_all('a')
		for i in a:
			i['class'] = 'text-body'
			i['target'] = '_blank'

		td = table.find_all('td')
		for i in td:
			i['class'] = 'align-middle'
			del i['style']
			del i['width']

		tr = table.find_all('tr')
		tour_list = ''


		def tour_list_desktop():
			return """<th class="col-2 d-sm-none d-md-block d-none">%s</th>
						<td class="col-3 d-sm-none d-md-block d-none text-right">%s<img class="club-logo" src="%s"></td>
						<td class="col-3 d-sm-none d-md-block d-none"><img class="club-logo" src="%s">%s</td>
						<td class="col-4 d-sm-none d-md-block d-none"><span class="place">%s</span></td>
					""" %(tour, host, path_to_host_img, path_to_guest_img, guest, date)


		def tour_list_tablet():
			return """<td class="col-2 d-none d-sm-block d-md-none text-center"><img class="club-logo-big" src="%s"></td>
						<td class="col-8 d-none d-sm-block d-md-none text-center">
						<span class="badge badge-success">Тур %s</span><br>
						<b>%s – %s</b><br>
						<span class="place">%s</span></td>
						<td class="col-2 d-none d-sm-block d-md-none text-center"><img class="club-logo-big" src="%s"><br></td>
					""" %(path_to_host_img, tour, host, guest, date, path_to_guest_img)


		def tour_list_mobile():
			return """<td class="col-12 d-block d-sm-none text-center">
						<span class="badge badge-success">Тур %s</span><br>
						<img class="club-logo-small" src="%s"><b>%s – %s</b><img class="club-logo-small" src="%s"><br>
						<span class="place">%s</span></td>
					"""%(tour, path_to_host_img, host, guest, path_to_guest_img, date)

		for i in tr:
			find_all_img = i.find_all('img')
			tour = i.find_all('td')[0].get_text()
			host = i.find_all('td')[3].get_text()
			host_img = i.find_all('img')[0]['src']
			guest = i.find_all('td')[5].get_text()
			guest_img = i.find_all('img')[1]['src']
			if len(i.find_all('td')[1].get_text()) > 1:
				date = (i.find_all('td')[1].get_text() + ' ' + i.find_all('td')[7].get_text() + ', ' + i.find_all('td')[2].get_text()) 
			else:
				date = '-'
			host_filename = host_img.split("/")[-1]
			guest_filename = guest_img.split("/")[-1]
			path_to_host_img = '/images/' + host_filename
			path_to_guest_img = '/images/' + guest_filename
			outpath = os.path.join(HOME_DIR + 'images/', host_filename)
			outpath2 = os.path.join(HOME_DIR + 'images/', guest_filename)
			tour_list += """<tr class="row">%s%s%s</tr>"""%(tour_list_desktop(), tour_list_tablet(), tour_list_mobile())
			if os.path.exists(outpath) and os.path.exists(outpath2):
				pass
			else:
				opener = urllib.request.build_opener()
				opener.addheaders = [('User-Agent', user_agent)]
				urllib.request.install_opener(opener)
				urllib.request.urlretrieve(host_img, outpath)
				urllib.request.urlretrieve(guest_img, outpath2)
		return tour_list


#generate players table
#@catch_exception
def players_table():
	with open(TEMP_DIR + 'players_table') as table:
		soup = BeautifulSoup(table, 'lxml')
		table = soup.find('tbody')

		tr = table.find_all('tr')
		for i in tr:
			i['class'] = 'table-light'
			del i['data-division-id']
			del i['data-tournament-id']

		tour_header = table.find_all(attrs={"class":"tour-header"})
		for i in tour_header:
			i['class'] = 'amplua text-center font-weight-bold'

		players = table.find_all(attrs={"class":"player"})		
		for i in players:
			i['href'] = 'https://lfl.ru' + i['href']
			i['class'] = 'text-body'
			i['target'] = '_blank'

		images = table.find_all(attrs={"class":"usr-image_link"})
		for img in images:
			img['href'] = 'https://lfl.ru' + img['href']
			img['target'] = '_blank'
			style = img['style']
			image = re.search("http.*[)]", style)
			image_url = style[image.start():image.end()-1]
			image_name = image_url.split("/")[-1]
			img['style'] = '''"background: url(fc-camelot.ru/images/%s)"''' %image_name
			img['class'] = (img['class'] + ['pr-1'])
			outpath = os.path.join(HOME_DIR + 'images/', image_name)
			if os.path.exists(outpath):
				pass
			else:
				opener = urllib.request.build_opener()
				opener.addheaders = [('User-Agent', user_agent)]
				urllib.request.install_opener(opener)
				urllib.request.urlretrieve(image_url, outpath)

		td = table.find_all('td')
		for i in td:
			if not i.has_attr('class'):
				i['class'] = 'text-center align-middle'
			span = i.find_all('span')
			for s in span:
				s.extract()	
		return table


#generate disqual table
@catch_exception
def disqual_table():
	with open(TEMP_DIR + 'disqual_table') as table:
		soup = BeautifulSoup(table, 'lxml')
		table = soup.find('div').get_text()
		return table


html = open(HOME_DIR + 'template.html').read()
template = Template(html)

tournament = tournament_table()
calendar = calendar_table()
players = players_table()
disqual = disqual_table()

with open(HOME_DIR + "index.html", "w") as index:
	index.write(template.render(tournament_table=tournament, calendar_table=calendar,
		players_table=players, disqual_table=disqual))
	print('index.html updated successfully!' + '	' +  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

shutil.rmtree(HOME_DIR + 'temp_tables')
