from spiders import justSpider
from datastore import gymDB
from google.appengine.ext import ndb
import traceback

def mineGymData(city_name):

	spider = justSpider(city_name)
	page_no = 1
	while True:
		try:
			gym_list = spider.parsePage(page_no)
			if gym_list is None:
				break

			entity_list = []
			for gym in gym_list:
				mykey = ndb.Key('gymDB', gym[3])
				if city_name.lower() in gym[2].lower():
					if gymDB.get_by_id(gym[3]) is None:
						entity_list.append( 
							gymDB(key = mykey, gym_name = gym[0], gym_number = gym[1], gym_address = gym[2], gym_city = city_name.lower()) 
							)
					else:
						raise Exception("Assertion Fail. Check")

			ndb.put_multi(entity_list)
			page_no+=1

		except Exception as exp:
			print str(exp), traceback.format_exc()

def fetchGymData(city_name):

	city_name = city_name.lower()

	gym_query = gymDB.query( gymDB.gym_city == city_name )
	entity_list = gym_query.fetch()

	gym_list = []
	for entity in entity_list:
		gym_list.append((entity.gym_name, entity.gym_number, entity.gym_address))

	return gym_list
