from bs4 import BeautifulSoup
import urllib2
import re
import threading


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
	name=top.find('td',{"id":"overview-top"}).h1.get_text()
	print name
	image="none"
	try:
		image=str(top.find('div', {"class":"image"}).find('img')['src'])
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
		year=di.find('span',{'class':'year_column'}).get_text()
		di_parts=di['id'].split("-")
		category=di_parts[0]

		film_id=di_parts[1]
		film_name=di.find('a').get_text()
		print film_name
		film_link="http://www.imdb.com/title/"+str(di_parts[1])
		film_image_link=get_film_image_link(film_link)
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
	##filmography


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

artist("0424103")

