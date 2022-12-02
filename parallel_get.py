import re
from chunker import ChunkExtractor

class ParallelExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.rentai_check = chunker.rentai_check



    para_ng_word = ["合弁", "競合", "共同", "同盟", "統合", "連合"]
    def para_get(self, start, end, *doc):
        """
        並列句の取得
        並立対象句（startからend）に係っている名詞句を並立句とする
        """
        ret = []
        sp = start
        ep = end
        find_ct = 0
        subject_f = False
        if doc[start].lemma_ in self.para_ng_word:
            subject_f = True
#            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
#            return ret
        no_word = ""
#        """
        if doc[ep].tag_ == "名詞-普通名詞-サ変可能":
            stop_f = False
            for pt in range(sp, ep):
                if stop_f:
                    break
                re_katakana = re.compile(r'[\u30A1-\u30F4ー]+')
                if doc[pt].lemma_ == "・" and not re_katakana.fullmatch(doc[pt - 1].lemma_):
                    for ppt in range(pt, ep):
                        if doc[ppt].lemma_ == "の":
                            no_word = ""
                            break
                    if not no_word:
                        break
                if doc[pt].lemma_ == "の" and doc[pt].pos_ == "ADP" and doc[pt - 1].pos_ != "ADP":
                    if doc[pt - 1].tag_ == "名詞-普通名詞-サ変可能":
                        no_word = ""
                        continue
                    for npt in range(pt, ep + 1):
                        no_word = no_word + doc[npt].orth_
                        if doc[npt].lemma_ == "の" and npt != pt:
                            no_word = ""
                            stop_f = True
                            break
        #       """
        # 〇〇と（主語）が…　のパターン
        for cpt in reversed(range(0, start)):
            if doc[cpt].lemma_ == "なか" and doc[cpt + 1].pos_ != "ADP":  # 〇〇のなか、…
                continue
#            if (sp > cpt or cpt > ep) and (start <= doc[cpt].head.i <= end or sp <= doc[cpt].head.i <= ep or (doc[cpt].head.i == doc[end].head.i and doc[cpt + 1].lemma_ == 'と')):
            if (sp > cpt or cpt > ep) and (start <= doc[cpt].head.i <= end or sp <= doc[cpt].head.i <= ep):
                if (doc[cpt].pos_ == 'CCONJ' or doc[cpt].pos_ == 'SCONJ' or doc[cpt].pos_ == 'PUNCT' or doc[cpt].pos_ == 'ADP' or doc[cpt].pos_ == 'DET' or doc[cpt].pos_ == 'AUX' or
                        ((doc[cpt].pos_ == 'VERB' or doc[cpt].pos_ == 'ADJ' or doc[cpt].pos_ == 'ADV') and (len(doc) <= cpt + 1 or doc[cpt + 1].tag_ != '接尾辞-名詞的-一般'))):
                    continue
                if len(doc) > cpt + 1 and (doc[cpt + 1].pos_ == 'VERB' or doc[cpt + 1].tag_ == '動詞-非自立可能'):
                    continue
#                if doc[cpt].tag_ != '名詞-普通名詞-副詞可能' and doc[end].tag_ == '名詞-普通名詞-副詞可能':     # 誤解析対応　山形空港と庄内空港は3月1日から、それぞれ空港ビル1階ロビーにモバイルバッテリーのレンタルスタンド「ChargeSPOT」を設置する
#                    continue
                chek = self.num_chunk(cpt, *doc)
                chek["subject"] = subject_f
                if subject_f:
                    chek["dummy"] = False
                if "の" not in chek["lemma"] and "な" not in chek["lemma"] and (doc[chek["lemma_end"] + 1].lemma_ != "など" or doc[chek["lemma_end"] + 2].lemma_ != "に") and no_word:
                    chek["lemma"] = chek["lemma"] + no_word
                elif "の" in chek["lemma"]:
                    if doc[chek["lemma_end"]].tag_ == "名詞-普通名詞-サ変可能":
                        no_word = ""
                        for pt in range(chek["lemma_start"], chek["lemma_end"]):
                            if doc[pt].lemma_ == "の" and doc[pt].pos_ == "ADP" and doc[pt - 1].pos_ != "ADP":
                                if no_word:
                                    no_word = ""
                                    break
                                for npt in range(pt, chek["lemma_end"] + 1):
                                    no_word = no_word + doc[npt].orth_

                """ 慣用句的(fixed)な連体修飾関係
                if doc[chek["lemma_start"] - 1].dep_ == "fixed" and (doc[chek["lemma_start"] - 1].morph.get("Inflection") and '連体形' in doc[chek["lemma_start"] - 1].morph.get("Inflection")[0]):
                    for v_c in reversed(range(0, chek["lemma_start"] - 2)):
                        if "助詞" in doc[v_c].tag_:
                            continue
                        v_chunk = self.verb_chunk(v_c, *doc)
                        chek["lemma_start"] = v_chunk["lemma_start"]
                        chek["lemma"] = ""
                        for v_p in range(chek["lemma_start"], chek["lemma_end"] + 1):
                            chek["lemma"] = chek["lemma"] + doc[v_p].orth_
                        break
                """
                if (len(doc) > chek["lemma_end"] + 1 and ((doc[chek["lemma_end"] + 1].lemma_ == 'と' and doc[chek["lemma_end"] + 2].lemma_ != 'の') or doc[chek["lemma_end"] + 1].lemma_ == 'や' or doc[chek["lemma_end"] + 1].norm_ == '及び' or doc[chek["lemma_end"] + 1].norm_ == 'など' or
                        (len(doc) > chek["lemma_end"] + 2 and doc[chek["lemma_end"] + 1].norm_ == 'を' and doc[chek["lemma_end"] + 2].norm_ == 'はじめ') or
                        doc[chek["lemma_end"] + 1].tag_ == '補助記号-読点')):
