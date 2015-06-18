from bs4 import BeautifulSoup
import urllib2
import re
import threading
import unicodedata
import json


def get_film_image_link(link):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(link,headers=hdr)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page.read())
	top = soup.find('div', {"id":"title-overview-widget"})
	image_link="none"
	try:
		image_link=str(top.find('div', {"class":"image"}).find('img')['src'])
		print image_link
	except Exception as e:
		print e
	return image_link


#get_film_image_link("http://www.imdb.com/title/tt1849718/")

def artist(id):
	link="http://www.imdb.com/name/nm"+str(id)
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(link,headers=hdr)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page.read())
	top = soup.find('div', {"class":"article name-overview"})
	name=top.find('td',{"id":"overview-top"}).h1.get_text().replace("\n","").replace(" ","",1)
	name=unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
	name
	print type(name)
	print name
	image="none"
	try:
		image=str(top.find('div', {"class":"image"}).find('img')['src']).decode('unicode_escape')
	except Exception as e:
		print e
	print image

def main(call):
	fil=open("counter.txt","r+")
	index=1
	while True:
		while threading.activeCount()<1000:
			t=threading.Thread(target=artist,args=(index,))
			t.start()
			fil.write(str(index))
			fil.write("\n")
			print index
			index+=1

#main("g")

artist("0461498")

