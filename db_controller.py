import torch


class Connector():

    def __init__(self,link,host,user,password,db):
        self.link = link
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        """
        connect to db

        :return: a status that indicates
            0 not connected to db
            1 connected to db
        """
        # TODO
        pass

    def disconnect(self)->int:
        """
        disconnect from db

        :return:status that indicates
            0 not connected to db
            1 connected to db
        """
        # TODO
        pass

    def fetch_per_batch(self,query:str,batch_size:int=1000)->list:
        """
        perform query to database, and retrieve data per batch

        :param query: SQL Quert
        :param batch_size: num data per batch
        :return: sorted ranked text embedding
        """
        # TODO
        pass

    def annoy_search(self,user_input:torch.Tensor)->list:
        """
        perform annoy search based on query per batch result

        :param user_input: embedded user input
        :return: choosen db embedding
        """
        # TODO
        pass

    def text_rank(self,retrieved:list)->list:
        """
        rank retrieved query from annoy search

        :param retrieved:  retrieved value from annoy_search
        :return: sorted ranked text embedding
        """
        # TODO
        pass