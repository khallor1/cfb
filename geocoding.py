import os, googlemaps
from pymongo import MongoClient

#connect to MongoDB and Google Maps
MONGO_URI = os.environ['MONGO_URI']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
mongo = MongoClient(MONGO_URI)
gmaps = googlemaps.Client(GOOGLE_API_KEY)

# input hometwon, return dict with 'lat' and 'lng' keys
def get_geo_data(hometown):
	geocode_result = gmaps.geocode(hometown)
	print('coding {}'.format(hometown))
	if hometown == '--':
		return hometown
	return geocode_result[0]['geometry']['location']

#iterate through distinct homewtown locations
db = mongo.test
for town in db.rosters.distinct('roster.hometown'):
	#get geolocation data
	loc = get_geo_data(town)
	#append data to all queried players with that hometown
	db.rosters.update_many(
		{},
		{'$set': {'roster.$[elem].loc': loc}},
		array_filters=[{'elem.hometown': town}]
	)
