#!/usr/bin/env python

import urllib2, os, bs4, pprint


url = 'http://www.weather.com.cn/weather/101020100.shtml'

print('Downloading page %s...' % url)
html = urllib2.urlopen(url).read()


soup = bs4.BeautifulSoup(html, 'lxml')
print soup.head.title

whetherList = []
for whether in soup.select('li.sky'):
	tmp = whether.p
	whetherJson = { "h1": whether.h1.get_text(),	"title": tmp[0].get_text(), "tem": tmp[1].get_text(), "win": tmp[2].get_text()}

	whetherList.append(whetherJson)
	print whetherJson.h1

pprint.pprint(whetherList)




