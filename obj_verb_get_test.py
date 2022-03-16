import json
import re
from object_verb_structureing import VerbExtractor

model = VerbExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
solution = open('solution_sentence.txt')
out_file = open('result.txt', 'w')
#for doc in articles:
for doc in solution:
#  print('doc = ', doc)
  for sep_doc in doc.splitlines():
#  for sep_doc in re.findall("\n",doc):
#    print("sep = ",sep_doc)
    keyword_list = model.v_o_get(sep_doc) # キーワードの候補の抽出

    out_file.write(keyword_list)

out_file.close()