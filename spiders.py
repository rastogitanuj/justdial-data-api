import sys
sys.path.append('beautifulsoup4-4.2.1')
from bs4 import BeautifulSoup
import urllib2
import time
import traceback
from google.appengine.api import urlfetch

class justSpider(object):
    
    """Spider responsible for crawling justdial"""

    def __init__(self, city, entity = "Gyms"):
        self.city = city
        self.entity = entity
    
    def parsePage(self, page_no = 1):
        
        url = "http://www.justdial.com/"+self.city+"/"+self.entity+"/page-"+str(page_no)
        
        try:
            page = urllib2.urlopen(url, timeout = 20)
            urlfetch.set_default_fetch_deadline(20)
        except Exception as exp:
            print "Exception in justSpider, urllib2",str(exp)#, traceback.format_exc()
            raise exp
        
        src = BeautifulSoup(page.read())
        
        sections = src.find_all("section") #contains all section tags.

        jrcls = [] #each section with jbbg class contains item/gym infromation.
        
        try:
            for e in sections:
                if e.get('class') is not None:
                    if "jrcl" in e['class']:
                        jrcls.append(e)
        except Exception as exp:
            print str(exp), traceback.format_exc()
            raise exp

        if len(jrcls) == 0: #No more gyms
            return None

        gym_list = []
        for e in jrcls:
            try:
                
                p = e.find_all('p') # first 3 paragraphs contain relevent information.

                gym_num = None
                gym_add = None
                gym_name = None

                for para in p:

                    if para['class'][0].strip() == "jcnwrp":

                        spans = para.find_all('span')
                        for span in spans:

                            if span['class'][0].strip() == "jcn":

                                gym_name = span.a["title"]
                                gym_url = span.a["href"].split('/')[-1]

                    elif para['class'][0].strip() == "jrcw":
                        gym_num = para.text.strip()

                    elif para['class'][0].strip() == "jaid":

                        spans = para.find_all('span')
                        for span in spans:

                            if span['class'][0].strip() == "jaddt":

                                spans2 = span.find_all('span')
                                for span2 in spans2:
                                    if span2['class'][0].strip() == "mrehover":
                                         gym_add = span2.text.strip()

                if gym_name is None:
                    raise Exception("Assertion Failed. Gym must have a name")

                if gym_add is None:
                    print "$$$$\nIgnoring address-less gyms:", gym_name
                    continue
                
                """A mini algorithm for removing " in place ,city_name" suffix attached with each gym name"""
                namelen = len(gym_name)
                cut = namelen
                for i in xrange(namelen-3):
                    state = 0
                    if state == 0 and gym_name[i] == ' ':
                        state = 1
                    if state == 1 and gym_name[i+1] == 'i':
                        state = 2
                    if state == 2 and gym_name[i+2] == 'n':
                        state = 3
                    if state == 3 and gym_name[i+3] == ' ':
                        state = 4
                    if state == 4:
                        cut = i
                        break
                gym_name = gym_name[:cut]
                """ algorithm complete"""
                
                gym_list.append((gym_name, gym_num, gym_add, gym_url))

            except Exception as exp:
                print str(exp), traceback.format_exc()
                raise exp
    
        print "Done page: "+str(page_no)
        return gym_list


class citySpider(object):

    def parse(self):
        url = "http://en.wikipedia.org/wiki/List_of_most_populous_cities_in_India"
        
        try:
            page = urllib2.urlopen(url)
        except Exception as exp:
            print str(exp), traceback.format_exc()
            raise exp

        src = BeautifulSoup(page.read())

        table = src.table

        tr = table.find_all('tr')[1:] # first row contains the Field names

        city_list = []

        for row in tr:
            data = row.find_all('td')
            name = data[1].text.split('(')
            city_name = name[0].split('[')[0]
            alt_name = None
            if len(name) > 1:
                print name
                alt_name = name[1][:-1]
            #city_list.append( ( city_name, data[4].text, alt_name) ) #<- old, data[4].text --> state name
            city_list.append((city_name, alt_name))

        return city_list