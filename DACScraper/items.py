# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    """
    Item to store info about a single course
    id:             the course id
    title:          the course title
    year:           the catalog year that the course was extracted
    requirement:    the pre-requisites to attend this course
    syllabus:       the course syllabus
    codes:          the course codes - https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2020/legenda.html
    """
    id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    requirement = scrapy.Field()
    syllabus = scrapy.Field()
    codes = scrapy.Field()


class CourseIdURLItem(scrapy.Item):
    """
    Item to store url and year to be scraped
    url:    the url to be scraped
    year:   the catalog year that the course was extracted
    """
    url = scrapy.Field()
    year = scrapy.Field()


class CourseListItem(scrapy.Item):
    """
    Item year and list of courses to be scraped
    year:           the catalog year
    courses_list:   list of courses from that catalog year
    """
    year = scrapy.Field()
    courses_list = scrapy.Field()


class SemestersItem(scrapy.Item):
    """
    Item to store semesters info
    id:             the course id
    code:           the 'major' code
    emphasis:       the 'minor' code (if available)
    year:           the catalog year
    name:           the 'major' name
    semesters:      the courses, split into semesters, from that major
    text_electives: the elective courses info
    """
    id = scrapy.Field()
    code = scrapy.Field()
    emphasis = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()
    semesters = scrapy.Field()
    text_electives = scrapy.Field()
