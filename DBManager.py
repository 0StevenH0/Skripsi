import itertools
import json
import re

from RecordKeeper import Record
from settings import Settings


class DBManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.setup_all_collections(connection, cursor)

    def get_vector_collection(self, connection, cursor):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vector_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            text VARCHAR(1000),             
            level_0 VARCHAR(100),
            level_1 VARCHAR(100),
            level_2 VARCHAR(100),
            level_3 VARCHAR(100),
            level_4 VARCHAR(100),
            level_5 VARCHAR(100),
            level_6 VARCHAR(100),
            level_7 VARCHAR(100),
            val varchar(1000)
        );
        """

        cursor.execute(create_table_query)
        connection.commit()

    def get_level_collection(self, level, connection, cursor):
        cursor.execute(self.create_level_query(level))
        connection.commit()

    def setup_all_collections(self, connection, cursor):
        self.get_vector_collection(connection, cursor)
        self.get_multi_media_collection(connection, cursor)
        for i in range(0, 8):
            self.get_level_collection(i, connection, cursor)

    def insert_to_vector_table(self, context, level, batch_size):
        """
        Inserts multiple rows into the vector_table in batches.
        :param batch_size: batch size per insert
        :param context: List of context texts
        :param level: Dictionary of level lists
        """
        query = """
        INSERT INTO vector_table (
            text, 
            level_0, 
            level_1, 
            level_2, 
            level_3, 
            level_4, 
            level_5, 
            level_6, 
            level_7,
            val
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?);
        """

        # Prepare data for batch insert
        data = list(
            zip(
                context,
                level["level_0"],
                level["level_1"],
                level["level_2"],
                level["level_3"],
                level["level_4"],
                level["level_5"],
                level["level_6"],
                level["level_7"],
                level["val"],
            )
        )

        # Process in batches
        for batch in self.batch_generator(data, batch_size):
            try:
                self.cursor.executemany(query, batch)
                self.connection.commit()
            except Exception as e:
                print(f"SQLite error: {e}")
                self.connection.rollback()

    def batch_generator(self, iterable, batch_size):
        """
        Yield successive batch_size chunks from iterable.
        """
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, batch_size))
            if not batch:
                break
            yield batch

    def create_level_query(self, level):
        return f""" CREATE TABLE IF NOT EXISTS level_{level} (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            vector BLOB,                         
            text VARCHAR(2500)             
        );
        """

    def get_multi_media_collection(self, connection, cursor):
        create_table_query = f""" CREATE TABLE IF NOT EXISTS multi_media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,                          
            name VARCHAR(500),
            path VARCHAR(1000)             
        );
        """

        cursor.execute(create_table_query)
        connection.commit()

    @Record("query_construction.csv")
    def query_construction(self, merged_pairs):
        grouped = {}
        for text, pred in merged_pairs:
            grouped.setdefault(pred, []).append(text)

        conditions = []
        for pred, texts in grouped.items():
            if len(texts) > 1:
                or_conditions = " OR ".join(
                    f"level_{pred} = '{text}'" for text in texts
                )
                conditions.append(f"({or_conditions})")
            else:
                conditions.append(f"level_{pred} = '{texts[0]}'")

        where_clause = " AND ".join(conditions)
        query = f"WHERE {where_clause}"
        return query

    @Record("sql_retrieval.csv")
    def find_data(self, condition):
        create_table_query = f"""SELECT var FROM vector_table {condition}"""

        return self.cursor.execute(create_table_query)


settings = Settings()
