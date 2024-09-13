from settings import Settings
import os
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, BertModel, BertForQuestionAnswering, AutoModelForSeq2SeqLM


class ModelManager:
    __slots__ = ["model", "typo_corrector", "tokenizer", "qa_model"]

    def __init__(self):
        print("Initializing model")
        self.model = self.init_model()
        print("Initializing tokenizer")
        self.tokenizer = self.init_tokenizer()
        print("Initializing qa_model")
        self.qa_model = self.init_qa_model()
        print("Initializing typo corrector")
        self.typo_corrector = self.init_typo_corrector()

    def init_model(self):
        self.ensure_directory_exists(settings.model_path)
        if not self.is_file_exist(settings.model_path):
            print("Downloading model from Hugging Face")
            model = BertModel.from_pretrained(settings.source_model_path)
            model.save_pretrained(settings.model_path)

        print("Model initialized")
        return BertModel.from_pretrained(settings.model_path)

    def init_tokenizer(self):
        self.ensure_directory_exists(settings.tokenizer_path)
        if not self.is_file_exist(settings.tokenizer_path):
            print("Downloading tokenizer from Hugging Face")
            tokenizer = AutoTokenizer.from_pretrained(settings.source_tokenizer_path)
            tokenizer.save_pretrained(settings.tokenizer_path)

        print("Tokenizer initialized")
        return AutoTokenizer.from_pretrained(settings.tokenizer_path)

    def init_qa_model(self):
        self.ensure_directory_exists(settings.qa_model_path)
        if not self.is_file_exist(settings.qa_model_path):
            print("Downloading QA model from Hugging Face")
            qa_model = BertForQuestionAnswering.from_pretrained(settings.source_qa_model_path)
            qa_model.save_pretrained(settings.qa_model_path)

        print("QA model initialized")
        return AutoModelForQuestionAnswering.from_pretrained(settings.qa_model_path)

    def init_typo_corrector(self):
        self.ensure_directory_exists(settings.typo_corrector_path)
        if not self.is_file_exist(settings.typo_corrector_path):
            print("Downloading typo corrector model from Hugging Face")
            typo_corrector = AutoModelForSeq2SeqLM.from_pretrained(settings.source_typo_corrector_path)
            typo_corrector.save_pretrained(settings.typo_corrector_path)

        print("Typo corrector initialized")
        return AutoModelForSeq2SeqLM.from_pretrained(settings.typo_corrector_path)

    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

    def is_file_exist(self, path):
        if not os.path.exists(path):
            print(f"The directory {path} does not exist.")
            return False
        if not os.path.isdir(path):
            print(f"{path} is not a directory.")
            return False
        return len(os.listdir(path)) > 0


settings = Settings()
