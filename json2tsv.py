import json


import json

out_file = open('news_out.tsv', 'w')

d = {}
f = open("news_out.json", mode="r")
j_data = json.load(f)
for d in j_data:
    print("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (d["id"], d["soshiki"], d["busho"], d["title"], d["title_type"], d["head"].replace('\t', '\\t'), d["head_type"]))
    out_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (d["id"], d["soshiki"], d["busho"], d["title"], d["title_type"], d["head"].replace('\t', '\\t'), d["head_type"]))
out_file.close()

