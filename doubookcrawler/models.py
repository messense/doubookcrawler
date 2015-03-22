# -*- coding: utf-8 -*-
import os
import sys

if __name__ == '__main__':
    curr_path = os.path.abspath(os.path.dirname(__file__))
    proj_path = os.path.dirname(curr_path)
    sys.path.append(proj_path)

import scrapy

from doubookcrawler.settings import db_conn


class BaseModel(object):
    _table = ''
    _fields = ''

    @classmethod
    def get_cursor(cls):
        return db_conn.cursor(), db_conn

    @classmethod
    def close_cursor(cls, cursor):
        cursor.close()

    @classmethod
    def create_table(cls):
        raise NotImplementedError()


class Book(BaseModel):
    _table = 'book'
    _fields = 'id,title,author,rating'

    @classmethod
    def upsert_book(cls, book):
        if isinstance(book, scrapy.Item):
            book = dict(book)
        sql = """REPLACE INTO {table}({fields}) VALUES(
            %(id)s,%(title)s,%(author)s,%(rating)s
        )""".format(table=cls._table, fields=cls._fields)
        cursor, conn = cls.get_cursor()
        cursor.execute(sql, book)
        conn.commit()
        cls.close_cursor(cursor)

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS {table}(
        id BIGINT NOT NULL PRIMARY KEY,
        title VARCHAR(256) NOT NULL,
        author VARCHAR(128) NOT NULL,
        rating FLOAT NOT NULL DEFAULT 0,
        INDEX(rating),
        INDEX(author)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """.format(table=cls._table)
        cursor, conn = cls.get_cursor()
        cursor.execute(sql)
        conn.commit()
        cls.close_cursor(cursor)


class Rating(BaseModel):
    _table = 'rating'
    _fields = 'book_id,user,rating,vote'

    @classmethod
    def upsert_rating(cls, rating):
        if isinstance(rating, scrapy.Item):
            rating = dict(rating)
        sql = """REPLACE INTO {table}({fields}) VALUES(
            %(book_id)s,%(user)s,%(rating)s,%(vote)s
        )""".format(table=cls._table, fields=cls._fields)
        cursor, conn = cls.get_cursor()
        cursor.execute(sql, rating)
        conn.commit()
        cls.close_cursor(cursor)

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS {table} (
        id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        book_id BIGINT NOT NULL,
        user VARCHAR(128) NOT NULL,
        rating FLOAT NOT NULL,
        vote INT NOT NULL DEFAULT 0,
        UNIQUE(book_id, user),
        INDEX(rating),
        INDEX(vote)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        """.format(table=cls._table)
        cursor, conn = cls.get_cursor()
        cursor.execute(sql)
        conn.commit()
        cls.close_cursor(cursor)


if __name__ == '__main__':
    Book.create_table()
    Rating.create_table()
