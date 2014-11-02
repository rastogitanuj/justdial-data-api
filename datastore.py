from google.appengine.ext import ndb

class cityDB(ndb.Model):
	city_name = ndb.StringProperty()
	state_name = ndb.StringProperty()
	alt_name = ndb.StringProperty()
	city_state = ndb.StringProperty()