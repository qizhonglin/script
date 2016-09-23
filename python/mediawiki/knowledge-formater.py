#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json, re

import requests
from wikimarkup import parselite
from pprint import pprint


def fetch_wikitext(url):
    r = requests.get(url)
    decode_json = json.loads(r.text)
    wikitext = decode_json["query"]["pages"].values()[0]["revisions"][0]["*"]
    return wikitext

def fetch_categories(wikitext):
    categories = []
    pattern = r'(\[\[Category:(.*)]])'
    for match in re.findall(pattern, wikitext):
        # print match[0]
        category = match[1]
        categories.append(category)

    return categories

def fetch_categorylinks(wikitext):
    categories = fetch_categories(wikitext)
    categorylinks = [categories]
    while categories:
        for category in categories:
            titles = u'Category:{0}'.format(category)
            wikitext = fetch_wikitext(
                u"http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles={0}&format=json".format(
                    titles))
            categories = fetch_categories(wikitext)
            categorylinks += categories
    return categorylinks

def parse_pic(wikitext):
    pic_list = []
    pattern = r'(\[\[File:(.*)]])'
    for match in re.findall(pattern, wikitext):
        # print match[0]
        pic_name = match[1].split("|")[0]
        # print pic_name
        pic_dict = {"name": pic_name.strip(),
                    "wikitext": match[0]}
        pic_list.append(pic_dict)

    return pic_list

def fetch_piclinks(wikitext):
    pic_list = parse_pic(wikitext)
    #pprint(pic_list)

    allpics = []
    #r = requests.get("http://localhost/mediawiki/api.php?action=query&list=allimages&pageids=2&format=json")
    r = requests.get("http://localhost/mediawiki/api.php?action=query&list=allimages&pageids=5&format=json")
    decode_json = json.loads(r.text)
    allimages = decode_json["query"]["allimages"]
    for pic in pic_list:
        for image in allimages:
            if pic["name"] == image["name"].strip():
                pic["url"] = "[{0} {1}]".format(image["url"], pic["name"])
                allpics.append(pic)
    #pprint(allpics)
    return allpics

def fetch_allcategories_from_root(categoryname_list, result):
    if len(categoryname_list) == 0: return result
    for categoryname in categoryname_list:
        r = requests.get(
            u"http://localhost/mediawiki/api.php?action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:{0}&format=json".format(categoryname))
        decode_json = json.loads(r.text)
        categorymembers = decode_json["query"]["categorymembers"]

        subcategory_list = []
        if len(categorymembers) != 0:
            for categorymember in categorymembers:
                subcategory = categorymember["title"][9:]
                subcategory_list.append(subcategory)
            result.append(subcategory_list)

        return fetch_allcategories_from_root(subcategory_list, result)




if __name__ == "__main__":
    # wikitext = fetch_wikitext(
    #     "http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles=HelloWorld&format=json")
    titles = u'放了支架不代表“万事大吉”'
    wikitext = fetch_wikitext(u"http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles={0}&format=json".format(titles))
    print "======format: wikitext====="
    print wikitext
    print "======format: html========="
    print parselite(wikitext)

    print "======all images==========="
    allpics = fetch_piclinks(wikitext)
    pprint(allpics)

    print "======wikitext after changed====="
    for pic in allpics:
        wikitext = wikitext.replace(pic["wikitext"], pic["url"])
    print wikitext

    print "======html after changed========="
    print parselite(wikitext)


    print fetch_allcategories_from_root(["Categories"], ["Categories"])

    print fetch_categories(wikitext)

    print fetch_categorylinks(wikitext)













