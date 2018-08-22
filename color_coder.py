import os, requests, re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from fuzzywuzzy import fuzz

# #connect to MongoDB
# MONGO_URI = os.environ['MONGO_URI']
# mongo = MongoClient(MONGO_URI)

def mkSoup(url):
	page = requests.get(url).text
	return BeautifulSoup(page, 'html.parser')

#map mongo names to searchable full team names
def getTeamNames():
	out = {}

	soup = mkSoup('http://www.espn.com/college-football/teams')

	#find list of fbs teams
	fbs = soup.find('div', class_='span-2')
	teams = fbs.find_all('li')

	#add teamname and roster to list
	for li in teams:
		#name matching 
		mongoName = li.find('h5').get_text()
		url = li.find('h5').find('a')['href']
		match = re.search(r'id/\d+/(.*)', url)
		if match:
			colorMatchName = requests.utils.unquote(match.group(1)).replace('-',' ')
			out[mongoName] = colorMatchName
	return out

def searchTeamNames():
	out = {}
	soup = mkSoup('https://teamcolorcodes.com/ncaa-color-codes/')
	content = soup.find('div', class_='entry-content')
	#skip first 'p' tag (conferences)
	for p in content.p.find_next_siblings('p'):
		#get links for each team
		for a in p.find_all('a'):
			teamname = a.get_text()
			link = a['href']
			out[teamname] = link
	return out

print(searchTeamNames())

#use fuzzy to match teamname to url, get colors from url and match to mongo name
def team_to_link():

#get primary and secondary colors, add to mongo

