import sys
sys.path.append('beautifulsoup4-4.2.1')
from bs4 import BeautifulSoup
import urllib2
import time
import traceback

class justSpider(object):
    
    """Spider responsible for crawling justdial"""

    def __init__(self, city, entity = "Gyms"):
        self.city = city
        self.entity = entity
    
    def parsePage(self, page_no = 1):
        
        url = "http://www.justdial.com/"+self.city+"/"+self.entity+"/page-"+str(page_no)
        
        try:
            page = urllib2.urlopen(url)
        except Exception as exp:
            print str(exp), traceback.format_exc()
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

        gyms = []
        for e in jrcls:
            try:
                
                p = e.find_all('p')[:3] # first 3 paragraphs contain relevent information.
                name = p[0].find_all('a')
                
                if len(name) >=2: # for gym-name and number
                    if p[1]['class'][0].strip() == "jrcw":
                        gym_name = name[1]["title"]
                        gym_url = name[1]["href"]
                        gym_num = p[1].text
                    else:
                        gym_name = name[1]["title"]
                        gym_url = name[1]["href"]
                        gym_num = "N.A"
                else:
                    if p[1]['class'][0].strip() == "jrcw": # Gym number is not present
                        gym_name = p[0].a["title"]
                        gym_url = p[0].a["href"]
                        gym_num = p[1].text
                    else:
                        gym_name = p[0].a["title"]
                        gym_url = p[0].a["href"]
                        gym_num = "N.A"
                
                spans = p[2].find_all("span")
                gym_add = spans[2].text.strip()
                
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
                
                gyms.append((gym_name, gym_num, gym_add, gym_url))

            except Exception as exp:
                print str(exp), traceback.format_exc()
                raise exp

        resultstr = ""
        cnt = 1
        for gym in gyms:
            resultstr+= str(cnt)+'. '+gym[0]+"</br>"+gym[1]+"</br>"+gym[2]+"</br>"+gym[3]+"</br>"+"<hr/>"
            cnt+=1
    
        print "Done page"
        return resultstr

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
            data = row.find_all('a')
            city_list.append( (data[0].text, data[1].text) )

        return city_list

