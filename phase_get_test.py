import json
import re
from object_verb_structureing import VerbExtractor

model = VerbExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
solution = open('solution_sentence.txt')
out_file = open('phase_result.tsv', 'w')

#"""
for doc in solution:
  for sep_doc in doc.splitlines():
    keyword_list = model.phase_get(sep_doc) # キーワードの候補の抽出
    ret = sep_doc + '\t' + keyword_list + '\n'
    print(ret)
    out_file.write(ret)
out_file.close()
"""
for doc in articles:
  for sep_doc in doc.splitlines():
    keyword_list = model.v_o_get(sep_doc) # キーワードの候補の抽出
    out_file2.write(keyword_list)
out_file2.close()
"""