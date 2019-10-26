# -*- coding: utf-8 -*-
import scrapy

# XPATHS
XPATH_TITLE = "//div[@class='ancora']//a/text()"
XPATH_REQ = "//div[@class='ancora']/following-sibling::p/strong/text()"
XPATH_CODES = "//div[@class='ancora']/following-sibling::p[contains(text(), 'OF')]//text()"
XPATH_SYLLABUS = "//div[@class='ancora']//following-sibling::div[@class='justificado']//text()"


class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'
    allowed_domains = ['https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044']
    start_urls = ['http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/']

    def parse(self, response):
        pass
