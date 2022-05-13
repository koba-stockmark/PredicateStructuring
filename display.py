text = '今日は天気が良いので公園兵へいきいます。'

import spacy
nlp = spacy.load('ja_ginza_electra')

from spacy import displacy

doc = nlp(text)
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

displacy.render(doc, style="dep", options={"compact": True})