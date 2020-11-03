# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import mysql.connector
from DACScraper.items import CourseItem, SemestersItem
from DACScraper.settings import dac_pwd, dac_user, database_name, dac_host


class MySQLPipeline(object):
    """
    Pipeline to process items and add to a database using the credentials in settings.
    """

    def __init__(self):
        """
        Initializes connection with mysql database using the credentials in settings.
        """
        self.cnx = mysql.connector.connect(user=dac_user, password=dac_pwd, host=dac_host, database=database_name)

    def process_item(self, item, spider):
        """
        Process 'CourseItem' and 'SemestersItem' objects and add data to mysql database.
        :param item:    object with 'CourseItem' or 'SemestersItem' data
        :param spider:
        """
        if isinstance(item, CourseItem):
            self.process_course_item(item)
        elif isinstance(item, SemestersItem):
            self.process_semesters_item(item)
        else:
            return item

    def process_course_item(self, item):
        """
        Process 'CourseItem' objects and add data to the tables 'materia' and 'requirements'.

        :param item:  object with 'CourseItem' data
        """
        cursor = self.cnx.cursor()
        # Add to table reqs
        self.add_subject(item, cursor)
        self.add_requirements(item, cursor)
        cursor.close()

    def add_subject(self, item, cursor):
        """
        Add subjects to table 'materia'.

        :param item:    object with 'CourseItem' data
        :param cursor:  mysql cursor
        """
        # Add to table materia
        add_curso = (" "
                     "INSERT INTO materia (idmateria, year, title, codes, syllabus) "
                     "VALUES (%s, %s, %s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE idmateria=VALUES(idmateria), year=VALUES(year), "
                     "title=VALUES(title), codes=VALUES(codes), syllabus=VALUES(syllabus)")
        data_curso = (item['id'], item['year'], item['title'], item['codes'], item['syllabus'])
        cursor.execute(add_curso, data_curso)
        self.cnx.commit()

    def add_requirements(self, item, cursor):
        """
        Add requirements to table 'requirements'

        :param item:    object with 'CourseItem' data
        :param cursor:  mysql cursor
        """
        add_reqs = ("INSERT INTO requirements "
                    "(grupo, idmateria, req, year, partial) "
                    "VALUES (%s, %s, %s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE grupo=VALUES(grupo), idmateria=VALUES(idmateria), req=VALUES(req), "
                    "year=VALUES(year), partial=VALUES(partial)")
        reqs = item['requirement']
        if reqs:
            group = 1
            for req in reqs:
                for materia in req:
                    partial = 0
                    if '*' in materia:
                        partial = 1
                        materia = materia.replace('*', '')

                    data_reqs = (group, item['id'], materia, item['year'], partial)
                    cursor.execute(add_reqs, data_reqs)
                group += 1
        else:
            partial = 0
            data_reqs = (0, item['id'], "Nenhum", item['year'], partial)
            cursor.execute(add_reqs, data_reqs)
        self.cnx.commit()

    def process_semesters_item(self, item):
        """
        Process 'SemestersItem' objects and add data to the tables 'curso' and 'semestres'.

        :param item:  object with 'SemestersItem' data
        """
        cursor = self.cnx.cursor()
        self.add_curso(item, cursor)
        self.add_semesters(item, cursor)
        cursor.close()

    def add_curso(self, item, cursor):
        """
        Add requirements to table 'curso'.

        :param item:    object with 'SemestersItem' data
        :param cursor:  mysql cursor
        """
        add_curso = (" "
                     "INSERT INTO curso (idcurso, code, name, year, emphasis, text_electives) "
                     "VALUES (%s, %s, %s, %s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE idcurso=VALUES(idcurso), code=VALUES(code), "
                     "name=VALUES(name), year=VALUES(year), emphasis=VALUES(emphasis), text_electives=VALUES(text_electives)")
        data_curso = (item['id'], item['code'], item['name'], item['year'], item['emphasis'], item['text_electives'])
        cursor.execute(add_curso, data_curso)
        self.cnx.commit()

    def add_semesters(self, item, cursor):
        """
        Add requirements to table 'semestres'.

        :param item:    object with 'SemestersItem' data
        :param cursor:  mysql cursor
        """
        add_curso = (" "
                     "INSERT INTO semestres (ind_semestre, materia, idcurso) "
                     "VALUES (%s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE ind_semestre=VALUES(ind_semestre), materia=VALUES(materia), idcurso=VALUES(idcurso)")
        for s in item['semesters']:
            for m in item['semesters'][s]['materias']:
                data_curso = (int(s), m, item['id'])
                cursor.execute(add_curso, data_curso)
                self.cnx.commit()

    def close_spider(self, spider):
        """
        Close the mysql connection when the spider closes

        :param spider: scrapy spider
        """
        self.cnx.close()

class MongoPipeline(object):
    """
    Pipeline to process items and add to a mongo database.
    """
