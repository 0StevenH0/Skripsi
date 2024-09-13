import torch
import transformers
from transformers import pipeline

# TODO
"""use pretrained library to remove typos, then return it"""
class typo_corrector():
    def __init__(self, model_path="./typo_corrector"):
        self.corrector = pipeline("text2text-generation", model=model_path)

    def correct_text(self, text: str, max_length: int = 512) -> str:
        corrected = self.corrector(text, max_length=max_length)

        corrected_text = corrected[0]['generated_text']

        return corrected_text