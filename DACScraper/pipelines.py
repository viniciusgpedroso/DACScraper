# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import mysql.connector
from DACScraper.items import CourseItem, SemestersItem

class DacscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline(object):

    def open_spider(self, spider):
        # TODO add to settings
        self.cnx = mysql.connector.connect(user='demo', password='demo', host='127.0.0.1', database='dac_database')

    def process_item(self, item, spider):
        if isinstance(item, CourseItem):
            cursor = self.cnx.cursor()
            # Add to table materia
            add_curso = (" "
               "INSERT INTO materia (idmateria, year, title, codes, syllabus) "
               "VALUES (%s, %s, %s, %s, %s)")
            data_curso = (item['id'], item['year'], item['title'], item['codes'], item['syllabus'])
            cursor.execute(add_curso, data_curso)
            # Add to table reqs
            add_reqs = ("INSET INTO requirements "
               "(grupo, idmateria, req) "
               "VALUES (%s, %s, %s)")
            reqs = item['requirement']
            if reqs:
                group = 1
                for req in reqs:
                    for materia in req:
                        data_reqs = (group, materia, item['id'])
                        cursor.execute(add_reqs, data_reqs)
                    group += 1
            else:
                data_reqs = (item['id'], None, None)
                cursor.execute(add_reqs, data_reqs)
            self.cnx.commit()
            cursor.close()
        if isinstance(item, SemestersItem):
            logging.warning("SemesterItem not implemented in MySQLPipeline")

    def close_spider(self, spider):
        self.cnx.close()