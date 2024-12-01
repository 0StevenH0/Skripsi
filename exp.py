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


def init_index():
    setting = settings.Settings()
    model_manager = ModelManager.ModelManager()
    core_model = CoreModel()
    nltk.download("punkt")
    core_model.add(
        model=model_manager.model,
        tokenizer=model_manager.tokenizer,
        qa_model=model_manager.qa_model,
    )

    knowledge_handler = KnowledgeHandler()

    for key, value in knowledge_handler.list_per_level().items():
        index_per_level = Index(faiss.IndexFlatIP(setting.vector_dims), f"{key}.index")
        level_item = []
        for i in value:
            embed = core_model.embed(i, pool=False)[1]
            level_item.append(embed.mean(dim=1))
        level_item = torch.stack(level_item, dim=1)[0]
        level_item = level_item.detach().numpy()
        level_item = level_item.astype(np.float32)
        index_per_level.train2(level_item, path=f"{key}.index")


@Record("test.csv")
def test_index(chunked_entity):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
    setting = settings.Settings()

    model_manager = ModelManager.ModelManager()
    core_model = CoreModel()
    nltk.download("punkt")
    core_model.add(
        model=model_manager.model,
        tokenizer=model_manager.tokenizer,
        qa_model=model_manager.qa_model,
    )

    res = []
    for i in chunked_entity:
        index = Index(path=f"level_{i[1].item()}.index")
        search_vector = core_model.embed(i[0], pool=False)[1]
        search_vector = search_vector.mean(dim=1).detach().numpy().reshape(1, -1)
        res.append(index.search(search_vector))

    return res


@Record("test.csv")
def test():
    setting = settings.Settings()
    model_manager = ModelManager.ModelManager()
    core_model = CoreModel()
    nltk.download("punkt")
    core_model.add(
        model=model_manager.model,
        tokenizer=model_manager.tokenizer,
        qa_model=model_manager.qa_model,
    )
    return core_model.embed("ACCOUNTING")


def test2():
    print(KnowledgeHandler.list_per_level()["level_1"][5])


# init_index()
test2()


# test_index(
#     [
#         ("waktu berapa tahun", torch.tensor(1)),
#         ("sains komputer", torch.tensor(3)),
#         ("akuntansi", torch.tensor(3)),
#     ]
# )
