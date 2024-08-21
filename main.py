import db_controller
import settings
import fix_typo
import rag_pipeline
import torch

if __name__ == "__main__":
    settings = settings.Settings()

    connection = db_controller.DBConnectorService(
        settings.link,
        settings.alias,
        settings.host,
        settings.user,
        settings.port,
        settings.password
    )

    # uncomment this if database not exist
    connection.purge_db(settings.vector_db_name)
    connection.create_db(settings.vector_db_name)

    # connection.connect()
    connection.use_db(settings.vector_db_name)
    collection = settings.get_vector_collection()

    import random

    # Prepare some sample data
    num_entities = 1000
    vectors = [[random.random() for _ in range(256)] for _ in range(num_entities)]
    texts = [f"Text {i}" for i in range(num_entities)]

    collection.insert([vectors,texts])

    collection.load()

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[vectors[0]],  # Use the first vector as a query example
        anns_field="vector",
        param=search_params,
        limit=5,
        expr=None,
        output_fields=["text"]
    )

    # Print results
    for hits in results:
        for hit in hits:
            print(f"ID: {hit.id}, Distance: {hit.distance}, Text: {hit.entity.get('text')}")
    # model = rag_pipeline.BERT_QA()
    # question = "Who is te daughter of A?"
    # answer = """B'S Father's C and her mother is A"""
    # inputs = model.tokenizer(question, answer, return_tensors="pt")
    #
    # outputs = model.QA(**inputs)
    # start_scores = outputs.start_logits
    # end_scores = outputs.end_logits
    #
    # start_index = torch.argmax(start_scores)
    # end_index = torch.argmax(end_scores)
    #
    # answer_tokens = inputs["input_ids"][0][start_index:end_index + 1]
    # answer = model.tokenizer.decode(answer_tokens, skip_special_tokens=True)
    # print(answer)