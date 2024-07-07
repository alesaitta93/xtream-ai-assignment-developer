from decouple import config
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))


class DatabaseInfo:
    def __init__(self):
        self.url = config('DATABASE_URL', default="127.0.0.1", cast=str)
        self.usr = config('DATABASE_USERNAME', default="", cast=str)
        self.psw = config('DATABASE_PASSWORD', default="", cast=str)
        self.port = config('DATABASE_PORT', default=3306, cast=int)
        self.name = config('DATABASE_DIAMONDS', default="diamonds_db", cast=str)


database_info = DatabaseInfo()