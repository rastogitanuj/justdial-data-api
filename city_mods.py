from spiders import citySpider
from datastore import cityDB
from google.appengine.ext import ndb

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
			entity = cityDB(city_name = city[0], alt_name = city[2],state_name = city[1], city_state = city[0]+'_'+city[1])
			entity_list.append(entity)
		ndb.put_multi(entity_list)
	except Exception as exp:
		raise exp

def fetchCityData():
	try:
		city_query = cityDB.query()
		entity_list = city_query.fetch()
		city_list = []
		for entity in entity_list:
			city_list.append((entity.city_name, entity.city_state, entity.alt_name, entity.city_state))
	except Exception as exp:
		raise exp
	return city_list