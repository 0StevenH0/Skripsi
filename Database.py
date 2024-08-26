import pymilvus as m
from settings import Settings


class DB:


    def get_vector_collection(self):
        id_field = m.FieldSchema(name="id", dtype=m.DataType.INT64, is_primary=True, auto_id=True)
        vector_field = m.FieldSchema(name="vector", dtype=m.DataType.FLOAT_VECTOR, dim=settings.vector_dims)
        text_field = m.FieldSchema(name="text", dtype=m.DataType.VARCHAR, max_length=1000)

        schema = m.CollectionSchema(fields=[id_field, vector_field, text_field],
                                    description="Text vector collection with HNSW index")

        # Create the collection
        collection_name = "hnsw_vectors"
        collection = m.Collection(name=collection_name, schema=schema)

        # Create HNSW index
        index_params = {
            "metric_type": settings.vector_metrics,
            "index_type": settings.vector_index_type,
            "params": settings.params
        }
        collection.create_index(field_name="vector", index_params=index_params)

        return collection

settings = Settings()