# -*- coding: utf-8 -*-
from abc import ABC

import scrapy
import re
from DACScraper.items import CourseListItem
import DACScraper.constants as cnst


class SemestersListerSpider(scrapy.Spider):
    """
    Spider to list all the 'majors' codes and add to CourseListItem objects.
    """
    name = 'semestersLister'

    def __init__(self, first_year=cnst.FIRST_YEAR, last_year=cnst.LAST_YEAR, **kwargs):
        """
        Initializes the catalog urls in the range from 'first_year' and 'last_year' using build_urls.
        :param first_year:  first_year of the catalog to be used to generate the urls, oldest year supported: 2013.
        :param last_year:   last_year of the catalog to be used to generate the urls
        """
        super().__init__(**kwargs)
        self.urls = self.build_urls(first_year, last_year)

    @staticmethod
    def build_urls(first_year: str, last_year: str):
        """
        Builds the catalog urls in the range 'first_year' to 'last_year'
        :param first_year:  with a valid catalog year in the {XXXX} format
        :param last_year:   with valid catalog year in the {XXXX} format
        :return:            an empty list if last_year < first_year,
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
        """
        Starts requests using the urls from 'self.urls' list.
        :return: scrapy.http.requests to be parsed
        """
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse_course_list)

    @staticmethod
    def parse_course_list(response):
        """
        Parses the response and yields CourseListItem objects
        :param response:    response from the url of each 'major'
        :return:            filled CourseListItem object
        """
        item = CourseListItem()
        item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, response.url)[0]

        courses_list = []
        courses_codes = response.xpath(cnst.XPATH_COURSE_CODE).getall()
        for i in range(len(courses_codes)):
            courses_list.append(int(courses_codes[i]))
        courses_list.sort()
        item['courses_list'] = courses_list
        yield item
