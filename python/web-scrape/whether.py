#!/usr/bin/env python


import urllib2, bs4, pprint

url = r'http://www.weather.com.cn/weather/101020100.shtml'

html = urllib2.urlopen(url).read()
soup = bs4.BeautifulSoup(html, 'lxml')

print soup.original_coding
print soup.select('head title')[0].get_text()


whetherList = []
whetherElemList = soup.select('li.sky.skyid')
for whetherElem in whetherElemList:
    para = whetherElem.find_all('p')
    whetherDict = {'h1': whetherElem.h1.get_text(),
                   'wea': para[0].get_text(),
                   'tem': para[1].get_text(),
                   'win': para[2].get_text()}
    whetherList.append(whetherDict)
    print '----'*10
    print 'h1 = ' + whetherDict.get('h1')
    print 'wea = ' + whetherDict.get('wea')
    print 'tem = ' + whetherDict.get('tem')
    print 'win = ' + whetherDict.get('win')


print whetherList[0].get('h1')
print len(whetherList)
pprint.pprint(whetherList)