import os
from pymongo import MongoClient
from dotenv import load_dotenv


# load enviroment variables from .env file
load_dotenv()


# get database host, database name and database port from enviroment variables
DATABASEHOST = os.environ["DATABASEHOST"] if "DATABASEHOST" in os.environ else "localhost"
DATABASENAME = os.environ["DATABASENAME"] if "DATABASENAME" in os.environ else "test_stackhubdb"


class BaseDB:
    __client = MongoClient(DATABASEHOST)
    db = __client[DATABASENAME]

    def set_database(self, name):
        self.db = self.__client[name]
