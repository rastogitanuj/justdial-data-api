from google.appengine.ext import ndb

class cityDB(ndb.Model):
	city_name = ndb.StringProperty()
	state_name = ndb.StringProperty()
	alt_name = ndb.StringProperty()
	city_state = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty()

class gymDB(ndb.Model):
	gym_name = ndb.StringProperty()
  	gym_number = ndb.StringProperty()
	gym_address = ndb.StringProperty()
	gym_city = ndb.StringProperty(indexed = True)

class FailTable(ndb.Model):
	fail_city = ndb.StringProperty()
	fail_page_no = ndb.IntegerProperty()