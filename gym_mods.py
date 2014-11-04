from spiders import justSpider
from datastore import gymDB
from google.appengine.ext import ndb
import traceback

def getGymData(city_name):

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
							gymDB(key = mykey, gym_name = gym[0], gym_number = gym[1], gym_address = gym[2], gym_city = city_name) 
							)
					else:
						raise Exception("Assertion Fail. Check")

			ndb.put_multi(entity_list)
			page_no+=1

		except Exception as exp:
			print str(exp), traceback.format_exc()