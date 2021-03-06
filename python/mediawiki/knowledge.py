#!/usr/bin/env python



import json, re

import requests
from wikimarkup import parselite

def fetch_wikitext(url):
	r = requests.get(url)
	decode_json = json.loads(r.text)
	wikitext = decode_json["query"]["pages"]["2"]["revisions"][0]["*"]
	return wikitext

if __name__ == "__main__":
	wikitext = fetch_wikitext("http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles=HelloWorld&format=json")
	print "======format: wikitext====="
	print wikitext
	print "======format: html========="
	print parselite(wikitext)

	picRegex = re.compile(r'[[File:(*) | *]]')
	matchObj = picRegex.search(wikitext)
	print matchObj.group(1)

	

	
	
	
	

