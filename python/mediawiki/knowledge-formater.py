#!/usr/bin/env python



import json, re

import requests
from wikimarkup import parselite
from pprint import pprint


def fetch_wikitext(url):
    r = requests.get(url)
    decode_json = json.loads(r.text)
    wikitext = decode_json["query"]["pages"]["2"]["revisions"][0]["*"]
    return wikitext

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
    r = requests.get("http://192.168.1.12/mediawiki/api.php?action=query&list=allimages&pageids=2&format=json")
    decode_json = json.loads(r.text)
    allimages = decode_json["query"]["allimages"]
    for pic in pic_list:
        for image in allimages:
            if pic["name"] == image["name"].strip():
                pic["url"] = "[{0} {1}]".format(image["url"], pic["name"])
                allpics.append(pic)
    #pprint(allpics)
    return allpics

if __name__ == "__main__":
    wikitext = fetch_wikitext(
        "http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles=HelloWorld&format=json")
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















