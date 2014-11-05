import webapp2
import traceback
from spiders import justSpider, citySpider
import city_mods, gym_mods

class MainPage(webapp2.RequestHandler):

    MAIN_PAGE_HTML ="""
    <html>
      <body>
        <form action="/fetchGymData" method="get">
            Mine gyms in city: <input type='text' name = 'city_name'/>
            <input type = 'submit' value='Fetch Data'>
        </form>
        <br/><hr/>
        Before viewing any city, first mine it above.<hr/>
        <form action="/showGyms" method="get">
            View gyms in city: <input type='text' name = 'city_name'/>
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

class mineGymData(webapp2.RequestHandler):

    def get(self):
        city_name = self.request.get('city_name')
        gym_mods.mineGymData(city_name)

class crawlGyms(webapp2.RequestHandler):

    def get(self):
        city_name = self.request.get('city_name')
        spider = justSpider(city_name)
        output = ""
        cnt = 1
        for page_no in xrange(1,3):
            try:
                gyms = spider.parsePage(page_no)
                resultstr = ""
                for gym in gyms:
                    resultstr+= str(cnt)+'. '+gym[0]+"</br>"+gym[1]+"</br>"+gym[2]+"</br>"+gym[3]+"</br>"+"<hr/>"
                    cnt+=1
                output += resultstr
                #self.response.write(output)
            except Exception as exp:
                output += "Exception encontered in page number "+str(page_no)+": "+str(exp)+"<br/>"
        self.response.write(output)

class showGyms(webapp2.RequestHandler):

    def get(self):
        resultstr = ""
        try:
            city_name = self.request.get('city_name')
            gym_list = gym_mods.fetchGymData(city_name)
            cnt = 1
            for gym in gym_list:
                resultstr+= str(cnt)+'. '+gym[0]+"</br>"+gym[1]+"</br>"+gym[2]+"</br>"+"<hr/>"
                cnt+=1
        except Exception as exp:
            print "Exception: "+str(exp), traceback.format_exc()
        self.response.write(resultstr)



class showCities(webapp2.RequestHandler):

    def get(self):
        city_list = city_mods.fetchCityData()
        output = "Cities stored in the database:<hr/>"
        cno = 1
        for city in city_list:
            output+= str(cno)+". "+city[0]+"  ---  "+city[1]+"  ---  "+city[2]+"  ---  "+str(city[3])+"<br/>"
            cno+=1
        self.response.write(output)

class refreshCityData(webapp2.RequestHandler):

    def get(self):
        city_mods.refreshData()
        city_list = city_mods.fetchCityData()
        output = "Cities stored in the database:<hr/>"
        cno = 1
        for city in city_list:
            output+= str(cno)+". "+city[0]+"  ---  "+city[1]+"  ---  "+city[2]+"  ---  "+str(city[3])+"<br/>"
            cno+=1
        self.response.write(output)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/crawlGyms', crawlGyms),
    ('/showGyms', showGyms),
    ('/showCities', showCities),
    ('/refreshCities', refreshCityData),
    ('/mineGymData', mineGymData)
], debug=True)
