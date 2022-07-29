import json
import re
from phase_extractor import PhaseExtractor

model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
articles2 = json.load(open('nikkei_5000.json'))
solution = open('solution_sentence.txt')
error = open('error.txt')
out_file = open('result.tsv', 'w')
out_file2 = open('result_nikkei.tsv', 'w')

#"""
for doc in solution:
  for sep_doc in doc.splitlines():
    keyword_list = model.pas_get(sep_doc, 0) # キーワードの候補の抽出
    out_file.write(keyword_list)
out_file.close()
"""
for doc in articles2:
  for sep_doc in doc.splitlines():
    keyword_list = model.pas_get(sep_doc, 0) # キーワードの候補の抽出
    out_file2.write(keyword_list)
  out_file2.write("----\t----\t----\t----\t----\t----\t----\t----\t----\t----\n")
out_file2.close()
"""