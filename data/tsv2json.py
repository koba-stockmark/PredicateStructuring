import csv
import json
import copy


def tsv2json(self):
    with open("input.tsv", 'r') as f:
        input_news = csv.reader(f, delimiter='\t')
        o_text = ""
        out_data = []
        news_data = {}
        for row in input_news:
            news_data["media_name"] = row[0]
            news_data["text"] = row[1]
            news_data["id"] = row[2]
            news_data["preprocessed_title"] = row[3]
            out_data.append(copy.deepcopy(news_data))
    json_file = open("keisan_input.json", mode="w")
    json.dump(out_data, json_file, indent=2, ensure_ascii=False)
    json_file.close()
