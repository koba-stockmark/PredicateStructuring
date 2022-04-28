import json
import re
from object_verb_structureing import VerbExtractor

model = VerbExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
solution = open('solution_sentence.txt')
out_file = open('result.tsv', 'w')
out_file2 = open('result_nikkei.tsv', 'w')

#"""
for doc in solution:
  for sep_doc in doc.splitlines():
    keyword_list = model.v_o_get2(sep_doc) # キーワードの候補の抽出
    out_file.write(keyword_list)
out_file.close()
"""
for doc in articles:
  for sep_doc in doc.splitlines():
    keyword_list = model.v_o_get(sep_doc) # キーワードの候補の抽出
    out_file2.write(keyword_list)
out_file2.close()
"""