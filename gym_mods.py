from spiders import justSpider
from datastore import gymDB, cityDB, FailTable
from google.appengine.ext import ndb
import traceback, datetime as dt

def mineGymData(city_name, single = False, mypage = None):

	spider = justSpider(city_name)
	
	if mypage is None:
		page_no = 1
	else:
		page_no = mypage

	city_name = city_name.lower()
	while True:
		try:
			gym_list = spider.parsePage(page_no)
			if gym_list is None:
				break

			entity_list = []
			for gym in gym_list: #gym tuple is (gym_name, gym_num, gym_add, gym_url)
				mykey = ndb.Key('gymDB', gym[3])
				#print page_no, gym[0], gym[1]
				if city_name in gym[2].lower(): #if gym is in the correct city
					entity = gymDB.get_by_id(gym[3])
					if entity is None: # entity is new
						entity_list.append( 
							gymDB(key = mykey, gym_name = gym[0], gym_number = gym[1], gym_address = gym[2], gym_city = city_name)
							)
					elif entity.gym_city ==  city_name: #entity is already present
						print "*********Duplicate***********"
						print gym[0], city_name, page_no, len(gym_list), gym[1]
						print entity.gym_name, entity.gym_city, entity.key.id(), entity.gym_number
						entity_list.append( 
							gymDB(key = mykey, gym_name = gym[0], gym_number = gym[1], gym_address = gym[2], gym_city = city_name)
							)
					else:
						print gym[0], city_name
						print entity.gym_name, entity.gym_city
						raise Exception("Assertion Failed in mineGymData, gym_mods.py. gym_name = "+ gym[0])

			ndb.put_multi(entity_list)
			if single:
				break

		except Exception as exp:
			print str(exp), traceback.format_exc()
			entity = FailTable(fail_city = str(city_name), fail_page_no = page_no)
			entity.put()
		page_no+=1

	# updating city's timetamp
	city_entity = cityDB.get_by_id(city_name)
	city_entity.timestamp = dt.datetime.now()
	city_entity.put()


def fetchGymData(city_name):
	""" Query and return gyms by city name """

	city_name = city_name.lower()

	gym_query = gymDB.query( gymDB.gym_city == city_name )
	entity_list = gym_query.fetch()

	print "No. of query results: ", len(entity_list)

	gym_list = []
	for entity in entity_list:
		gym_list.append((entity.gym_name, entity.gym_number, entity.gym_address))

	return gym_list

def updateGymData(lim = 7):

	""" Upadte the gym kind by 'lim' entries """

	freshperiod = dt.timedelta(days = 7) # amount of time for which data should not be updated.

	failtable_query = FailTable.query()
	failentity_list = failtable_query.fetch(lim)
	for entity in failentity_list:
		print "Parsing Fail city:", entity.fail_city, "fail page number:", entity.fail_page_no
		mineGymData( entity.fail_city, single = True, mypage = entity.fail_page_no)

	#city_query = cityDB.query( (dt.datetime.now() - ((dt.datetime)cityDB.timestamp) ) >= freshperiod )
	city_query = cityDB.query( cityDB.timestamp <= dt.datetime.now() - freshperiod )

	entity_list = city_query.fetch(lim)

	if entity_list == [] and failentity_list == []:
		print "All cities updated."
		return None # data for all cities has been updated.

	city_list = []
	for entity in entity_list:
		city_name = entity.key.id()
		print "Mining:", city_name
		city_list.append(city_name)
		mineGymData(str(city_name))

	return city_list