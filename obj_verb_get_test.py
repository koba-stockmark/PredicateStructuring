import json
import re
from phase_extractor import PhaseExtractor

model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
solution = open('solution_sentence.txt')
out_file = open('result.tsv', 'w')
out_file2 = open('result_nikkei.tsv', 'w')

#"""
for doc in solution:
  for sep_doc in doc.splitlines():
    keyword_list = model.pas_get(sep_doc) # キーワードの候補の抽出
    out_file.write(keyword_list)
out_file.close()
"""
for doc in articles:
  for sep_doc in doc.splitlines():
    keyword_list = model.pas_get(sep_doc) # キーワードの候補の抽出
    out_file2.write(keyword_list)
out_file2.close()
"""