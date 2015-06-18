from bs4 import BeautifulSoup
import urllib2
import re
import threading
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db=client.test
Filmography=db.Filmography

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
	print name
	image="none"
	try:
		image=str(top.find('div', {"class":"image"}).find('img')['src']).decode('unicode_escape')
	except Exception as e:
		print e
	print image

	#print linkclass="article name-overview"
	filmo=soup.find('div',{'id':'filmography'})
	# category # name # imagelink # year

	data={}
	divs=filmo.find_all('div',{'class':'filmo-row'})
	print len(divs)
	for di in divs:
		print di['id']
		year=str(di.find('span',{'class':'year_column'}))
		year=re.findall(r"\d{4}",year)
		if year!=[]:
			year=year[0]
		else:
			year="none"
		di_parts=di['id'].split("-")
		category=di_parts[0]

		film_id=di_parts[1].decode('unicode_escape')
		film_name=di.find('a').get_text().decode('unicode_escape')
		print film_name
		film_link="http://www.imdb.com/title/"+str(di_parts[1]).decode('unicode_escape')
		film_image_link=get_film_image_link(film_link).decode('unicode_escape')
		print film_link
		print year

		film_data={film_name:[film_link,film_image_link,year]}
		print film_data

		if category in data.keys():
			data[category].append(film_data)
		else:
			data[category]=[film_data]

		filmography={'artist':name,'image':image,'imdb_profile_link':link,'filmography':data}
		print"**************"
		print data
		print"##############"
		print filmography
		Filmography.insert(filmography)
	##filmography


def main(call):
	index=1
	while True:
		while threading.activeCount()<100:
			t=threading.Thread(target=artist,args=(index,))
			t.start()
			fil=open("counter.txt","w")
			fil.write(str(index))
			fil.write("\n")
			fil.close()
			print index
			index+=1

main("g")

#artist("0424103")

