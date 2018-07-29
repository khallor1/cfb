# Copyright 2018 Kieran Halloran
# ESPN cfb web scraper
# import libraries
import json
import requests
from bs4 import BeautifulSoup

#make a player from html row
def mkplayer(row):
	dict = {}
	dict['no'] = row[0].get_text()
	dict['name'] = row[1].get_text()
	dict['pos'] = row[2].get_text()
	dict['ht'] = row[3].get_text()
	dict['wt'] = row[4].get_text()
	dict['class'] = row[5].get_text()
	dict['hometown'] = row[6].get_text()
	return dict

#list of players for a given team
def mkroster(url):
	#parse html contents
	page = requests.get(url).text
	soup = BeautifulSoup(page, 'html.parser')

	#get rows of roster table
	rows = soup.find('table', 'tablehead').contents
	del rows[:2]

	#create a list of players
	players = []
	for r in rows:
		player = mkplayer(r.contents)
		players.append(player)
	return players

#creates list of teamnames, attached to rosters
def mkteams():
	#return this list of team objects
	out = []

	#base url
	baseurl = 'http://www.espn.com/college-football/teams'
	#parse html
	page = requests.get(baseurl).text
	soup = BeautifulSoup(page, 'html.parser')

	#find list of fbs teams
	fbs = soup.find('div', class_='span-2')
	teams = fbs.find_all('li')

	#add teamname and roster to list
	for li in teams:
		name = li.find('h5').get_text()
		roster = li.find('a', string='Roster')['href']
		roster = 'http://www.espn.com' + roster
		players = mkroster(roster)
		obj = {'teamname': name, 'roster': players}
		out.append(obj)
	return out

# write result to file
with open('result.json', 'w') as fp:
    json.dump(mkteams(), fp)

