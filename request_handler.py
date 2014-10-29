import webapp2
import traceback
from spiders import justSpider

class MainPage(webapp2.RequestHandler):

    MAIN_PAGE_HTML ="""
    <html>
      <body>
        <form action="/showGyms" method="get">
            City Name: <input type='text' name = 'city_name'/>
            <input type = 'submit' value='Go'>
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

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/showGyms', showGyms)
], debug=True)
