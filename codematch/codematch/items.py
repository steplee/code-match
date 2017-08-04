# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EditorialItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    all_text = scrapy.Field()

    difficulty = scrapy.Field()
    problem_summary = scrapy.Field()
    preqrequisites = scrapy.Field()
    explanation = scrapy.Field()
    solution_links = scrapy.Field()
class BriefItem(scrapy.Item):
    title = scrapy.Field()
    full_title = scrapy.Field()
    url = scrapy.Field()
    all_text = scrapy.Field()

    prompt = scrapy.Field()
    input = scrapy.Field()
    output = scrapy.Field()
    constraints = scrapy.Field()
    explanation = scrapy.Field()
