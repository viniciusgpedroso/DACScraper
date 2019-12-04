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
               "VALUES (%s, %s, %s, %s, %s) "
               "ON DUPLICATE KEY UPDATE idmateria=VALUES(idmateria), year=VALUES(year), "
               "title=VALUES(title), codes=VALUES(codes), syllabus=VALUES(syllabus)")
            data_curso = (item['id'], item['year'], item['title'], item['codes'], item['syllabus'])
            cursor.execute(add_curso, data_curso)
            self.cnx.commit()
            # Add to table reqs
            add_reqs = ("INSERT INTO requirements "
               "(grupo, idmateria, req) "
               "VALUES (%s, %s, %s) "
               "ON DUPLICATE KEY UPDATE grupo=VALUES(grupo), idmateria=VALUES(idmateria), req=VALUES(req)")
            reqs = item['requirement']
            if reqs:
                group = 1
                for req in reqs:
                    for materia in req:
                        data_reqs = (group, item['id'], materia)
                        cursor.execute(add_reqs, data_reqs)
                    group += 1
            else:
                data_reqs = (item['id'], 0, None)
                cursor.execute(add_reqs, data_reqs)
            self.cnx.commit()
            cursor.close()
        if isinstance(item, SemestersItem):
            cursor = self.cnx.cursor()
            # Add to table curso
            add_curso = (" "
               "INSERT INTO curso (idcurso, code, name, year, text_electives) "
               "VALUES (%s, %s, %s, %s, %s) "
               "ON DUPLICATE KEY UPDATE idcurso=VALUES(idcurso), code=VALUES(code), "
               "name=VALUES(name), year=VALUES(year), text_electives=VALUES(text_electives)")
            data_curso = (item['id'], item['code'], item['name'], item['year'], item['text_electives'])
            cursor.execute(add_curso, data_curso)
            self.cnx.commit()
            # Add to table semestres
            add_curso = (" "
               "INSERT INTO semestres (ind_semestre, materia, idcurso) "
               "VALUES (%s, %s, %s) "
               "ON DUPLICATE KEY UPDATE ind_semestre=VALUES(ind_semestre), materia=VALUES(materia), idcurso=VALUES(idcurso)")
            for s in item['semesters']:
                for m in item['semesters'][s]['materias']:
                    data_curso = (int(s), m, item['id'])
                    cursor.execute(add_curso, data_curso)
                    self.cnx.commit()
            cursor.close()

    def close_spider(self, spider):
        self.cnx.close()