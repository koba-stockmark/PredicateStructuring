import json
import re
from phase_extractor import PhaseExtractor

model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
articles2 = json.load(open('nikkei_5000.json'))
solution = open('solution_sentence.txt')
error = open('error.txt')
head = open('../DataClean/head_1line.txt')
out_file = open('result.tsv', 'w')
out_file2 = open('result_nikkei.tsv', 'w')
out_file3 = open('result_head_1line.tsv', 'w')

#"""
for doc in solution:
  for sep_doc in doc.splitlines():
    keyword_list = model.phase_get(sep_doc, 0) # キーワードの候補の抽出
    out_file.write(keyword_list)
out_file.close()
#####
"""
for doc in head:
  for sep_doc in doc.splitlines():
    keyword_list = model.phase_get(sep_doc, 2) # キーワードの候補の抽出
    out_file3.write(keyword_list)
out_file3.close()
#####
for doc in articles2:
  for sep_doc in doc.splitlines():
    keyword_list = model.phase_get(sep_doc, 0) # キーワードの候補の抽出
    out_file2.write(keyword_list)
  out_file2.write("----\t----\t----\t----\t----\t----\t----\t----\t----\t----\n")
out_file2.close()
"""