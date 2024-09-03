import itertools
import json
import re

from settings import Settings


class DBManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.setup_all_collections(connection, cursor)

    def get_vector_collection(self, connection, cursor):
        create_table_query = '''
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
            level_7 VARCHAR(100)
        );
        '''

        cursor.execute(create_table_query)
        connection.commit()

    def get_level_collection(self, level, connection, cursor):
        cursor.execute(self.create_level_query(level))
        connection.commit()

    def setup_all_collections(self, connection, cursor):
        self.get_vector_collection(connection, cursor)
        for i in range(0, 8):
            self.get_level_collection(i, connection, cursor)

    def insert_to_vector_table(self, context, level,batch_size):
        """
        Inserts multiple rows into the vector_table in batches.
        :param batch_size: batch size per insert
        :param context: List of context texts
        :param level: Dictionary of level lists
        """
        query = '''
        INSERT INTO vector_table (
            text, 
            level_0, 
            level_1, 
            level_2, 
            level_3, 
            level_4, 
            level_5, 
            level_6, 
            level_7
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        # Prepare data for batch insert
        data = list(zip(
            context,
            level["level_0"],
            level["level_1"],
            level["level_2"],
            level["level_3"],
            level["level_4"],
            level["level_5"],
            level["level_6"],
            level["level_7"]
        ))

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

    # def flow_controller(self, header, level):
    #     """
    #         In A case where there are multiple same code within a level, decide which one to take
    #
    #         e.g :
    #             multiple Accounting that are separated by school region // strata
    #         should traverse within multiple level
    #
    #         the decision are made based on related_fields from level_n table
    #         the header should look like :
    #             - [1[code1]] [2[code2]] [3[code3]] [4[code4]] [5[code5]] [6[code6]] [7[code7]]
    #             - if level = 1, we wll use code1, level = 2, we will use code2, etc
    #
    #         this function will check the value in related_fields from level_n table, if:
    #         - all value from json in related_fields appears on header : return this as the answer
    #         - if some value from json in related_fields
    #         appears on header, we will pick the one where the most value occurs, in case of multiple equal number
    #         of value occurs, take first one
    #         - if none, just return ""
    #
    #         function should return ONLY 1 value, the value are get from text column of level_n table
    #
    #         :return: string
    #     """
    #
    #     level_code_pattern = rf"\[{level}\[([^\]]+)\]\]"
    #     level_code_match = re.search(level_code_pattern, header)
    #     if not level_code_match:
    #         return ""
    #     level_code = level_code_match.group(1)
    #
    #     # Query the level_n collection for entries with this code
    #     level_collection = self.level_dbs[f'level_{level}_db']
    #     results = level_collection.query(
    #         expr=f"level_{level} == '{level_code}'",
    #         output_fields=[f"level_{level}", "value", "related_field"]
    #     )
    #
    #     if not results:
    #         return ""
    #
    #     # Extract all codes from the header
    #     all_codes = re.findall(r"\[\d+\[([^\]]+)\]\]", header)
    #
    #     best_match = None
    #     max_match_count = -1
    #
    #     for result in results:
    #         related_fields = json.loads(result['related_field'])
    #         match_count = 0
    #
    #         for field, values in related_fields.items():
    #             field_level = int(field.split('_')[1])
    #             if field_level - 1 < len(all_codes):  # Check if the field level exists in the header
    #                 if all_codes[field_level - 1] in values:
    #                     match_count += 1
    #
    #         if match_count > max_match_count:
    #             max_match_count = match_count
    #             best_match = result
    #
    #     return best_match['value'] if best_match else ""
    #
    # def find_by_level_code(self, code):
    #
    #     pass
    #
    # def create_relation(self):
    #     """
    #     Should be run after data are inserted, called by API; should do:
    #     - traverse vector_table then
    #     - find non-unique CODE in level 1 - 7 tables, then traverse back
    #     - for each non-unique CODE, input value to related_fields column
    #     e.g:
    #         looking for level 1 , in vector_db's text column:
    #
    #         [1[a]] [2[b]] [3[c]]
    #         [1[a]] [2[d]] [3[c]]
    #
    #         store in level_n:
    #             - [1[a]];text; {level_2 : [2[b]]}
    #             - [1[a]];text; {level_2 : [2[d]]}
    #
    #     - no need to care about consistency, we can just populate based on id,
    #      so we pair earlier id from vector_table to earlier id from level_n table
    #
    #     e.g :
    #         previously from level_n table:
    #         [1[a]];text1;null
    #         [1[a]];text2;null
    #
    #     we can just look from vector_table where exact occurrences exist, then just repopulate level table like above
    #
    #     :return: None
    #     """
    #
    #     self.vector_db.load()
    #     for level_db in self.level_dbs.values():
    #         level_db.load()
    #
    #     # Query all data from vector_db
    #     vector_data = self.vector_db.query(expr="id >= 0",
    #                                        output_fields=["id"] + [f"level_{i}" for i in range(1, 8)] + ["text"])
    #
    #     # Process each level
    #     for level in range(1, 8):
    #         level_collection = self.level_dbs[f'level_{level}_db']
    #         level_field = f"level_{level}"
    #
    #         # Group vector_data by level code
    #         level_groups = {}
    #         for item in vector_data:
    #             level_code = item[level_field]
    #             if level_code not in level_groups:
    #                 level_groups[level_code] = []
    #             level_groups[level_code].append(item)
    #
    #         # Process each group
    #         for level_code, group in level_groups.items():
    #             if len(group) > 1:  # Non-unique code
    #                 for item in group:
    #                     related_fields = {f"level_{i}": [] for i in range(1, 8) if i != level}
    #                     for related_item in group:
    #                         if related_item['id'] != item['id']:
    #                             for i in range(1, 8):
    #                                 if i != level:
    #                                     related_fields[f"level_{i}"].append(related_item[f"level_{i}"])
    #
    #                     # Remove empty lists and convert to JSON
    #                     related_fields = {k: v for k, v in related_fields.items() if v}
    #                     related_fields_json = json.dumps(related_fields)
    #
    #                     # Update the level collection
    #                     level_collection.upsert([
    #                         [level_code],  # level_{level}
    #                         [item['text']],  # value
    #                         [[0, 0]],  # dummy_vector
    #                         [related_fields_json]  # related_field
    #                     ])
    #
    #     print("Relations created successfully.")
    #
    # def search(self, search_vector):
    #
    #     search_params = {"metric_type": settings.vector_metrics_type, "params": {"nprobe": 10}}
    #
    #     output_fields = ["text"] + [f"level_{i}" for i in range(8)]
    #
    #     results = self.vector_db.search(
    #         data=search_vector,
    #         anns_field="vector",
    #         param=search_params,
    #         limit=5,
    #         expr=None,
    #         output_fields=output_fields
    #     )
    #
    #     processed_results = []
    #     for hit in results[0]:
    #         processed_hit = {
    #             "id": hit.id,
    #             "distance": hit.distance,
    #             "text": hit.entity.get('text'),
    #         }
    #         for level in range(8):
    #             field_name = f"level_{level}"
    #             processed_hit[field_name] = hit.entity.get(field_name)
    #
    #         processed_results.append(processed_hit)
    #
    #     return processed_results

    def create_level_query(self, level):
        return f''' CREATE TABLE IF NOT EXISTS level_{level} (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            vector BLOB,                         
            text VARCHAR(2500),             
            level_{level} VARCHAR(100)
        );
        '''


settings = Settings()
