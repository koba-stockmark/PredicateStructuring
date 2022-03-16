import spacy
from spacy.matcher import DependencyMatcher, Matcher
from spacy.tokens import Token

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

kanryou_rule = [    # 書いた
    [
        {"TAG": {"REGEX": "^動詞"}},
        {
            "TEXT": {"IN": ["た", "だ"]},
            "TAG": "助動詞"
        }
    ],
    [    # 勉強した
        {"TAG": {"REGEX": "^名詞"}},
        {
            "LEMMA": {"IN": ["する"]},
            "TAG": {"REGEX": "^動詞"}
        },
        {
            "TEXT": {"IN": ["た"]},
            "TAG": "助動詞"
        }
    ],
    [    # 書きたかった
        {"TAG": {"REGEX": "^動詞"}},
        {"TAG": "助動詞"},
        {
            "TEXT": {"IN": ["た"]},
            "TAG": "助動詞"
        }
    ],
    [   # 美しかった
        {"TAG": {"REGEX": "^形容詞"}},
        {
            "TEXT": {"IN": ["た", "だ"]},
            "TAG": "助動詞"
        }
    ]
]

kanryou_rule1 = [
    [
        {"MORPH": "五段-マ行;連用形-撥音便"}
#        {"MORTH": "形態素", "_": {"Inflection": "連用形"}}
#        {"MORPH": "Inflection", "_": "五段-マ行;連用形-撥音便"}
  #      {"MORPH": {"Inflection": {"五段-マ行;連用形-撥音便"}}}
        #       "TEXT": {"IN": ["た", "だ"] }]
    ]
]

#####
# 断定（意思表明）、進行
#####

dantei_rule = [
    [  # 書く。
        {"TAG": {"REGEX": "^動詞"}},
        {"TEXT": {"IN": ["。", "、"]}}
    ],
    [  # 書く
        {"TAG": {"REGEX": "^動詞"},
         "IS_SENT_START": True}
    ],
    [  # 美しい
        {"TAG": {"REGEX": "^形容詞"}},
        {"TEXT": {"IN": ["。", "、"]}}
    ],
    [     # 学校だ
        {"TAG": {"REGEX": "^名詞"}},
        {"TEXT": {"IN": ["だ"]}}
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

        fruit_getter = lambda token: token.text in ("apple", "pear", "banana")
        Token.set_extension("Inflection", getter=fruit_getter)

        self.matcher = Matcher(self.nlp.vocab)            # Matcher  のセット
        self.matcher.add("完了", kanryou_rule)
        self.matcher.add("断定", dantei_rule)
        self.matcher.add("noun-adj", match_patterns)

        self.dependency_matcher = DependencyMatcher(self.nlp.vocab)            # DependencyMatcher  のセット
        self.dependency_matcher.add("adj_noun_pair", dependency_patterns)
        return

    def depend_get(self, text):
        doc = self.nlp(text)

        for token in doc:
            print(
                token.i,
                token.orth_,
                token.lemma_,
                token.norm_,
                token.morph.get("Reading"),
                token.pos_,
                token.morph.get("Inflection"),
                token.tag_,
                token.dep_,
                token.head.i,
            )

# matcher
        matches = self.matcher(doc)
        print("matches = ", matches)
        for mat in matches:
            print(mat)
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            print("【", string_id, "】", doc[start:end].orth_)

# dependency_matcher
        dependency_match = self.dependency_matcher(doc)
        print("dep_matches = ", dependency_match)
        for mat in dependency_match:
            print(mat)

        for match_id, alignments in dependency_match:
            string_id = self.nlp.vocab.strings[match_id]
            print(string_id, [doc[alignment].lemma_ for alignment in alignments])
        return

