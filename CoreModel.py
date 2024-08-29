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

    def embed(self, text, is_pooled):
        tokens = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**tokens)

        if is_pooled:
            return tokens, outputs["pooler_output"]
        return tokens, outputs["last_hidden_state"]