#                    ret.append((self.num_chunk(cpt, *doc)))
                    ret.append(chek)
                    find_ct = find_ct + 1
                    """
#                     〇〇や〇〇の〇〇　　曖昧なので難しい
                    if doc[chek["lemma_start"] - 1].lemma_ == "や":
                        ret_para = self.num_chunk(chek["lemma_start"] - 2, *doc)
                        if "の" in chek["lemma"] and "の" not in ret_para["lemma"]:
                            of_f = False
                            for i in range(chek["lemma_start"], chek["lemma_end"] + 1):
                                if of_f or doc[i].lemma_ == "の" or (doc[i + 1].lemma_ == "の" and doc[i].pos_ == "ADP"):
                                    of_f = True
                                    ret_para["lemma"] = ret_para["lemma"] + doc[i].orth_
                            ret.append(ret_para)
                            find_ct = find_ct + 1
                    """
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
#                    if no_word and doc[chek["lemma_end"] + 1].lemma_ == 'や' and "の" not in ret[find_ct - 1]["lemma"]:
#                        ret[find_ct - 1]["lemma"] = ret[find_ct - 1]["lemma"] + no_word
        # （主語1）が（主語2）と…　のパターン
        if len(doc) > end + 1 and doc[end + 1].lemma_ == 'が':
            for i in range(end + 1, doc[end].head.i):
                if doc[i].tag_ == '名詞-数詞' or doc[i].tag_ == '名詞-普通名詞-助数詞可能' or doc[i].tag_ == '名詞-普通名詞-副詞可能':
                    break
                if doc[i + 1].pos_ == 'ADV':
                    break
                if len(doc) > i + 1 and doc[i + 1].lemma_ == 'の' and doc[i + 1].pos_ == 'ADP':  # 〇〇の〇〇　は並列扱いしない
                    if sp <= doc[i].head.i <= ep:
                        if not find_ct:
                            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1, "subject": False})
                        return ret
                    else:
                        continue
                if doc[i].head.i == doc[end].head.i and (doc[i + 1].lemma_ == 'と' or doc[i + 1].lemma_ == 'や' or doc[i + 1].norm_ == '及び' or (doc[i + 1].lemma_ == 'など' and (doc[i + 2].lemma_ == 'と' or doc[i + 2].lemma_ == 'や' or doc[i + 2].norm_ == '及び' or doc[i + 2].pos_ != 'ADP')) or (doc[i + 1].lemma_ == '、' and doc[i + 2].pos_ != 'ADP')) and doc[i + 2].lemma_ != 'する' and doc[i + 2].lemma_ != 'なる':
                    if doc[i].head.i != doc[end].head.i:
                        continue
                    chek = self.num_chunk(i, *doc)
                    chek["subject"] = subject_f
                    if subject_f:
                        chek["dummy"] = False
#                    ret.append((self.num_chunk(i, *doc)))
                    ret.append(chek)
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
#                    if no_word and doc[i + 1].lemma_ == 'や' and "の" not in ret[find_ct - 1]["lemma"]:
#                        ret[find_ct - 1]["lemma"] = ret[find_ct - 1]["lemma"] + no_word
                    continue
                if doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ != 'など':
                    break
        if not find_ct:
            if len(doc) > end + 1 and (doc[end + 1].dep_ == 'case' and doc[end + 1].lemma_ != 'は' and doc[end + 1].lemma_ != 'と' and doc[end + 1].lemma_ != 'が'):
                return ret
#            for i in reversed(range(0, doc[end].head.i)):
#                if i != end:
#                    if doc[i].head.i == doc[end].head.i and doc[i].lemma_ == '共同':
#                        ret = self.para_get(i, i, *doc)
#                        return ret
            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1, "subject": False})
        return ret


