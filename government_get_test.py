import json
import re
from phase_extractor import PhaseExtractor

model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

articles = json.load(open('nikkei.json'))
articles2 = json.load(open('nikkei_5000.json'))
solution2 = open('government_news.txt')
out_file2 = open('government_result.tsv', 'w')

#"""
for doc in solution2:
  for sep_doc in doc.splitlines():
    keyword_list = model.government_action_extract(sep_doc, 1) # キーワードの候補の抽出
    ret = sep_doc + '\t' + keyword_list + '\n'
    print(ret)
    out_file2.write(ret)
out_file2.close()
"""
for doc in articles:
  for sep_doc in doc.splitlines():
    keyword_list = model.government_action_extract(sep_doc) # キーワードの候補の抽出
    ret = sep_doc + '\t' + keyword_list + '\n'
    print(ret)
    out_file2.write(ret)
out_file2.close()
"""