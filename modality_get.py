import spacy
from spacy.matcher import DependencyMatcher, Matcher

"""
構想、研究、実装、販売
"""

match_patterns = [
    [
        {"TAG": {"REGEX": "^名詞"}},
        {"TEXT": {"IN": ["は", "が"]}}, #「は」か「が」のいずれかにマッチ
        {"TAG": {"REGEX": "^形容詞"}}],
#       {"TAG": {"REGEX": "^形容詞"}},
#       {"TAG": {"REGEX": "^助動詞"}}],
    [
        {"TAG": {"REGEX": "^形容詞"}},
        {"TAG": {"REGEX": "^助動詞"}},
        {"TAG": {"REGEX": "^補助記号"}}
    ]

    ]

#####
# 完了
#####

kanryou_rule = [
    [
        {"TAG": {"REGEX": "^動詞", "REGEX": "^形容詞"}},
        {
            "TEXT": {"IN": ["た", "だ"]},
            "TAG": "助動詞"
        }
    ]
]

kanryou_rule1 = [
    [
        {"MORPH": {"Inflection" : {"五段-マ行;連用形-撥音便"}}}
#       "TEXT": {"IN": ["た", "だ"] }]
    ]
]

#####
# 断定（意思表明）、進行
#####

dantei_rule = [
  [
        {"TAG": {"REGEX": "^名詞"}},
        {"TEXT": {"IN": ["は", "が"]}}, #「は」か「が」のいずれかにマッチ
        {"TAG": {"REGEX": "^補助記号"}},
        {"TEXT": {"IN": ["は", "が"]}} #「は」か「が」のいずれかにマッチ
  ]
]
#####
# 目標、予定、計画
#####

#####
# 中止
#####

#####
# 再開
#####

#####
# 否定
#####

#####
# 願望
#####

dependency_patterns = [
    [
        {
            "RIGHT_ID": "adj"
            ,"RIGHT_ATTRS": {"TAG": {"REGEX": "^形容詞"}}
        },
        {
            "LEFT_ID": "adj"
            ,"REL_OP": ">"
            ,"RIGHT_ID": "noun"
            ,"RIGHT_ATTRS": {"TAG": {"REGEX": "^名詞"}, "DEP": "nsubj"}
        }
    ]
]

class DependExtractor:

    def __init__(self):
        self.nlp = spacy.load('ja_ginza_electra')         # Ginzaのロード　tranceferモデル

        self.matcher = Matcher(self.nlp.vocab)            # Matcher  のセット
        self.matcher.add("完了", kanryou_rule)
        self.matcher.add("noun-adj", match_patterns)

        self.dependency_matcher = DependencyMatcher(self.nlp.vocab)            # DependencyMatcher  のセット
        self.dependency_matcher.add("adj_noun_pair", dependency_patterns)
        return

    def depend_get(self, text):
        doc = self.nlp(text)
# matcher
        matches = self.matcher(doc)
        print("matches = ", matches)
        for mat in matches:
            print(mat)
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            print("【", string_id, "】", doc[start:end].orth_)

# dependency_matcher
        matches = self.dependency_matcher(doc)
        print("dep_matches = ", matches)
        for mat in matches:
            print(mat)

        for match_id, alignments in matches:
            string_id = self.nlp.vocab.strings[match_id]
            print(string_id, [doc[alignment].lemma_ for alignment in alignments])
        return

