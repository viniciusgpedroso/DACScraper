# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
from DACScraper.items import CourseIdURLItem

# XPATHS
XPATH_IDS = '//div[@class="div10b"]//@href'

# REGEX
REGEX_CATALOG_YEAR = 'catalogo([0-9]{4})'

class CourseslisterSpider(scrapy.Spider):
    name = 'coursesLister'

    """
    1st Level: Obtains all div10b urls and follows link
    2nd Level: Obtains first div10b url and saves
    """
    sample_urls = ["https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/TiposDisciplinas.html"]

    def __init__(self, urls=sample_urls, filename='', **kwargs):
        """
        Initializes from sample_urls if not empty 
        or reads from json file with structure
        TODO estabilish url structure from file
        """
        if (len(urls) == 0):
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            data = json.loads(f.read())
            urls = data['urls']
            f.close()
        
        self.urls = urls
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.continue_requests)
    
    def continue_requests(self, response):
        """
        Requests for each course code prefix and callback to parse
        """
        for relative_url in response.xpath(XPATH_IDS).getall():
            item = CourseIdURLItem()
            item['year'] = re.findall(REGEX_CATALOG_YEAR, response.url)[0]
            url = response.urljoin(relative_url)
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request
    
    def parse(self, response):
        
        item = response.meta['item']
        relative_url = response.xpath(XPATH_IDS).get()
        url = response.urljoin(relative_url)
        item['url'] = url
        yield item