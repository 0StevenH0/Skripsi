import faiss

import DBController
import settings
import FixTypo
import torch
import DBManager
import ModelManager
from CoreModel import CoreModel
from nltk.tokenize import sent_tokenize
import nltk
from fastapi import FastAPI
from KnowledgeHandler import KnowledgeHandler
from RequestForm import ModelRequest
import numpy as np
from Index import Index
import os
import google.generativeai as genai
from MatchingStrategy import *
from RecordKeeper import Record, persist_result
import dill
import re
from PreProcess import PreProcess

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global \
        core_model, \
        connection, \
        db, \
        index, \
        knowledge_handler, \
        gemini_model, \
        app_settings

    # this solution is bad, but dont have lots of time so fk it
    os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
    # Initialize settings and models
    app_settings = settings.Settings()
    genai.configure(api_key=app_settings.GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash-exp-0827")

    print("Establishing connection\n")

    # Establish database connection
    connection = DBController.DBController(
        app_settings.link,
        app_settings.alias,
        app_settings.host,
        app_settings.user,
        app_settings.port,
        app_settings.password,
    )
    knowledge_handler = KnowledgeHandler()
    connection.connect()

    connection.use_db(app_settings.vector_db_name)

    print("Setting up\n")

    model_manager = ModelManager.ModelManager()
    core_model = CoreModel()

    index = Index()

    print("installing punkt")
    nltk.download("punkt")
    core_model.add(
        model=model_manager.model,
        tokenizer=model_manager.tokenizer,
        qa_model=model_manager.qa_model,
    )
    with open("model.pkl", "rb") as f:
        core_model.add(ner=dill.load(f))

    core_model.add(pre_process=PreProcess())
    db = DBManager.DBManager(connection.connection, connection.cursor)

    print("Startup complete")


@app.post("/response")
async def response(request: ModelRequest):
    # Main Port
    global core_model, connection, db, index

    print("starting")
    knowledge = KnowledgeHandler()
    text = match(request.search, knowledge)
    search_vector = core_model.embed(text[1])[1]
    search_vector = search_vector.detach().numpy()

    docs = index.search(search_vector)

    condition = knowledge_handler.make_condition(request.search)
    result = connection.get_vector_db(docs[1], condition)
    answers = ".".join([i[0].strip() for i in result])
    inputs = core_model.tokenizer(text[0], answers, return_tensors="pt")
    outputs = core_model.qa_model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    return_query = {}

    if start_index >= end_index:
        answer = "Maaf Saya Tidak Dapat Menjawab Pertanyaan Anda"
    else:
        answer_tokens = inputs["input_ids"][0][start_index : end_index + 1]
        answer = core_model.tokenizer.decode(answer_tokens, skip_special_tokens=True)

    return_query["BERT_MODEL"] = answer

    condition = knowledge_handler.make_condition(text[1])
    result = connection.get_vector_db(docs[1], condition)
    answers = ".".join([i[0].strip() for i in result])

    try:
        gemini_answer = gemini_model.generate_content(
            f"Answer question about binus based on this knowledge and ensure you're using the same language the user ask. Knowledge : {answers}; question : {request.search}",
            safety_settings={"HARASSMENT": "block_none"},
        )
        return_query["GEMINI"] = gemini_answer.text
    except Exception as e:
        return_query["GEMINI"] = f"error {e} for question : request.search"

    persist_result(request, return_query, answers)
    return {"message": return_query["GEMINI"]}


@app.post("/response2")
async def response_2(request: ModelRequest):
    # Main Port
    global core_model, connection, db, index, app_settings

    print("starting")
    question = re.sub(r"[^\w\s]", "", request.search)
    question = question.lower()
    question = core_model.pre_process.process(question)
    ner_result = torch.tensor(core_model.ner.predict(question))
    merged_pairs = merge_pairs(question, ner_result)
    merged_pairs = index_per_level(merged_pairs, app_settings.threshold)
    query_condition = db.query_construction(merged_pairs)
    result = connection.find_data(query_condition)
    answers = ".".join([i[0].strip() for i in result])

    return_query = {}

    try:
        gemini_answer = gemini_model.generate_content(
            f"Answer question about binus based on this knowledge and ensure you're using the same language the user ask. Knowledge : {answers}; question : {request.search}",
            safety_settings={"HARASSMENT": "block_none"},
        )
        return_query["GEMINI"] = gemini_answer.text
    except Exception as e:
        return_query["GEMINI"] = f"error {e} for question : request.search"

    return {"message": return_query["GEMINI"]}


@app.post("/response-gemini")
async def gemini_response(request: ModelRequest):
    # Main Port
    global core_model, connection, db, index, knowledge_handler, gemini_model

    print("starting")
    search_vector = core_model.embed(request.search)[1]
    search_vector = search_vector.detach().numpy()

    docs = index.search(search_vector)

    condition = knowledge_handler.make_condition(request.search)

    result = connection.get_vector_db(docs[1], condition)
    print(result)
    answers = ".".join([i[0].strip() for i in result])
    gemini_response = gemini_model.generate_content(
        f"Answer question about binus based on this knowledge and ensure you're using the same language the user ask.Knowledge : {answers}; question : {request.search}",
        safety_settings={"HARASSMENT": "block_none"},
    )

    print(gemini_response)

    return {"message": gemini_response.text}


@app.get("/fix")
async def fix_relation():
    # Use this to repopulate
    global db

    db.create_relation()

    return {
        "message": "YEAH~~~!!! API is working!; ",
        "ignore this": "function : fix_relation",
    }


@app.get("/debug")
async def debug():
    # Use this for debugging
    global core_model, connection, db

    print(db.vector_db.list_collections)

    return {
        "message": "YEAH~~~!!! API is working!; ",
        "ignore this": db.vector_db,
        "ignore this 2": db.level_dbs,
    }


@app.post("/search")
async def search(request: ModelRequest):
    # Implement Search
    global core_model, connection, db, index
    embed = core_model.embed(request.search)[1]
    question = embed.detach().numpy()
    faiss.normalize_L2(question)
    docs = index.index.search(question, k=7)

    print(connection.get_vector_db(docs[1]))

    return {"response": "ok"}


@app.on_event("shutdown")
async def shutdown_event():
    global connection

    connection.disconnect()


if __name__ == "__main__":
    # This part of the code will be used for Resetting everything, including initializing DB, Model, And Inserting Data
    print("setting up\n")

    settings = settings.Settings()
    model_manager = ModelManager.ModelManager()
    core_model = CoreModel()
    print("downloading punkt")
    nltk.download("punkt")
    core_model.add(
        model=model_manager.model,
        tokenizer=model_manager.tokenizer,
        qa_model=model_manager.qa_model,
    )

    print("settings up done\nestablishing connection\n")

    connection = DBController.DBController(
        settings.link,
        settings.alias,
        settings.host,
        settings.user,
        settings.port,
        settings.password,
    )

    connection.connect()

    connection.purge_db(settings.vector_db_name)

    connection.create_db(settings.vector_db_name)

    connection.use_db(settings.vector_db_name)

    knowledge_handler = KnowledgeHandler()
    context = knowledge_handler.temporary_knowledge()
    knowledge = []

    for i in context:
        knowledge.append(core_model.embed(i, pool=True)[1])
    knowledge = torch.stack(knowledge, dim=1)[0]

    knowledge = knowledge.detach().numpy()
    knowledge = knowledge.astype(np.float32)
    # knowledge = [i.tobytes() for i in knowledge]
    level = knowledge_handler.make_level()

    index = Index(faiss.IndexFlatIP(settings.vector_dims))
    index.train(knowledge)

    index.load_index()

    index_per_level = Index(faiss.IndexFlatIP(settings.vector_dims))

    db = DBManager.DBManager(connection.connection, connection.cursor)

    print("Inserting to DB")

    db.insert_to_vector_table(context, level, settings.insert_batch_size)

    #
    # for i in range(0,8):
    #     db.level_dbs[f"level_{i}_db"].insert([
    #         level[f"level_{i}"],
    #
    #     ])

    # import random
    #
    # # Prepare some sample data
    # num_entities = 1000
    # vectors = [[random.random() for _ in range(256)] for _ in range(num_entities)]
    # texts = [f"Text {i}" for i in range(num_entities)]
    #
    # collection.insert([vectors,texts])
    #
    # collection.load()
    #
    # search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    # results = collection.search(
    #     data=[vectors[0]],  # Use the first vector as a query example
    #     anns_field="vector",
    #     param=search_params,
    #     limit=5,
    #     expr=None,
    #     output_fields=["text"]
    # )
    #
    # # Print results
    # for hits in results:
    #     for hit in hits:
    #         print(f"ID: {hit.id}, Distance: {hit.distance}, Text: {hit.entity.get('text')}")
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
    pass


@Record("entity_chunking.csv")
def merge_pairs(_question, model_prediction):
    question = _question.split(" ")

    merged_pairs = []
    current_pred = None
    current_text = []

    for q, pred in zip(question, model_prediction):
        if pred == 0:
            if current_text:
                merged_pairs.append([" ".join(current_text), current_pred])
                current_text = []
            current_pred = None
        elif pred == current_pred:
            current_text.append(q)
        else:
            if current_text:
                merged_pairs.append([" ".join(current_text), current_pred])
            current_pred = pred
            current_text = [q]

    if current_text:
        merged_pairs.append([" ".join(current_text), current_pred])

    if not merged_pairs:
        return -1

    return merged_pairs


@Record("per_level_index_mapping.csv")
def index_per_level(chunked_entity, threshold):
    global knowledge_handler
    res = []
    for j, i in enumerate(chunked_entity):
        index = Index(path=f"level_{i[1].item()}.index")
        search_vector = core_model.embed(i[0], pool=False)[1]
        search_vector = search_vector.mean(dim=1).detach().numpy().reshape(1, -1)
        dist, idx = index.search(search_vector, k=1)
        if dist[0] > threshold:
            chunked_entity[j][0] = knowledge_handler.list_per_level()[
                f"level_{i[1].item()}"
            ][idx[0][0]]
            res.append(chunked_entity[j])

    return res
