#!/usr/bin/env python

import requests

import json

from wikimarkup import parselite

if __name__ == "__main__":
	r = requests.get("http://localhost/mediawiki/api.php?action=query&prop=revisions&rvprop=content&titles=HelloWorld&format=json")
	decode_json = json.loads(r.text)
	wikitext = decode_json["query"]["pages"]["2"]["revisions"][0]["*"]
	print "======format: wikitext====="
	print wikitext
	print "======format: html========="
	print parselite(wikitext)
	
	

