# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from DACScraper.items import CourseListItem
import DACScraper.constants as cnst


class SemesterslisterSpider(scrapy.Spider):
    name = 'semestersLister'

    def __init__(self, last_year="2020", **kwargs):
        """
        Initializes from sample_urls if not empty 
        or reads from json file with structure
        """
        self.urls = self.build_urls(cnst.FIRST_YEAR, last_year)

    def build_urls(self, first_year, last_year):
        """Build urls from first year to last year (inclusive)

        Args:
            first_year (str): valid catalog year in the {XXXX} format
            last_year (str): valid catalog year in the {XXXX} format

        Returns:
            if last_year < first_year, returns an empty list
            else, a list with catalog urls from first year to last year
        """
        prefix = "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo"
        suffix = "/cursos.html"

        last = int(last_year)
        first = int(first_year)
        if last < first:
            return []
        
        urls = []
        for i in range(first, last + 1):
            urls.append(prefix + str(i) + suffix)
        
        return urls
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        item = CourseListItem()
        item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, response.url)[0]

        courses_list = []
        courses_codes = response.xpath(cnst.XPATH_COURSE_CODE).getall()
        for i in range(len(courses_codes)):
            courses_list.append(int(courses_codes[i]))
        courses_list.sort()
        item['courses_list'] = courses_list
        yield item
