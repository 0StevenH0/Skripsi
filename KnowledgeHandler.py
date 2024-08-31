import re
from collections import defaultdict

class KnowledgeHandler:
    __slots__ = ["text"]

    def __init__(self):
        self.text = None

    def temporary_knowledge(self):

        text = [
            "[6[Program Akademik]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [Deskripsi]",
            "[6[Program Akademik]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [Prospek Karir]",
            "[6[Program Akademik]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [Akreditasi]",
            "[6[Program Akademik]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [durasi]",
            "[6[Program Akademik]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [titel]",
        ]

        return text

    def make_level(self):
        text = self.temporary_knowledge()
        grouped_levels = defaultdict(list)

        level_patterns = {
            "level_7": r"\[7\[(.*?)\]\]",
            "level_6": r"\[6\[(.*?)\]\]",
            "level_5": r"\[5\[(.*?)\]\]",
            "level_4": r"\[4\[(.*?)\]\]",
            "level_3": r"\[3\[(.*?)\]\]",
            "level_2": r"\[2\[(.*?)\]\]",
            "level_1": r"\[1\[(.*?)\]\]",
            "level_0": r"\[(.*?)\]"
        }

        for item in text:
            for level, pattern in level_patterns.items():
                match = re.search(pattern, item)
                grouped_levels[level].append(match.group(1) if match else "")

        return dict(grouped_levels)
