import pymilvus as m
from settings import Settings


class DBManager:
    def __init__(self):
        self.vector_db = None
        self.level_dbs = {f'level_{i}_db': None for i in range(1, 8)}

        self.setup_all_collections()


    def get_vector_collection(self):
        fields = [
            m.FieldSchema(name="id", dtype=m.DataType.INT64, is_primary=True, auto_id=True),
            m.FieldSchema(name="vector", dtype=m.DataType.FLOAT_VECTOR, dim=settings.vector_dims),
            m.FieldSchema(name="text", dtype=m.DataType.VARCHAR, max_length=1000)
        ]

        fields.extend([
            m.FieldSchema(name=f"level_{i}", dtype=m.DataType.VARCHAR, max_length=100)
            for i in range(1, 8)
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
        index_params = {"index_type": "IVF_FLAT", "params": {"nlist": 1024}, "metric_type": "L2"}
        collection.create_index(field_name="vector", index_params=index_params)

        self.vector_db = collection
        return collection

    def get_level_collection(self, level):
        schema = m.CollectionSchema(
            fields=[
                m.FieldSchema(name=f"level_{level}", dtype=m.DataType.VARCHAR, max_length=100, is_primary=True),
                m.FieldSchema(name="value", dtype=m.DataType.VARCHAR, max_length=1000),
                m.FieldSchema(name="dummy_vector", dtype=m.DataType.FLOAT_VECTOR, dim=2)
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
        for i in range(1, 8):
            self.get_level_collection(i)

settings = Settings()
