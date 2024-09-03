import json
import re
import sqlite3
import settings

class DBController():

    def __init__(self, link, alias, host, user, port, password):
        self.link = link
        self.alias = alias
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.connection = None
        self.vector_db = None
        self.level_dbs = None
        self.conn = None
        self.cursor = None

    def assign_db(self,vector_db,level_dbs):
        self.vector_db = vector_db
        self.level_dbs = level_dbs

    def connect(self):
        """
        connect to db

        :return: a status that indicates
            0 not connected to db
            1 if all connection to db are success
        """

        try:
            self.connection = sqlite3.connect(self.alias)
            self.cursor = self.connection.cursor()
            print("Connected to DB server")

            return True
        except Exception as e:
            print(f"Failed to connect to DB server: {e}")
            return False

    def disconnect(self) -> bool:
        """
        disconnect from db

        :return:status that indicates
            False failed disconnect
            True successful disconnect
        """
        try:
            self.connection.close()
        except Exception as e:
            return False

        return True

    def fetch_per_batch(self, query: str, batch_size: int = 1000) -> list:
        """
        perform query to database, and retrieve data per batch

        :param query: SQL Quert
        :param batch_size: num data per batch
        :return: sorted ranked text embedding
        """
        pass

    def text_rank(self, retrieved: list) -> list:
        """
        rank retrieved query from annoy search

        :param retrieved:  retrieved value from annoy_search
        :return: sorted ranked text embedding
        """
        pass

    def create_db(self, db_name) -> bool:

        if not self.connection:
            if not self.connect():
                return False

        try:
            self.cursor.execute("PRAGMA database_list;")
            existing_dbs = self.cursor.fetchall()

            print("Existing databases:", existing_dbs)
            print("=========================================")

            if db_name in existing_dbs:
                print(f"Database '{db_name}' already exists")
                return True

            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()

            print(f"Database '{db_name}' created successfully")
            return True
        except Exception as e:
            print(f"Failed to create database: {e}")
            return False

    def use_db(self, db_name):

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        print("Successfully used DBManager")

    def purge_db(self,db_name):

        if not self.connection:
            if not self.connect():
                return False

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            cursor.execute(f"DELETE FROM {table[0]};")

        connection.commit()

    def get_vector_db(self,ids):
        # print(tuple(map(tuple,ids)))
        id_tuple = tuple(ids.tolist()[0])
        print(id_tuple)
        query = f"SELECT * FROM vector_table WHERE id IN {id_tuple}"
        self.cursor.execute(query)

        return self.cursor.fetchall()