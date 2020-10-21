# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import CourseItem
import DACScraper.constants as cnst


class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'

    # http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/
    sample_urls = ["https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0034/0034.html"]

    def __init__(self, urls=sample_urls, filename=None, **kwargs):
        if filename:
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            data = json.loads(f.read())
            f.close()
            data_urls = []
            for t in data:
                data_urls.append(t['url'])
            self.urls=data_urls
        else:
            self.urls = urls

    def start_requests(self):

        for url in self.urls:
            item = CourseItem()
            
            item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, url)[0]
            
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request

    def parse(self, response):
        item = response.meta['item']

        parents_selectors = response.xpath(cnst.XPATH_PARENT)
        # Remove "Disciplinas"
        parents_selectors.pop(0)

        for selector in parents_selectors:
            title = selector.xpath(cnst.XPATH_TITLE).get()
            codes = selector.xpath(cnst.XPATH_CODES).get()
            syllabus = selector.xpath(cnst.XPATH_SYLLABUS).get()
            
            item['id'] = re.findall(cnst.REGEX_ID, title)[0]
            item['title'] = re.findall(cnst.REGEX_TITLE, title)[0].strip()
            item['codes'] = re.findall(cnst.REGEX_CODE, codes)[0].strip()
            item['syllabus'] = syllabus.strip()
            item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, response.url)[0]
            req = re.findall(cnst.REGEX_PRE_REQ, codes)
            if req:
                item['requirement'] = self.processPreReqs(req[0].strip())
            else:
                item['requirement'] = None
            yield item

    def processPreReqs(self, reqsString):
        """
        Returns a list of lists containing the
        necessary pre-requisites for each course
        """
        if (not reqsString):
            logging.info("Empty pre-requisites string")
            pass

        reqs_list = []

        # multiple pre-requisites
        if ("/" in reqsString):
            for reqs in reqsString.split("/"):
                reqs_list.append(re.findall(cnst.REGEX_ID, reqs))

        else:
            reqs_list.append(re.findall(cnst.REGEX_ID, reqsString))
        return reqs_list
