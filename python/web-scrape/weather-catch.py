#!/usr/bin/env python

import requests, os, bs4, pprint


url = 'http://www.weather.com.cn/weather/101020100.shtml'

print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')

whetherList = []
for whether in soup.select('li.sky.skyid.lv3'):
	whetherJson = {"h1": whether.h1.get_text(), "title": whether.p[0].get_text(), "tem": whether.p[1].get_text(), "win": whether.p[2].get_text()}

	
	whetherList.append(whetherJson)

pprint.pprint(whetherList)




