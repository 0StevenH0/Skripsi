import pymilvus as m

class Connector():

    def __init__(self, link,alias, host, user, port,password):
        self.link = link
        self.alias = alias
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.connection = False

    def connect(self,name):
        """
        connect to db

        :return: a status that indicates
            0 not connected to db
            1 if all connection to db are success
        """

        try:
            self.connection = m.connections.connect(
                alias=self.alias,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            print("Connected to Milvus server")
            return True
        except Exception as e:
            print(f"Failed to connect to Milvus server: {e}")
            return False

    def disconnect(self) -> int:
        """
        disconnect from db

        :return:status that indicates
            0 not connected to db
            1 connected to db
        """
        # TODO
        pass

    def fetch_per_batch(self, query: str, batch_size: int = 1000) -> list:
        """
        perform query to database, and retrieve data per batch

        :param query: SQL Quert
        :param batch_size: num data per batch
        :return: sorted ranked text embedding
        """
        # TODO
        pass

    def text_rank(self, retrieved: list) -> list:
        """
        rank retrieved query from annoy search

        :param retrieved:  retrieved value from annoy_search
        :return: sorted ranked text embedding
        """
        # TODO
        pass

    def create_db(self, db_name) -> bool:

        if not self.connection:
            if not self.connect(self.alias):
                return False

        try:
            existing_dbs = m.utility.list_database()
            print("Existing databases:", existing_dbs)
            print("=========================================")

            if db_name in existing_dbs:
                print(f"Database '{db_name}' already exists")
                return True

            m.utility.create_database(db_name)
            print(f"Database '{db_name}' created successfully")
            return True
        except Exception as e:
            print(f"Failed to create database: {e}")
            return False
