# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import CourseItem
import DACScraper.constants as cnst


class CoursesRetrieverSpider(scrapy.Spider):
    """
    Spider to retrieve info about courses and add to a 'CourseItem'
    """
    name = 'coursesRetriever'

    def __init__(self, filename: str):
        """
        Reads the urls from the filename

        :param filename: location of json file with an array of objects with 'url' and 'year' fields.
        """
        logging.info(f"Loading '{filename}'")
        f = open(filename)
        data = json.loads(f.read())
        f.close()
        self.urls = []
        for t in data:
            self.urls.append(t['url'])

    def start_requests(self):
        """
        Starts requests using the urls from 'self.urls' list.

        :return: scrapy.http.requests to be parsed
        """
        for url in self.urls:
            item = CourseItem()
            item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, url)[0]
            
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request

    def parse(self, response):
        """
        Parses the response and yields CourseItem objects

        :param response:    scrapy.http.response objects
        :return:            filled CourseItem object
        """
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
            req = re.findall(cnst.REGEX_PRE_REQ, codes)
            if req:
                item['requirement'] = self.process_pre_reqs(req[0].strip())
            else:
                item['requirement'] = None
            yield item

    @staticmethod
    def process_pre_reqs(reqs_string: str):
        """
        Process pre-requisites into a list for each course

        :param reqs_string: pre-requisites
        :return:            list of lists containing the necessary pre-requisites for each course
        """
        if not reqs_string:
            logging.info("Empty pre-requisites string")
            pass

        reqs_list = []

        # multiple pre-requisites
        if "/" in reqs_string:
            for reqs in reqs_string.split("/"):
                reqs_list.append(re.findall(cnst.REGEX_ID, reqs))

        else:
            reqs_list.append(re.findall(cnst.REGEX_ID, reqs_string))
        return reqs_list
