from KnowledgeHandler import KnowledgeHandler
from fuzzywuzzy.process import extractOne
import Levenshtein

knowledge = KnowledgeHandler().question_mapping()


def question_preprocessing_strategy(text,threshold = 0.7):

	match,score = extractOne(knowledge.question_mapping(),knowledge)
	return (True, match) if score > threshold else (False, text)

