# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import CourseItem

# XPATHS
XPATH_TITLE = "//div[@class='ancora']//a/text()"
XPATH_CODES = "//div[@class='ancora']//following-sibling::p[1]"
XPATH_SYLLABUS = "//div[@class='ancora']//following-sibling::div[@class='justificado']//p/text()"

# REGEX
REGEX_CATALOG_YEAR = 'catalogo([0-9]{4})'
REGEX_PRE_REQ = '<strong>Pré-Req.: <\/strong>(.*)<br>'
REGEX_SYLLABUS = '<strong>Ementa: .*?>(.*?)(<\/p>|<br>)'
REGEX_CODE = '(OF.*?)<br>'

class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'

    # file:///home/endsieg/Documents/MCsUnicamp.html
    # http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/
    sample_urls = ['file:///home/endsieg/Documents/MCsUnicamp.html']

    def __init__(self, urls=sample_urls, filename='', **kwargs):
        if (len(urls) == 0):
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            urls = json.loads(f.read())
            f.close()
        
        self.urls = urls

    def start_requests(self):

        for url in self.urls:
            item = CourseItem()
            
            item['year'] = re.findall(REGEX_CATALOG_YEAR, url)[0]
            #item['year'] = '2018' 
            
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request

    def parse(self, response):
        item = response.meta['item']

        titles = response.xpath(XPATH_TITLE).getall()
        codes = response.xpath(XPATH_CODES).getall()
        syllabus = response.xpath(XPATH_SYLLABUS).getall()

        for t, c, s in zip(titles, codes, syllabus):
            item['title'] = t.strip()
            item['codes'] = re.findall(REGEX_CODE, c)[0]
            item['syllabus'] = s.strip()
            req = re.findall(REGEX_PRE_REQ, c)
            if req:
                item['requirement'] = req[0].strip()
            else:
                item['requirement'] = None
            yield item
