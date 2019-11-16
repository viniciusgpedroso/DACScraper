# -*- coding: utf-8 -*-
import scrapy


# Constants
FIRST_YEAR = "2012" # Previous catalogs do not have the same structure

class SemesterslisterSpider(scrapy.Spider):
    name = 'semestersLister'
    sample_urls = ['http://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2012/cursos.html/']

    def __init__(self, last_year="2012", **kwargs):
        """
        Initializes from sample_urls if not empty 
        or reads from json file with structure
        """
        self.urls = self.build_urls(FIRST_YEAR, last_year)

    def parse(self, response):
        pass

    def build_urls(self, first_year, last_year):
        """Build urls from first year to last year (inclusive)

        Args:
            first_year (str): valid catalog year in the {XXXX} format
            last_year (str): valid catalog year in the {XXXX} format

        Returns:
            if last_year < first_year, returns an empty list
            else, a list with catalog urls from first year to last year
        """

        prefix = "http://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo"
        suffix = "/cursos.html/"

        last = int(last_year)
        first = int(first_year)
        if last < first:
            return []
        
        urls = []
        for i in range(first_year, last_year + 1):
            urls.append(prefix + str(i) + suffix)
        
        return urls
