#!/usr/bin/env python

from selenium import webdriver

url = 'https://en.mail.qq.com/cgi-bin/loginpage'
account = '31974786'
password = 'qzlin157'

browser = webdriver.Firefox()
browser.get(url)

accountElem = browser.find_element_by_id('u')
passwordElem = browser.find_element_by_id('p')

accountEle.send_keys(account)
passwordElem.send_keys(password)

passwordElem.submit()
