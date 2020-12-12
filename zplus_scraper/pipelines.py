from datetime import datetime

import mysql
from scrapy.exceptions import NotConfigured

from database import create_database


class ZplusscraperPipeline:
    def process_item(self, item, spider):
        return item


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:  # if we don't define db config in settings
            raise NotConfigured  # then raise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)  # returning pipeline instance

    def open_spider(self, spider):
        print('open spider was called. Initializing database')
        self.context = mysql.connector.connect(
                                            user=self.user,
                                            passwd=self.passwd,
                                            host=self.host,
                                            charset='utf8mb4',
                                            use_unicode=True)
        create_database(self.context, self.db)

    def close_spider(self, spider):
        print('closing spider')
        self.context.close()

    def process_item(self, item, spider):
        existing_article = self.get_existing_article(item)
        if existing_article is None:
            article_id = self.save_article(item)
        else:
            article_id = existing_article[0]
            if item['datazplus'] is not None and item['article_html'] is not None:
                self.update_article(item)
        self.save_scrape_run(item, article_id)

        return item

    def get_existing_article(self, article):
        href = article['href']
        if href is None:
            return None

        cursor = self.context.cursor(buffered=True)
        sql_command = "SELECT id, title FROM articles WHERE href = %s"
        returned_rows = cursor.execute(sql_command, (href,))

        result = cursor.fetchone()
        cursor.close()
        return result

    def save_article(self, article):
        cursor = self.context.cursor(buffered=True)

        sql_command = """INSERT INTO articles (created, last_modified, title, href, article_html) 
                            VALUES (%s, %s, %s, %s, %s)"""
        str_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql_command, (str_now, str_now, article['title'], article['href'], article['article_html']))

        self.context.commit()
        row_id = cursor.lastrowid
        cursor.close()
        return row_id

    def update_article(self, article):
        cursor = self.context.cursor(buffered=True)

        sql_command = """UPDATE articles SET last_modified = %s, article_html = %s """
        str_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql_command, (str_now,  article['article_html']))

        self.context.commit()
        cursor.close()
        return None

    def save_scrape_run(self, article, article_id):
        cursor = self.context.cursor(buffered=True)

        sql_command = """INSERT INTO scrape_run (created, datazplus, article_id) 
                            VALUES (%s, %s, %s)"""
        str_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql_command, (str_now, article['datazplus'], article_id))

        self.context.commit()
        cursor.close()
        return None
