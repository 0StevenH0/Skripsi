from KnowledgeHandler import KnowledgeHandler
from fuzzywuzzy.process import extractOne
import Levenshtein

knowledge = KnowledgeHandler().question_mapping()

# will be disposable later
def match(question,knowledge:KnowledgeHandler):
	question_mapping = knowledge.question_mapping()
	possible_question = question_mapping.keys()
	matched = question_preprocessing_strategy(question,possible_question)
	if matched[0]:
		return question,question_mapping[matched[1]]
	return question,question

def question_preprocessing_strategy(text,knowledge,threshold = 0.7):

	match,score = extractOne(text,knowledge)
	return (True, match) if score > threshold else (False, text)

