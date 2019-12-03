# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DacscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CourseItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    requirement = scrapy.Field()
    syllabus = scrapy.Field()
    codes = scrapy.Field()

class CourseIdURLItem(scrapy.Item):
    url = scrapy.Field()
    year = scrapy.Field()

class CourseListItem(scrapy.Item):
    year = scrapy.Field()
    courses_list = scrapy.Field()

class SemestersItem(scrapy.Item):
    id = scrapy.Field()
    code = scrapy.Field()
    emphasis = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()
    semesters = scrapy.Field()
    text_electives = scrapy.Field()
