# -*- coding: utf-8 -*-
import scrapy
import logging
import json

# XPATHS
XPATH_TITLE = "//div[@class='ancora']//a/text()"
XPATH_REQ = "//div[@class='ancora']/following-sibling::p/strong/text()"
XPATH_CODES = "//div[@class='ancora']/following-sibling::p[contains(text(), 'OF')]//text()"
XPATH_SYLLABUS = "//div[@class='ancora']//following-sibling::div[@class='justificado']//text()"


class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'
    sample_urls = ['http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/']

    def __init__(self, urls=sample_urls, filename='', **kwargs):
        if (len(urls) == 0):
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            urls = json.loads(f.read())
            f.close()
        
        self.urls = urls

    def parse(self, response):
        pass
