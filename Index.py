from pathlib import Path

import faiss
import pickle
from settings import Settings


class Index:
    def __init__(self, index=None, path=None):
        self.index = None
        if not self.load_index(path):
            self.index = index

    def train(self, data, step_per_train=5, path=None):
        print(f"train for : {data}")
        for i in range(0, len(data) - 4, step_per_train):
            _data = data[i : i + step_per_train]
            faiss.normalize_L2(_data)
            self.index.add(_data)

        print(path)
        self.save_index(path)
        print(self.index.ntotal)

    def train2(self, data, path=None):
        faiss.normalize_L2(data)
        self.index.add(data)
        self.save_index(path)

    def save_index(self, path=None):
        faiss.write_index(self.index, path or settings.index_file_name)

    def load_index(self, path=None):
        index_file_path = Path(path or settings.index_file_name)

        if index_file_path.exists():
            self.index = faiss.read_index(str(index_file_path))
            return True
        else:
            return False

    def search(self, vector, k=5):
        faiss.normalize_L2(vector)
        docs = self.index.search(vector, k=k)
        return docs


settings = Settings()
