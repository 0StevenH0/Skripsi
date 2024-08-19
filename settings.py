import pymilvus as m

class Settings():
    # IK should use ENV; but too lazy to set it
    def __init__(self):
        self.alias = "default"
        self.vector_db_name = "vector_db"
        self.mm_db_name = "multi_media_db"
        self.host = "127.0.0.1"
        self.user = "user"
        self.password = "Santa_Claus"
        self.port = 19530
        self.link = "temp link"
        self.vector_dims = 256
        self.vector_metrics = "L2"
        self.vector_index_type = "HNSW"
        self.params ={
            "M": 16,
            "efConstruction": 500
        }

    def get_vector_collection(self):
        id_field = m.FieldSchema(name="id", dtype=m.DataType.INT64, is_primary=True, auto_id=True)
        vector_field = m.FieldSchema(name="vector", dtype= m.DataType.FLOAT_VECTOR, dim=self.vector_dims)
        text_field = m.FieldSchema(name="text", dtype=m.DataType.VARCHAR, max_length=1000)

        schema = m.CollectionSchema(fields=[id_field, vector_field,text_field],
                                  description="Text vector collection with HNSW index")

        # Create the collection
        collection_name = "hnsw_vectors"
        collection = m.Collection(name=collection_name, schema=schema)

        # Create HNSW index
        index_params = {
            "metric_type": self.vector_metrics,
            "index_type": self.vector_index_type,
            "params": self.params
        }
        collection.create_index(field_name="vector", index_params=index_params)

        return collection