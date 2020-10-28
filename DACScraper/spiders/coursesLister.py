# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
from DACScraper.items import CourseIdURLItem
import DACScraper.constants as cnst


class CoursesListerSpider(scrapy.Spider):
    """
    Spider to list all courses urls for a catalog year and add to 'CourseIdURLItem'.
    """
    name = 'coursesLister'

    def __init__(self, filename: str):
        """
        Reads the urls from the filename

        :param filename: location of json file with an 'urls' key and an array of urls.
        """
        logging.info(f"Loading '{filename}'")
        f = open(filename)
        data = json.loads(f.read())
        self.urls = data['urls']
        self.urls_seen = set()
        f.close()
    
    def start_requests(self):
        """
        Starts requests using the urls from 'self.urls' list and obtains the '1st Level' - all div10b urls and callback
        to continue_requests

        :return: scrapy.http.requests to be parsed
        """
        for url in self.urls:
            yield scrapy.Request(url, callback=self.continue_requests)
    
    def continue_requests(self, response):
        """
        Start requests for each course code prefix and obtains the '2nd Level' - first div10b url, saves and
        callback to parse

        :param response:    scrapy.http.response objects
        :return:            scrapy.http.requests to be parsed
        """
        for relative_url in response.xpath(cnst.XPATH_IDS).getall():
            item = CourseIdURLItem()
            item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, response.url)[0]
            url = response.urljoin(relative_url)
            request = scrapy.Request(url, callback=self.parse)
            request.meta['item'] = item
            yield request
    
    def parse(self, response):
        """
        Parses the response and yields CourseIdItem objects

        :param response:    scrapy.http.response objects
        :return:            filled CourseIdItem object
        """
        item = response.meta['item']
        relative_url = response.xpath(cnst.XPATH_IDS).get()
        url = response.urljoin(relative_url).split('#')[0]  # Avoid duplicates
        if url not in self.urls_seen:
            self.urls_seen.add(url)
            item['url'] = url
            yield item
