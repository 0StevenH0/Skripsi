from transformers import AutoTokenizer, AutoModelForQuestionAnswering


class CoreModel():
    __slots__ = ["model", "typo_corrector", "tokenizer"]

    def __init__(self):
        self.model = None
        self.typo_corrector = None
        self.tokenizer = None

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

