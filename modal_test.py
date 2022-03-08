import ginza
import spacy
from spacy.matcher import DependencyMatcher, Matcher

txts = [
    "書く。書いた。書く本。書きます。書きました。書こう。書きたい。書ければよい。読んだ。",
    "部屋から見える夜景が美しかった。",
    "立地は悪いが食事が美味しい。",
    "客室露天風呂は大人でも足がのばせてとても広かった。"
]

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

kanryou_rule = [
    [
        {"TAG": {"REGEX": "^動詞", "REGEX": "^形容詞"}},
        {
            "TEXT": {"IN": ["た", "だ"]}, #「は」か「が」のいずれかにマッチ
            "TAG": "助動詞"
        }
  ]
]

kanryou_rule1 = [
  [
        {"MORPH": {"Inflection" : {"五段-マ行;連用形-撥音便"}}}
#       "TEXT": {"IN": ["た", "だ"] }}
  ]
]

dantei_rule = [
  [
        {"TAG": {"REGEX": "^名詞"}},
        {"TEXT": {"IN": ["は", "が"]}}, #「は」か「が」のいずれかにマッチ
        {"TAG": {"REGEX": "^補助記号"}},
        {"TEXT": {"IN": ["は", "が"]}} #「は」か「が」のいずれかにマッチ
  ]
]

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
        matches = self.dependency_matcher(doc)
        print("dep_matches = ", matches)
        for mat in matches:
            print(mat)

        for match_id, alignments in matches:
            string_id = self.nlp.vocab.strings[match_id]
            print(string_id, [doc[alignment].lemma_ for alignment in alignments])
        return

###############################################################################

model = DependExtractor()
for text in txts:
    model.depend_get(text)