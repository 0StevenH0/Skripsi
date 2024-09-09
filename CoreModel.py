from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import faiss

from settings import Settings


class CoreModel():
    __slots__ = ["model", "typo_corrector", "tokenizer","index","qa_model"]

    def __init__(self):
        self.model = None
        self.typo_corrector = None
        self.tokenizer = None
        self.qa_model = None
        self.index = faiss.IndexFlatIP(settings.vector_dims)

    def add(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__slots__:
                setattr(self, key, value)
            else:
                raise AttributeError(f"Unknown attribute: {key}")

    def embed(self, text, pool = True):
        tokens = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**tokens)

        if pool:
            return tokens, outputs["pooler_output"], outputs
        return tokens, outputs["last_hidden_state"], outputs

    def train_index(self,knowledge):

        for i in range(0, len(knowledge) - 5, 5):
            z = knowledge[i:i + 4]
            faiss.normalize_L2(z)
            self.index.add(z)

        faiss.write_index(self.index,settings.index_file_name)

settings = Settings()