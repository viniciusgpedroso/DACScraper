# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import SemestersItem

# XPATH
XPATH_COURSE = "//h2[contains(text(), 'Curso')]/text()"
XPATH_EMPHASIS = "//h1/text()"
XPATH_SEMESTER = '//div[@class="div100"]//a[contains(text(), "(")]/text() | //div[@class="div100"]//text()[contains(., "Semestre")]'
XPATH_SEMESTER += ' | //div[@class="div100"]//text()[contains(., "eletivos")]'
# REGEX
REGEX_EMPHASIS_DETECTOR = "([A-Z]{1,3}) -"
REGEX_CATALOG_YEAR = 'catalogo([0-9]{4})'
REGEX_COURSE_CODE_FROM_PROPOSAL_URL = 'sug([0-9]{1,3})'
REGEX_COURSE_NAME = "Curso [0-9]{1,3} - (.*)"
REGEX_CREDITS_AMOUNT = "([0-9]{1,2}) Cr"
REGEX_NUMERIC_ONLY = "[^0-9]"
REGEX_REMOVE_PARENTHESES = r'\([^)]*\)'

# Constansts
FIRST_SEMESTER = "01° Semestre"
FIRST_SEMESTER_ALT = "01� Semestre"

class SemestersretrieverSpider(scrapy.Spider):
    name = 'semestersRetriever'
    #sample_urls = ['https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2018/proposta/sug34.html']
    sample_urls = ['file:///mnt/sda1/github/DACScraper/.scrapy/sug2catalogo2017.html',
                    'file:///mnt/sda1/github/DACScraper/.scrapy/sug48catalogo2013.html',
                    'file:///mnt/sda1/github/DACScraper/.scrapy/sug108catalogo2017.html',
                    'file:///mnt/sda1/github/DACScraper/.scrapy/sug11catalogo2018.html',
                    'file:///mnt/sda1/github/DACScraper/.scrapy/sug12catalogo2018.html',
                    'file:///mnt/sda1/github/DACScraper/.scrapy/sug34catalogo2018.html']

    # 'https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2018/proposta/sug11.html'

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
        emphasis = False
        if possible_emphasis:
            for e in possible_emphasis:
                if re.findall(REGEX_EMPHASIS_DETECTOR, e):
                    emphasis = True
                    break
        if emphasis:
            print("emphasis True")
            return self.parse_with_emphasis(response)
        else:
            return self.parse_without_emphasis(response)

    def parse_with_emphasis(self, response):
        """Parses courses with multiple emphasis

        Args:
            reponse (scrapy.response): response from the url of the course with
            multiple emphasis
        
        Returns:
            SemestersItem (scrapy.Item): item with information about the course
        """
        sems = response.xpath(XPATH_SEMESTER).getall()

        # Splits all emphasis semesters
        split_indexes = []
        for i in range(len(sems)):
            if FIRST_SEMESTER in sems[i] or FIRST_SEMESTER_ALT in sems[i]:
                split_indexes.append(i)
        emphasis_sems = [sems[i:j] for i,j in zip(split_indexes, split_indexes[1:]+[None])]
        emphasis_titles = response.xpath(XPATH_EMPHASIS).getall()

        num_emphasis = len(emphasis_titles)
        assert len(emphasis_sems) == num_emphasis
        
        print("emphasis_titles: " + str(emphasis_titles))
        # Builds an item for each emphasis
        for i in range(num_emphasis): 
            item = SemestersItem()
            item['year'] = re.findall(REGEX_CATALOG_YEAR, response.url)[0]
            item['code'] = re.findall(REGEX_COURSE_CODE_FROM_PROPOSAL_URL, response.url)[0]
            item['name'] = re.findall(REGEX_COURSE_NAME, response.xpath(XPATH_COURSE).get())[0]

            emp_code = re.findall(REGEX_EMPHASIS_DETECTOR, emphasis_titles[i])[0]
            item['id'] = item['code'] + "_" + emp_code + "_" + item['year']
            item['semesters'] = self.build_semesters_dict(emphasis_sems[i])
            yield item
        # TODO make request to gather data about electives
    
    def parse_without_emphasis(self, response):
        sems = response.xpath(XPATH_SEMESTER).getall()
        item = SemestersItem()
        item['year'] = re.findall(REGEX_CATALOG_YEAR, response.url)[0]
        item['code'] = re.findall(REGEX_COURSE_CODE_FROM_PROPOSAL_URL, response.url)[0]
        item['name'] = re.findall(REGEX_COURSE_NAME, response.xpath(XPATH_COURSE).get())[0]
        item['id'] = item['code'] + "_" + item['year']
        item['semesters'] = self.build_semesters_dict(sems)
        yield item

    def build_semesters_dict(self, emphasis_sem):
        semesters = []
        sem_atual = None
        for it in emphasis_sem: 
            if "Semestre" in it:
                if sem_atual:
                    semesters.append(sem_atual)
                creds = re.findall(REGEX_CREDITS_AMOUNT, it)[0]
                sem_atual = {"creditos": creds, "materias": []} 
            else:
                if "(" in it: 
                    materia = re.sub(REGEX_REMOVE_PARENTHESES, '', it)
                else:
                    materia = re.sub(REGEX_NUMERIC_ONLY, '', it) + " créditos eletivos"
                sem_atual["materias"].append(materia.strip())
        semesters.append(sem_atual)
        #print("build - semesters: " +str(semesters))
        s = {}
        for i in range(len(semesters)):
            s[str(i+1)] = semesters[i]
        
        return s

