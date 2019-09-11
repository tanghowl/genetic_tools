from pymongo import MongoClient
from genetic.log import logger
from genetic.settings import DATABASES


class MongoDB(object):

    def __init__(self):
        self.host = DATABASES['mongo']['host']
        self.port = int(DATABASES['mongo']['port'])
        self.usr = DATABASES['mongo']['user']
        self.passwd = DATABASES['mongo']['pwd']
        self.dbname = DATABASES['mongo']['db']
        self.table = DATABASES['mongo']['table']

    def __enter__(self):
        logger.info(f'Connect Mongo Use HOST:{self.host}, PORT:{self.port}, DB:{self.dbname}, TABLE:{self.table}')
        client = MongoClient(host=self.host,
                             port=self.port,
                             username=self.usr,
                             password=self.passwd)
        self._db = client[self.dbname][self.table]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_barcode_info(self, barcode):
        infos = self._db.find({'Barcode': {"$in": barcode}}).sort('Barcode')
        return infos
