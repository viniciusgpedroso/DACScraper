# -*- coding: utf-8 -*-
import scrapy


class CoursesretrieverSpider(scrapy.Spider):
    name = 'coursesRetriever'
    allowed_domains = ['https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044']
    start_urls = ['http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044/']

    def parse(self, response):
        pass
