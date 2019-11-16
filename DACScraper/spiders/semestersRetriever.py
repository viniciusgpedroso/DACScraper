# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re

# XPATH
XPATH_EMPHASIS = "//h1/text()"
XPATH_COURSE = "//h2[contains(text(), 'Curso')]"

# REGEX
REGEX_EMPHASIS_DETECTOR = "[A-Z]{1,2} -"

class SemestersretrieverSpider(scrapy.Spider):
    name = 'semestersRetriever'
    sample_urls = ['https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2018/proposta/sug34.html',
        'https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2018/proposta/sug11.html']

    def __init__(self, urls=sample_urls, filename=None, **kwargs):
        
        if filename:
            logging.info(f"Loading '{filename}'")
            f = open(filename)
            data = json.loads(f.read())
            # save numbers and save urls
            self.courses_lists = data
            urls = self.build_proposal_urls(self.courses_lists)
            f.close()
        else:
            urls = self.sample_urls
        
        self.urls = urls

    def build_proposal_urls(self, courses_list):
        """Build urls from first year to last year (inclusive)

        Args:
            courses_list (list of dics with year and courses_list attr): 
                list of valid courses numbers for a given year

        Returns:
            list of urls in the format
            https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo{YEAR}/proposta/sug{CODE}.html
        """
        preffix = "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo"
        after_year = "/proposta/sug"
        after_course = ".html"
        urls = []
        for courses_year in courses_list:
            year = courses_year['year']
            for course in courses_year["courses_list"]:
                urls.append(preffix + year + after_year + str(course) + after_course)

        print("URLS:")
        return urls

    def start_requests(self):
        print("Empty start requests")
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Checks if the course has multiple emphasis
        possible_emphasis = response.xpath(XPATH_EMPHASIS).getall()
        if possible_emphasis:
            emphasis = False
            for e in possible_emphasis:
                if re.findall(REGEX_EMPHASIS_DETECTOR, e):
                    emphasis = True
                    break
        if emphasis:
            self.parse_with_emphasis(response)
        else:
            self.parse_without_emphasis(response)
