import re
import dill
import sys
import os

from RecordKeeper import Record

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class PreProcess:
    def __init__(self, knowledge: dict = None):
        self.knowledge = knowledge or {
            "compsci": "sains komputer",
            "compscience": "sains komputer",
            "computer science": "sains komputer",
        }

    @Record("pre_processing.csv")
    def process(self, text):
        pattern = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in self.knowledge.keys()) + r")\b",
            re.IGNORECASE,
        )

        def replace_match(match):
            key = match.group(0)
            return self.knowledge.get(key, key)

        return pattern.sub(replace_match, text)
