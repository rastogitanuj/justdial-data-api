from spiders import citySpider
from datastore import cityDB
from google.appengine.ext import ndb
import traceback
import datetime as dt

def refreshData():
	try:
		spider = citySpider()
		city_list = spider.parse()

		"""First empty the data-store"""
		city_query = cityDB.query()
		entity_list = city_query.fetch()
		key_list = []
		for entity in entity_list:
			key_list.append(entity.key)
		ndb.delete_multi(key_list)
		
		"""Store fresh cities"""
		entity_list = []
		for city in city_list:
			city_name = ""
			for i in xrange(len(city[0])): # replcaing spaces with '-'(dash)
	  			if city[0][i] == ' ':
	 				city_name += '-'
	 			else:
	 				city_name += city[0][i]
	 		city_name = city_name.lower()
			mykey = ndb.Key('cityDB',city_name)
			if cityDB.get_by_id(city_name) is None:
				entity = cityDB(key = mykey, alt_name = city[1], timestamp = dt.datetime(2000,1,1,0,0,0,0))
			else:
				raise Exception("Assertion Fail. Two cities with same name encountered")
			entity_list.append(entity)
		ndb.put_multi(entity_list)

	except Exception as exp:
		raise exp

def add_city(city_name, alt_name = None):
	try:
		mykey = ndb.Key('cityDB',city_name)
		if cityDB.get_by_id(city_name) is None:
			entity = cityDB(key = mykey, alt_name = alt_name, timestamp = dt.datetime(2000,1,1,0,0,0,0))
			entity.put()
			return "City added"
		else:
			return "City already present"
	except Exception as exp:
		raise exp

def fetchCityData():
	try:
		city_query = cityDB.query()
		entity_list = city_query.fetch()
		city_list = []
		for entity in entity_list:
			city_list.append((entity.key.id(), entity.alt_name))
	except Exception as exp:
		print str(exp), traceback.format_exc()
		raise exp
	return city_list

def getValidCities():

	SENT = dt.datetime(2000,1,1,0,0,0,0)
	city_query = cityDB.query( cityDB.timestamp > SENT )
	entity_list = city_query.fetch()
	city_list = []
	for entity in entity_list:
		city_list.append(entity.key.id())
	return city_list