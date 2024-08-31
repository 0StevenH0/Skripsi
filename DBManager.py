import json
import re

import pymilvus as m
from settings import Settings


class DBManager:
    def __init__(self):
        self.vector_db = None
        self.level_dbs = {f'level_{i}_db': None for i in range(0, 8)}

        self.setup_all_collections()
        self.load_collections()

    def get_vector_collection(self):
        fields = [
            m.FieldSchema(name="id", dtype=m.DataType.INT64, is_primary=True, auto_id=True),
            m.FieldSchema(name="vector", dtype=m.DataType.FLOAT_VECTOR, dim=settings.vector_dims),
            m.FieldSchema(name="text", dtype=m.DataType.VARCHAR, max_length=1000)
        ]

        fields.extend([
            m.FieldSchema(name=f"level_{i}", dtype=m.DataType.VARCHAR, max_length=100)
            for i in range(0, 8)
        ])

        schema = m.CollectionSchema(fields=fields, description="Vector Index")
        collection_name = "vector_db"
        collection = m.Collection(name=collection_name, schema=schema)

        # somehow bug
        # index_params = {
        #     "metric_type": settings.vector_metrics_type,
        #     "index_type": settings.vector_index_type,
        #     "params": settings.params
        # }
        index_params = {"index_type": "IVF_FLAT", "params": {"nlist": 256}, "metric_type": "L2"}
        collection.create_index(field_name="vector", index_params=index_params)

        self.vector_db = collection
        return collection

    def get_level_collection(self, level):
        schema = m.CollectionSchema(
            fields=[
                m.FieldSchema(name=f"level_{level}", dtype=m.DataType.VARCHAR, max_length=100, is_primary=True),
                m.FieldSchema(name="value", dtype=m.DataType.VARCHAR, max_length=1000),
                m.FieldSchema(name="dummy_vector", dtype=m.DataType.FLOAT_VECTOR, dim=2),
                m.FieldSchema(name="related_field",dtype=m.DataType.JSON)
            ],
            description=f"Level {level} Table, Treat like SQL"
        )

        collection_name = f"level_{level}_db"

        dummy_index_params = {
            "metric_type": "L2",
            "index_type": "FLAT",
            "params": {}
        }

        collection = m.Collection(name=collection_name, schema=schema)
        collection.create_index(field_name="dummy_vector", index_params=dummy_index_params)


        self.level_dbs[f'level_{level}_db'] = collection
        return collection

    def setup_all_collections(self):
        self.get_vector_collection()
        for i in range(0, 8):
            self.get_level_collection(i)

    def load_collections(self):
        self.vector_db.load()

    def flow_controller(self,header,level):
        """
            In A case where there are multiple same code within a level, decide which one to take

            e.g :
                multiple Accounting that are separated by school region // strata
            should traverse within multiple level

            the decision are made based on related_fields from level_n table
            the header should look like :
                - [1[code1]] [2[code2]] [3[code3]] [4[code4]] [5[code5]] [6[code6]] [7[code7]]
                - if level = 1, we wll use code1, level = 2, we will use code2, etc

            this function will check the value in related_fields from level_n table, if:
            - all value from json in related_fields appears on header : return this as the answer
            - if some value from json in related_fields
            appears on header, we will pick the one where the most value occurs, in case of multiple equal number
            of value occurs, take first one
            - if none, just return ""

            function should return ONLY 1 value, the value are get from text column of level_n table

            :return: string
        """

        level_code_pattern = rf"\[{level}\[([^\]]+)\]\]"
        level_code_match = re.search(level_code_pattern, header)
        if not level_code_match:
            return ""
        level_code = level_code_match.group(1)

        # Query the level_n collection for entries with this code
        level_collection = self.level_dbs[f'level_{level}_db']
        results = level_collection.query(
            expr=f"level_{level} == '{level_code}'",
            output_fields=[f"level_{level}", "value", "related_field"]
        )

        if not results:
            return ""

        # Extract all codes from the header
        all_codes = re.findall(r"\[\d+\[([^\]]+)\]\]", header)

        best_match = None
        max_match_count = -1

        for result in results:
            related_fields = json.loads(result['related_field'])
            match_count = 0

            for field, values in related_fields.items():
                field_level = int(field.split('_')[1])
                if field_level - 1 < len(all_codes):  # Check if the field level exists in the header
                    if all_codes[field_level - 1] in values:
                        match_count += 1

            if match_count > max_match_count:
                max_match_count = match_count
                best_match = result

        return best_match['value'] if best_match else ""


    def find_by_level_code(self,code):

        pass

    def create_relation(self):
        """
        Should be run after data are inserted, called by API; should do:
        - traverse vector_table then
        - find non-unique CODE in level 1 - 7 tables, then traverse back
        - for each non-unique CODE, input value to related_fields column
        e.g:
            looking for level 1 , in vector_db's text column:

            [1[a]] [2[b]] [3[c]]
            [1[a]] [2[d]] [3[c]]

            store in level_n:
                - [1[a]];text; {level_2 : [2[b]]}
                - [1[a]];text; {level_2 : [2[d]]}

        - no need to care about consistency, we can just populate based on id,
         so we pair earlier id from vector_table to earlier id from level_n table

        e.g :
            previously from level_n table:
            [1[a]];text1;null
            [1[a]];text2;null

        we can just look from vector_table where exact occurrences exist, then just repopulate level table like above

        :return: None
        """

        self.vector_db.load()
        for level_db in self.level_dbs.values():
            level_db.load()

        # Query all data from vector_db
        vector_data = self.vector_db.query(expr="id >= 0",
                                           output_fields=["id"] + [f"level_{i}" for i in range(1, 8)] + ["text"])

        # Process each level
        for level in range(1, 8):
            level_collection = self.level_dbs[f'level_{level}_db']
            level_field = f"level_{level}"

            # Group vector_data by level code
            level_groups = {}
            for item in vector_data:
                level_code = item[level_field]
                if level_code not in level_groups:
                    level_groups[level_code] = []
                level_groups[level_code].append(item)

            # Process each group
            for level_code, group in level_groups.items():
                if len(group) > 1:  # Non-unique code
                    for item in group:
                        related_fields = {f"level_{i}": [] for i in range(1, 8) if i != level}
                        for related_item in group:
                            if related_item['id'] != item['id']:
                                for i in range(1, 8):
                                    if i != level:
                                        related_fields[f"level_{i}"].append(related_item[f"level_{i}"])

                        # Remove empty lists and convert to JSON
                        related_fields = {k: v for k, v in related_fields.items() if v}
                        related_fields_json = json.dumps(related_fields)

                        # Update the level collection
                        level_collection.upsert([
                            [level_code],  # level_{level}
                            [item['text']],  # value
                            [[0, 0]],  # dummy_vector
                            [related_fields_json]  # related_field
                        ])

        print("Relations created successfully.")

    def search(self,search_vector):

        search_params = {"metric_type": settings.vector_metrics_type, "params": {"nprobe": 10}}

        output_fields = ["text"] + [f"level_{i}" for i in range(8)]

        results = self.vector_db.search(
            data=search_vector,
            anns_field="vector",
            param=search_params,
            limit=5,
            expr=None,
            output_fields=output_fields
        )

        processed_results = []
        for hit in results[0]:
            processed_hit = {
                "id": hit.id,
                "distance": hit.distance,
                "text": hit.entity.get('text'),
            }
            for level in range(8):
                field_name = f"level_{level}"
                processed_hit[field_name] = hit.entity.get(field_name)

            processed_results.append(processed_hit)

        return processed_results

settings = Settings()
