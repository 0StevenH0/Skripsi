from symspellpy import SymSpell, Verbosity
import os

class typo_corrector:
    def __init__(self,
                 prefix_length=7, 
                 dictionary_path="typo_corrector/frequency_dict.txt",
                 term_index=0, 
                 count_index=1):

        self.sym_spell = SymSpell(prefix_length=prefix_length)

        if not os.path.exists(dictionary_path):
            raise FileNotFoundError(f"Frequency dictionary file not found at {dictionary_path}")

        if not self.sym_spell.load_dictionary(dictionary_path, term_index, count_index):
            raise ValueError(f"Failed to load dictionary from {dictionary_path}")

    def fix(self, text: str) -> str:
        corrected_words = []
        for word in text.split():
            corrected_word = self.fix(word)
            corrected_words.append(corrected_word)
        corrected_text = ' '.join(corrected_words)
        return corrected_text

    def fix_word(self, word: str) -> str:
        suggestions = self.sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            return suggestions[0].term
        else:
            return word