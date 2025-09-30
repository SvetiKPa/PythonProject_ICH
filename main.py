import os
import dotenv
from pathlib import Path
import pymysql
import main_film_search
from pymongo import MongoClient
import log_writer
import statistic_report
import formatter
import datetime

def main():
    dotenv.load_dotenv(Path('.env'))
    dbconfig = {'host': os.environ.get('MYSQL_HOST'),
                'port': int(os.environ.get('MYSQL_PORT', 3306)),
                'user': os.environ.get('MYSQL_USER'),
                'password': os.environ.get('MYSQL_PASSWORD'),
                'database': os.environ.get('MYSQL_DB'),
                }

    client    = MongoClient(os.environ.get('MONGO_URI'))
    db        = client[os.environ.get('MONGO_DB')]
    statistic_collection = db[os.environ.get('MONGO_COLLECTION')]


    with pymysql.connect(**dbconfig) as connection:
        cursor = connection.cursor()
        while True:
            print("=" * 50)
            print("--- Search Film from DB Sakila ---")
            print("=" * 50)
            print("1. Search name of films")
            print("2. Search category of films")
            print("3. Popular or last query")
            print("0. Exit")
            print("-" * 50)
            choice = input("Выберите действие (0-3): ").strip()

            if choice == "1":
                while True:
                    print("Enter name of films: ")
                    result = main_film_search.search_by_keyword(cursor)
                    if result is None:
                        print("Поиск отменен")
                    else:
                        try:
                            log_writer.load_statistic(statistic_collection, result)
                        except ValueError as e:
                            print("ERROR")
                    res = input("Сделать еще один поиск по названию? Y/N: ").strip().lower()
                    if res in ['n', 'т', 'no', 'нет']:
                        break
            elif choice == "2":
                while True:
                    print("Enter category of films: ")
                    result = main_film_search.search_by_category_year(cursor)
                    if result is None:
                        print("Поиск отменен")
                    else:
                        try:
                            log_writer.load_statistic(statistic_collection, result)
                        except ValueError as e:
                            print("ERROR")
                    res = input("Сделать еще один поиск по категории? Y/N: ").strip().lower()
                    if res in ['n', 'т', 'no', 'нет']:
                        break
            elif choice == "3":
                statistic_report.report_popular_keywords(statistic_collection, "keyword", limit=10)
                print('-'*70)
                statistic_report.report_popular_keywords(statistic_collection, "category")
                res = input("Показать другие отчеты? (Y/N): ").strip().lower()
                if res in ['y', 'д', 'yes', 'да']:
                    statistic_report.report_unique_searches(statistic_collection, limit=3)
            elif choice == "0":
                print("Goodbye! See you again!")
                cursor.close()
                client.close()
                break
            else:
                print("\n INVALID CHOICE! TRY AGAIN!")


if __name__ == "__main__":
    main()