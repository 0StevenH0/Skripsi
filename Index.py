from pathlib import Path

import faiss
import pickle
from settings import Settings


class Index:

    def __init__(self, index=None):
        if not self.load_index():
            self.index = index

    def train(self, data, step_per_train=5):

        for i in range(0, len(data) - 4, step_per_train):
            _data = data[i:i + step_per_train]
            faiss.normalize_L2(_data)
            self.index.add(_data)

        self.save_index()
        print(self.index.ntotal)

    def save_index(self):
        faiss.write_index(self.index, settings.index_file_name)

    def load_index(self):
        index_file_path = Path(settings.index_file_name)

        if index_file_path.exists():
            self.index = faiss.read_index(str(index_file_path))
            return True
        else:
            return False

    def search(self,vector,k=7):
        faiss.normalize_L2(vector)
        docs = self.index.search(vector, k=k)
        return docs


settings = Settings()
