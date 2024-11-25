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
from RecordKeeper import persist_result
import dill
import re


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

    knowledge_handler = KnowledgeHandler()

    for key, value in knowledge_handler.list_per_level().items():
        index_per_level = Index(
            faiss.IndexFlatIP(setting.vector_dims), f"level_{key}.index"
        )
        level_item = []
        for i in value:
            level_item.append(core_model.embed(i, pool=True)[1])
        level_item = torch.stack(level_item, dim=1)[0]
        level_item = level_item.detach().numpy()
        level_item = level_item.astype(np.float32)
        index_per_level.train(level_item, path=f"level_{key}.index")


test()
