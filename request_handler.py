import webapp2
import traceback
from spiders import justSpider, citySpider
import city_mods

class MainPage(webapp2.RequestHandler):

    MAIN_PAGE_HTML ="""
    <html>
      <body>
        <form action="/showGyms" method="get">
            City Name: <input type='text' name = 'city_name'/>
            <input type = 'submit' value='Go'>
        </form>
        <br/><hr/>
        <form action="/showCities" method="get">
            <input type = 'submit' value='See citites'>
        </form>
        <form action="/refreshCities" method="get">
            <input type = 'submit' value='Refresh City Data'>
        </form>
      </body>
    </html>
    """

    def get(self):

        try:
            self.response.write(self.MAIN_PAGE_HTML)
            
        except Exception as e:
            print e

class showGyms(webapp2.RequestHandler):

    def get(self):
        city_name = self.request.get('city_name')
        spider = justSpider(city_name)
        output = ""
        for page_no in xrange(1,3):
            try:
                output += spider.parsePage(page_no)
                #self.response.write(output)
            except Exception as exp:
                output += "Exception encontered in page number "+str(page_no)+": "+str(exp)+"<br/>"
        self.response.write(output)

class showCities(webapp2.RequestHandler):

    def get(self):
        city_list = city_mods.fetchCityData()
        output = "Cities stored in the database:<hr/>"
        cno = 1
        for city in city_list:
            output+= str(cno)+". "+city[0]+" -- "+city[1]+" -- "+str(city[2])+" -- "+city[3]+"<br/>"
            cno+=1
        self.response.write(output)

class refreshCityData(webapp2.RequestHandler):

    def get(self):
        city_mods.refreshData()
        city_list = city_mods.fetchCityData()
        output = "Cities stored in the database:<hr/>"
        cno = 1
        for city in city_list:
            output+= str(cno)+". "+city[0]+" -- "+city[1]+" -- "+str(city[2])+" -- "+city[3]+"<br/>"
            cno+=1
        self.response.write(output)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/showGyms', showGyms),
    ('/showCities', showCities),
    ('/refreshCities', refreshCityData)
], debug=True)
