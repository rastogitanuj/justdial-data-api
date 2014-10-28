import sys
from bs4 import BeautifulSoup
import urllib2
import time
import traceback

class justSpider(object):
    
    def __init__(self, city, entity = "Gyms")
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
                p = e.find_all('p')[:2] # first 2 paragraphs contain relevent information.
                name = p[0].find_all('a')
                if len(name) >=2:
                    if p[1]['class'][0].strip() == "jrcw":
                        gyms.append( (name[1].text, p[1].text) ) # Gym name and number are appended as a tuple
                    else:
                        gyms.append( (name[1].text, "N.A") )
                else:
                    if p[1]['class'][0].strip() == "jrcw":
                        gyms.append( (p[0].a.text, p[1].text) )
                    else:
                        gyms.append( (p[0].a.text, "N.A") )
            except Exception as exp:
                print str(exp), traceback.format_exc()
                raise exp

        for gym in gyms:
            print gym[0]+",", gym[1]
    
        print "Done page #:",page_no
