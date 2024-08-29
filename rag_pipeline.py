from transformers import BertTokenizer, TFBertModel,BertForQuestionAnswering
import torch
import DBController,FixTypo

class BERT_QA():

    def __init__(self, tokenizer_path='./pretrained', qa_model_path="./QA_model"):
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.QA = BertForQuestionAnswering.from_pretrained(qa_model_path)

    def get_context(self,user_input:str)->list:
        """
        get context from the database

        :param user_input: user input, this got from frontend
        :return: sorted ranked text embedding
        """
        # TODO
        pass

    def ans(self,context:list)->str:
        """
        from answer context, answer it using QA model

        :param context: sorted ranked text embedding
        :return: user answer, this to be passed to frontend
        """
        # TODO
        pass

    def __is_out_of_scope(self,s):
        """
        Provide custom answer if model can't answer the question

        :param s: idk, add later
        :return:
        """
        pass