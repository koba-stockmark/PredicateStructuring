import re
from chunker import ChunkExtractor

class ParallelExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.rentai_check = chunker.rentai_check



    def para_get(self, start, end, *doc):
        """
        並列句の取得
        並立対象句（startからend）に係っている名詞句を並立句とする
        """
        ret = []
        sp = start
        ep = end
        find_ct = 0
        if doc[start].lemma_ == '共同':
            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
            return ret
        # 〇〇と（主語）が…　のパターン
        for cpt in reversed(range(0, start)):
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
                if (len(doc) > chek["lemma_end"] + 1 and ((doc[chek["lemma_end"] + 1].lemma_ == 'と' and doc[chek["lemma_end"] + 2].lemma_ != 'の') or doc[chek["lemma_end"] + 1].lemma_ == 'や' or doc[chek["lemma_end"] + 1].norm_ == '及び' or doc[chek["lemma_end"] + 1].norm_ == 'など' or
                        (len(doc) > chek["lemma_end"] + 2 and doc[chek["lemma_end"] + 1].norm_ == 'を' and doc[chek["lemma_end"] + 2].norm_ == 'はじめ') or
                        doc[chek["lemma_end"] + 1].tag_ == '補助記号-読点')):
                    ret.append((self.num_chunk(cpt, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
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
                            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
                        return ret
                    else:
                        continue
                if doc[i].head.i == doc[end].head.i and (doc[i + 1].lemma_ == 'と' or doc[i + 1].lemma_ == 'や' or doc[i + 1].norm_ == '及び' or (doc[i + 1].lemma_ == 'など' and (doc[i + 2].lemma_ == 'と' or doc[i + 2].lemma_ == 'や' or doc[i + 2].norm_ == '及び' or doc[i + 2].pos_ != 'ADP')) or (doc[i + 1].lemma_ == '、' and doc[i + 2].pos_ != 'ADP')) and doc[i + 2].lemma_ != 'する' and doc[i + 2].lemma_ != 'なる':
                    if doc[i].head.i != doc[end].head.i:
                        continue
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
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
            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
        return ret


