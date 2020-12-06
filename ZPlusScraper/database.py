from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

TABLES = {}
TABLES['articles'] = (
    "CREATE TABLE `articles` ("
    "  `id` bigint(20) NOT NULL AUTO_INCREMENT,"
    "  `created` date NOT NULL,"
    "  `last_modified` date NOT NULL,"
    "  `title` varchar(500) NOT NULL,"
    "  `href` varchar(200) NOT NULL,"
    "  `article_html` MEDIUMTEXT ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['scrape_run'] = (
    "CREATE TABLE `scrape_run` ("
    "  `id` bigint(20) NOT NULL AUTO_INCREMENT,"
    "  `created` date NOT NULL,"
    "  `datazplus` varchar(20),"
    "  `article_id` bigint(20) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  Foreign Key(`article_id`) references articles(`id`)"
    ") ENGINE=InnoDB")


def create_database(context, db_name):
    cursor = context.cursor()

    try:
        cursor.execute(f"USE {db_name}")
    except mysql.connector.Error as err:
        print(f"Database {db_name} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
            print(f"Database {db_name} created successfully.")
            context.database = db_name
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
