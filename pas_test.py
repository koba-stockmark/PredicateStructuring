import json
import spacy
from data_dump import DataDumpSave
from pas_analysis import PasAnalysis

pas_model = PasAnalysis()
d_d_s = DataDumpSave()

nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル

def pas_get(debug, text):
    ##########################################################################################################################################
    # 形態素解析
    ##########################################################################################################################################
    doc = nlp(text)  # 文章を解析
    d_d_s.text_treace(*doc)
    ##########################################################################################################################################
    # 述語項構造解析
    ##########################################################################################################################################
    pas_result = pas_model.pas_analysis(debug, text, *doc)
    argument = pas_result[0]["argument"]
    predicate = pas_result[0]["predicate"]
    ret = d_d_s.data_dump_and_save3(text, argument, predicate)
    return ret

# test
articles = json.load(open('nikkei.json'))
articles2 = json.load(open('nikkei_5000.json'))
articles3 = json.load(open('gyoukai.json'))
articles4 = json.load(open('datsutanso.json'))
solution = open('solution_sentence.txt')
error = open('error.txt')
#head = open('../DataClean/head_1line.txt')

#out_file = open('result.tsv', 'w')
out_file = open('result_nikkei.tsv', 'w')
#out_file = open('result_head_1line.tsv', 'w')

for doc in articles2:
    for sep_doc in doc.splitlines():
        keyword_list = pas_get(False, sep_doc)  # キーワードの候補の抽出
        out_file.write(keyword_list)
    out_file.write("----\t----\t----\t----\t----\t----\t----\t----\t----\t----\n")
out_file.close()
