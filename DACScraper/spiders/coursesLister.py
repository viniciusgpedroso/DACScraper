# -*- coding: utf-8 -*-
import scrapy

# XPATHS
XPATH_IDS = '//div[@class="div10b"]//@href'

class CourseslisterSpider(scrapy.Spider):
    name = 'coursesLister'
    allowed_domains = ['https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/TiposDisciplinas.html']
    start_urls = ['http://https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/TiposDisciplinas.html/']

    def parse(self, response):
        pass
