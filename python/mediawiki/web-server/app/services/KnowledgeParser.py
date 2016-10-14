#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json, re

import requests
from wikimarkup import parselite
from pprint import pprint


class KnowledgeParser(object):
    """
    parse content from MediaWiki
    """

    domain = u"http://localhost/mediawiki"

    def __init__(self):
        self.wikitext = ""
        self.id = 0
        self.title = ""

    def parse_bytitles(self, titles):
        fragment = u"&titles={0}".format(titles)
        return self.__parse(fragment)

    def parse_byid(self, id):
        fragment = u"&pageids={0}".format(id)
        return self.__parse(fragment)

    def __parse(self, fragment):
        content = KnowledgeParser.fetch_content(fragment)
        if content is None:
            return None
        else:
            self.id = content["id"]
            self.title = content["title"]
            self.wikitext = content["wikitext"]

        categorylinks = self.fetch_categorylinks()

        # remove the first pic and format the remaining pics
        allpics = self.__remove_first_pic()

        # remove category from wikitext
        self.__remove_categories()

        # wikitext -> html
        self.wikitext = self.wikitext.strip()
        body_html = parselite(self.wikitext)

        output = {
            "pic": allpics[0] if allpics else None,
            "title": self.title,
            "body": body_html,
            "categorylinks": categorylinks
        }

        return output

    def __remove_categories(self):
        category_list = KnowledgeParser.fetch_categories(self.wikitext)
        for i in range(len(category_list)):
            category = category_list[i]
            self.wikitext = self.wikitext.replace(category["wikitext"], "")

    def __remove_first_pic(self):
        allpics = self.fetch_piclinks()
        for i in range(len(allpics)):
            pic = allpics[i]
            if i == 0:
                self.wikitext = self.wikitext.replace(pic["wikitext"], "")
            else:
                self.wikitext = self.wikitext.replace(pic["wikitext"], pic["url"])
        return allpics

    def fetch_categorylinks(self):
        category_list = KnowledgeParser.fetch_categories(self.wikitext)
        categories = map(lambda x: x["name"], category_list)
        categorylinks = categories
        while categories:
            for category in categories:
                fragment = u'&titles=Category:{0}'.format(category)
                content = KnowledgeParser.fetch_content(fragment)
                categories = map(lambda x: x["name"], KnowledgeParser.fetch_categories(content["wikitext"]))
                categorylinks += categories
        return categorylinks

    def fetch_piclinks(self):
        pic_list = KnowledgeParser.parse_pic(self.wikitext)
        # pprint(pic_list)

        allpics = []
        r = requests.get(
            u"{0}/api.php?action=query&list=allimages&pageids={1}&format=json".format(KnowledgeParser.domain, self.id))
        decode_json = json.loads(r.text)
        allimages = decode_json["query"]["allimages"]
        for pic in pic_list:
            for image in allimages:
                if pic["name"] == image["name"].strip():
                    pic["url"] = image["url"]
                    allpics.append(pic)
        # pprint(allpics)
        return allpics

    @staticmethod
    def fetch_content(fragment):
        url = u"{0}/api.php?action=query&prop=revisions&rvprop=content&format=json".format(
            KnowledgeParser.domain) + fragment
        r = requests.get(url)
        decode_json = json.loads(r.text)
        content = {}
        try:
            content = {
                "id": decode_json["query"]["pages"].keys()[0],
                "title": decode_json["query"]["pages"].values()[0]["title"],
                "wikitext": decode_json["query"]["pages"].values()[0]["revisions"][0]["*"]
            }
        except KeyError, e:
            content = None
        return content

    @staticmethod
    def fetch_categories(wikitext):
        category_list = []
        pattern = r'(\[\[Category:(.*)]])'
        for match in re.findall(pattern, wikitext):
            # print match[0]
            category_dict = {
                "name": match[1],
                "wikitext": match[0]
            }
            category_list.append(category_dict)

        return category_list

    @staticmethod
    def parse_pic(wikitext):
        pic_list = []
        pattern = r'(\[\[File:(.*)]])'
        for match in re.findall(pattern, wikitext):
            pic_name = match[1].split("|")[0]
            pic_dict = {
                "name": pic_name.strip(),
                "wikitext": match[0]
            }
            pic_list.append(pic_dict)

        return pic_list

    @staticmethod
    def fetch_allcategories_from_root(categoryname_list, result):
        if len(categoryname_list) == 0: return result
        for categoryname in categoryname_list:
            r = requests.get(
                u"{0}/api.php?action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:{1}&format=json".format(
                    KnowledgeParser.domain,
                    categoryname))
            decode_json = json.loads(r.text)
            categorymembers = decode_json["query"]["categorymembers"]

            subcategory_list = []
            if len(categorymembers) != 0:
                for categorymember in categorymembers:
                    subcategory = categorymember["title"][9:]
                    subcategory_list.append(subcategory)
                result.append(subcategory_list)

            return KnowledgeParser.fetch_allcategories_from_root(subcategory_list, result)


if __name__ == "__main__":
    # titles = u'放了支架不代表“万事大吉”'
    # knowledge_parser = KnowledgeParser()
    #
    # pprint(knowledge_parser.parse_bytitles(titles))

    id = 5
    knowledge_parser = KnowledgeParser()
    pprint(knowledge_parser.parse_byid(id))
