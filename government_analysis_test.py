import json
from government_news_analysis import GovernmentNewsAnalysis

gnp = GovernmentNewsAnalysis()

input_file = "keisan_input.json"
input_file2 = "env.json"
out_file = open('keisan_result.tsv', 'w')

# 政府ニュースのチェック
gnp.government_news_analysis(input_file2)

d = {}
f = open("news_out.json", mode="r")
j_data = json.load(f)
for d in j_data:
    print("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (d["id"], d["soshiki"], d["busho"], d["title"], d["title_type"], d["head"].replace('\t', '\\t'), d["head_type"]))
    out_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (d["id"], d["soshiki"], d["busho"], d["title"], d["title_type"], d["head"].replace('\t', '\\t'), d["head_type"]))
out_file.close()