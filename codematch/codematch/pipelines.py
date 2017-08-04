# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from codematch.items import EditorialItem, BriefItem
import json,os
import pdb

class AssembleCodechefPipeline(object):
    def __init__(self):
        self.briefs = {}
        self.editorials = {}
        self.log_file = open("./data/codechef/_already_processed","a")

    def process_item(self, item, spider):
        title = item['title']
        if type(item) == EditorialItem:
            self.editorials[title] = item
        if type(item) == BriefItem:
            self.briefs[title] = item
        if title in self.briefs and title in self.editorials and title not in spider.already_processed:
            # Complete, store it!
            print("DONE WITH " + str(title))
            self.write_item(title)
            spider.already_processed.add(title)
            spider.num_success += 1

    def write_item(self, title):
        br = self.briefs[title]
        ed = self.editorials[title]
        d = {"title":title, "editorial":dict(ed), "brief":dict(br)}
        #pdb.set_trace()
        js = json.dumps(d)
        if os.path.exists("./data/codechef/"+title):
            print(" WARNING: %s file already processed !!!!"%title)
        else:
            with open("./data/codechef/"+title,"w") as f:
                f.write(js)
            self.log_file.write(title + "\n")

    def close_spider(self, spider):
        self.log_file.close()
