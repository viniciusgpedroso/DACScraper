# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import CourseItem

# XPATHS
XPATH_PARENT = "//div[@class='ancora']"
XPATH_TITLE = "self::*//a/text()"
XPATH_CODES = "self::*//following-sibling::p[1]"
XPATH_SYLLABUS = "self::*//following-sibling::div[@class='justificado']//p/text() | self::*//following-sibling::div[@class='justificado']/text()"

# REGEX
REGEX_CATALOG_YEAR = 'catalogo([0-9]{4})'
REGEX_PRE_REQ = '<strong>Pré-Req.: <\/strong>(.*)<br>'
REGEX_SYLLABUS = '<strong>Ementa: .*?>(.*?)(<\/p>|<br>)'
REGEX_CODE = '(OF.*?)<br>'
REGEX_TITLE = '- (.*)'
REGEX_ID = '([A-Z]{2}[0-9]{1,3}|[A-Z] [0-9]{1,3})'

class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'

    # http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/
    sample_urls = ["https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2015/coordenadorias/0023/0023.html", "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2016/coordenadorias/0023/0023.html", "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2017/coordenadorias/0023/0023.html", "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2018/coordenadorias/0023/0023.html", "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0023/0023.html", "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2020/coordenadorias/0023/0023.html"]

    def __init__(self, urls=sample_urls, filename='', **kwargs):
        if (len(urls) == 0):
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            data = json.loads(f.read())
            urls = data['urls']
            f.close()
        
        self.urls = urls

    def start_requests(self):

        for url in self.urls:
            item = CourseItem()
            
            item['year'] = re.findall(REGEX_CATALOG_YEAR, url)[0] 
            
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request

    def parse(self, response):
        item = response.meta['item']

        parents_selectors = response.xpath(XPATH_PARENT)
        # Remove "Disciplinas"
        parents_selectors.pop(0)

        for selector in parents_selectors:
            title = selector.xpath(XPATH_TITLE).get()
            codes = selector.xpath(XPATH_CODES).get()
            syllabus = selector.xpath(XPATH_SYLLABUS).get()
            
            item['id'] = re.findall(REGEX_ID, title)[0] + "_" + str(item['year'])
            item['title'] = re.findall(REGEX_TITLE, title)[0].strip()
            item['codes'] = re.findall(REGEX_CODE, codes)[0].strip()
            item['syllabus'] = syllabus.strip()
            req = re.findall(REGEX_PRE_REQ, codes)
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

        reqsList = []

        # multiple pre-requisites
        if ("/" in reqsString):
            for reqs in reqsString.split("/"):
                reqsList.append(reqs.split())
        else:
            reqsList.append(reqsString.split())
        return reqsList