# import libraries
import urllib2
from bs4 import BeautifulSoup

#parse html contents
url = 'http://www.espn.com/college-football/team/roster/_/id/25/california-golden-bears'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

#get rows of roster table
rows = soup.find('table', 'tablehead').contents
del rows[:2]

def mkdict(row):
	dict = {}
	dict['no'] = row[0].get_text()
	dict['name'] = row[1].get_text()
	dict['pos'] = row[2].get_text()
	dict['ht'] = row[3].get_text()
	dict['wt'] = row[4].get_text()
	dict['class'] = row[5].get_text()
	dict['hometown'] = row[6].get_text()
	return dict

players = []
for r in rows:
	dict = mkdict(r.contents)
	players.append(dict)
print(players)	

