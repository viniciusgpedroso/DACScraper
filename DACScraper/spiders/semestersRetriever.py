# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from DACScraper.items import SemestersItem
import DACScraper.constants as cnst


class SemestersRetrieverSpider(scrapy.Spider):
    """
    Spider to retrieve info about the 'majors' semesters and add to a 'SemestersItem' objects.
    """
    name = 'semestersRetriever'
    text_electives = []

    def __init__(self, filename: str, **kwargs):
        """
        Reads the urls from the filename

        :param filename: location of json file with an object with 'year' and 'courses_list' as keys.
        The 'courses_list' contains the code ids for each 'major' to be scraped.
        """
        super().__init__(**kwargs)
        logging.info(f"Loading '{filename}'")
        f = open(filename)
        data = json.loads(f.read())
        # save numbers and save urls
        self.courses_lists = data
        urls = self.build_proposal_urls(self.courses_lists)
        f.close()
        self.urls = urls

    @staticmethod
    def build_proposal_urls(courses_list: list):
        """
        Build urls from first year to last year (inclusive)

        :param courses_list:    (list of dicts with year and courses_list):
                                list of valid courses numbers for a given year
        :return:                list of urls in the format
                                https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo{YEAR}/proposta/sug{CODE}.html
        """
        preffix = "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo"
        after_year = "/proposta/sug"
        after_course = ".html"
        urls = []
        for courses_year in courses_list:
            year = courses_year['year']
            for course in courses_year["courses_list"]:
                urls.append("{}{}{}{}{}".format(preffix, year, after_year, course, after_course))

        return urls

    def start_requests(self):
        """
        Starts requests using the urls from 'self.urls' list.
        :return: scrapy.http.requests to be parsed
        """
        # Gets electives for all emphasis
        for url in self.urls:
            course_code = re.findall(cnst.REGEX_COURSE_CODE_FROM_PROPOSAL_URL, url)[0]
            course_year = re.findall(cnst.REGEX_CATALOG_YEAR, url)[0]
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """
        Parses the response from 'major' with and without 'minors'
        :param response:    scrapy.http.response objects
        :return:            scrapy.http.requests to parse electives info and a partially filled SemestersItem in meta
        """
        # Checks if the course has multiple emphasis
        possible_emphasis = response.xpath(cnst.XPATH_EMPHASIS).getall()
        emphasis = False
        if possible_emphasis:
            for e in possible_emphasis:
                if re.findall(cnst.REGEX_EMPHASIS_DETECTOR, e):
                    emphasis = True
                    break
        if emphasis:
            logging.info("emphasis True")
            return self.parse_with_emphasis(response)
        else:
            return self.parse_without_emphasis(response)

    def parse_with_emphasis(self, response):
        """
        Parses courses with multiple emphasis
        :param response:    response from the url of the course with multiple emphasis or 'minors'
        :return:            scrapy.http.request with a partially filled SemestersItem in meta
        """
        sems = response.xpath(cnst.XPATH_SEMESTER).getall()

        # Splits all emphasis semesters
        split_indexes = []
        for i in range(len(sems)):
            if cnst.FIRST_SEMESTER in sems[i] or cnst.FIRST_SEMESTER_ALT in sems[i]:
                split_indexes.append(i)
        emphasis_sems = [sems[i:j] for i, j in zip(split_indexes, split_indexes[1:] + [None])]
        emphasis_titles = response.xpath(cnst.XPATH_EMPHASIS).getall()

        num_emphasis = len(emphasis_titles)
        assert len(emphasis_sems) == num_emphasis

        logging.info('emphasis_titles: {}'.format(emphasis_titles))

        lst_electives = self.text_electives
        logging.info("lst_electives: {}".format(lst_electives))
        # Builds an item for each emphasis
        for i in range(num_emphasis):
            item = SemestersItem()
            self.fill_basic_semester_info(response, item)
            emp_code = re.findall(cnst.REGEX_EMPHASIS_DETECTOR, emphasis_titles[i])[0]
            item['emphasis'] = emp_code
            item['id'] = item['code'] + "_" + emp_code + "_" + item['year']
            item['semesters'] = self.build_semesters_dict(emphasis_sems[i])
            electives_url = self.get_electives_url(item['code'], item['year'])
            yield scrapy.Request(electives_url, callback=self.parse_electives, meta={'item': item, 'emp_index': i},
                                 dont_filter=True)

    @staticmethod
    def get_electives_url(course_code: str, year: str):
        """
        Build a list with each 'minor' emphasis into self.text_electives

        :param course_code: the code of the course (without emphasis)
        :param year:        the year of the course
        :return:            url for that 'minor' emphasis
        """
        url_prefix = "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo"
        url_before_code = "/curriculoPleno/cp"
        url_after_code = ".html"
        url = ('{}{}{}{}{}'.format(url_prefix, year, url_before_code, course_code, url_after_code))
        return url

    @staticmethod
    def parse_electives(response):
        """
        Parses courses electives and adds the data to self.text_electives

        :param response:    response from the url of the course with the electives text
        :return:            a filled SemestersItem object
        """
        xpath_electives_text = cnst.XPATH_ELECTIVES + "/text()"
        xpath_electives = xpath_electives_text + " | " + cnst.XPATH_ELECTIVES + cnst.XPATH_ELECTIVES_DATA + " | " + \
                          cnst.XPATH_ELECTIVES + cnst.XPATH_SUBJECTS

        electives_list = response.xpath(xpath_electives).getall()

        split_indexes = []
        for i in range(len(electives_list)):
            if cnst.ELECTIVES_DETECTOR in electives_list[i]:
                split_indexes.append(i)
            if '---' in electives_list[i]:
                electives_list[i] = "Qualquer Disciplina da Unicamp"
            if '\n' in electives_list[i]:
                electives_list[i] = re.sub('\\n', '', electives_list[i])

        text_electives = []
        lst_electives = [electives_list[i + 1:j] for i, j in zip(split_indexes, split_indexes[1:] + [None])]
        for group in lst_electives:
            single_text = ""
            for e in group:
                single_text += e + "\n"
            text_electives.append(single_text)

        item = response.meta['item']
        emp_ind = int(response.meta['emp_index'])

        item['text_electives'] = text_electives[emp_ind]
        yield item

    def parse_without_emphasis(self, response):
        """
        Parses courses without multiple emphasis
        :param response:    response from the url of the course
        :return:            scrapy.http.request with a partially filled SemestersItem in meta
        """
        sems = response.xpath(cnst.XPATH_SEMESTER).getall()
        item = SemestersItem()
        self.fill_basic_semester_info(response, item)
        item['id'] = item['code'] + "_" + item['year']
        item['semesters'] = self.build_semesters_dict(sems)
        item['emphasis'] = ""
        electives_url = self.get_electives_url(item['code'], item['year'])
        yield scrapy.Request(electives_url, callback=self.parse_electives, meta={'item': item, 'emp_index': 0},
                             dont_filter=True)

    @staticmethod
    def build_semesters_dict(emphasis_sem: list):
        """
        Builds an dictionary with the semesters info
        :param emphasis_sem:    list with all the semesters, credits and subjects in order
        :return:                dictionary with the semesters info
        """
        semesters = []
        sem_atual = None
        for it in emphasis_sem:
            if "Semestre" in it:
                if sem_atual:
                    semesters.append(sem_atual)
                creds = re.findall(cnst.REGEX_CREDITS_AMOUNT, it)[0]
                sem_atual = {"creditos": creds, "materias": []}
            else:
                if "(" in it:
                    materia = re.sub(cnst.REGEX_REMOVE_PARENTHESES, '', it)
                else:
                    materia = re.sub(cnst.REGEX_NUMERIC_ONLY, '', it) + " créditos eletivos"
                sem_atual["materias"].append(materia.strip())
        semesters.append(sem_atual)
        s = {}
        for i in range(len(semesters)):
            s[str(i + 1)] = semesters[i]

        return s

    @staticmethod
    def fill_basic_semester_info(response, item: SemestersItem):
        """
        Partially fills a 'SemestersItem' object with basic info, 'year', 'code' and 'name'.

        :param response:    scrapy.http.response with the info to fill the item
        :param item:        to be filled with year, 'major' code and 'major' name
        """
        item['year'] = re.findall(cnst.REGEX_CATALOG_YEAR, response.url)[0]
        item['code'] = re.findall(cnst.REGEX_COURSE_CODE_FROM_PROPOSAL_URL, response.url)[0]
        item['name'] = re.findall(cnst.REGEX_COURSE_NAME, response.xpath(cnst.XPATH_COURSE).get())[0]
