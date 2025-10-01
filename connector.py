import os
from pathlib import Path
import dotenv
import pymysql
from pymongo import MongoClient

dotenv.load_dotenv(Path('.env'))

client = MongoClient(os.environ.get('MONGO_URI'))
db = client[os.environ.get('MONGO_DB')]
collection = db[os.environ.get('MONGO_COLLECTION')]


def create_mysql_connection():
    """Создает подключение к MySQL"""
    dotenv.load_dotenv(Path('.env'))

    dbconfig = {
        'host': os.environ.get('MYSQL_HOST'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': os.environ.get('MYSQL_DB'),
    }

    required_params = ['host', 'user', 'password', 'database']
    for param in required_params:
        if not dbconfig[param]:
            raise ValueError(f"Отсутствует параметр MYSQL_{param.upper()}")

    try:
        connection = pymysql.connect(**dbconfig)
    except pymysql.OperationalError as e:
        print(f"Ошибка подключения к MySQL: {e}")
        return None

    return connection
