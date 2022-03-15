from __future__ import unicode_literals # It is not necessary when you use python3.
from pyknp import KNP
import spacy
import json
import time
import mojimoji

nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル

knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
text = '開発陣は経営危機、新型コロナウイルス禍などいくつものハードルを乗り越え、ついに旗艦車が日の目を見ようとしている。'

articles = json.load(open('nikkei_5000.json'))

print("KNP start")
start = time.time()
for doc in articles:
    for sep_doc in doc.splitlines():
        #print(sep_doc)
        result = knp.parse(mojimoji.han_to_zen(sep_doc))
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

print("spaCY start")
start = time.time()
for doc in articles:
    for sep_doc in doc.splitlines():
        doc = nlp(sep_doc)  # 文章を解析
elapsed_time = time.time() - start

print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")



"""
for bnst in result.bnst_list(): # 各文節へのアクセス
    print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" \
            % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))

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
"""