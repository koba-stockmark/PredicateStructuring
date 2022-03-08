import json
import re
from object_verb_structureing import VerbExtractor

model = VerbExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))

for doc in articles:
#  print('doc = ', doc)
  for sep_doc in doc.splitlines():
#  for sep_doc in re.findall("\n",doc):
#    print("sep = ",sep_doc)
    keyword_list = model.v_o_get(sep_doc) # キーワードの候補の抽出