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
        if doc[start].norm_ == '共' and doc[start - 1].lemma_ == 'と':   # 〜と共に　は並列でない
            return ret
        # 〇〇と（主語）が…　のパターン
        for i in reversed(range(0, start)):
            if sp <= i:
                continue
            if ((doc[i].pos_ == 'NOUN' or doc[i].pos_ == 'PROPN') and
                doc[i].tag_ != '名詞-普通名詞-副詞可能' and doc[i].tag_ != '接尾辞-名詞的-助数詞' and (doc[i].tag_ != '名詞-普通名詞-助数詞可能' or
                doc[i].lemma_ == '社' or doc[i].lemma_ == '課' or doc[i].lemma_ == '部' or re.compile(r'^[a-zA-Z]+$').search(doc[i].lemma_)) and (i >= ep or i < sp) or
                ((doc[i].head.head.i >= ep or doc[i].head.head.i < sp) and doc[doc[i].head.i].norm_ == '他')):
                if self.rentai_check(i, *doc):      #   連体修飾は並列から外す
                    continue
                if len(doc) > i + 1 and doc[i + 1].lemma_ == 'の' and doc[i + 1].pos_ == 'ADP':  # 〇〇の〇〇　は並列扱いしない
                    if sp <= doc[i].head.i <= ep:
                        if not find_ct:
                            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
                        return ret
                    else:
                        continue
                if (sp <= doc[i].head.i <= ep or start <= doc[i].head.i <= end) and (doc[i + 1].lemma_ == 'と' or doc[i + 1].lemma_ == 'や' or doc[i + 1].lemma_ == 'など' or doc[i + 1].norm_ == '及び' or (doc[i + 1].pos_ == 'PUNCT' and doc[i + 1].tag_ != '補助記号-括弧開')):
                    if len(doc) > i + 2 and doc[i + 1].pos_ == 'PUNCT' and doc[i + 2].lemma_ == 'を':
                        break
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
                    continue
                if doc[i + 1].pos_ == 'ADP' and (doc[i + 1].lemma_ != 'など' or (len(doc) > i + 2 and doc[i + 2].lemma_ != 'の')):
                    break
                if (doc[i].head.head.i >= ep or doc[i].head.head.i < sp) and (doc[i].pos_ == 'NOUN' or doc[i].pos_ == 'PROPN') and\
                        (doc[i + 1].lemma_ == '、' or doc[doc[i].head.i].i == i + 1) and doc[doc[i].head.i].norm_ == '他' and doc[doc[i].head.i + 1].pos_ != 'ADP':
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
                    continue
            elif doc[i].tag_ == '接尾辞-名詞的-一般':     # 派生名詞の場合
                if (sp <= doc[i].head.head.i <= ep or start <= doc[i].head.i <= end) and (doc[i + 1].lemma_ == 'と' or doc[i + 1].lemma_ == 'や' or doc[i + 1].lemma_ == 'など' or doc[i + 1].norm_ == '及び' or (doc[i + 1].pos_ == 'PUNCT' and doc[i + 1].tag_ != '補助記号-括弧開')):
                    if len(doc) > i + 2 and doc[i + 1].pos_ == 'PUNCT' and doc[i + 2].lemma_ == 'を':
                        break
                    ret.append((self.num_chunk(doc[i].head.i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1]['lemma_start']
                    ep = ret[find_ct - 1]['lemma_end']
                    continue
            elif doc[i].lemma_ == 'を' or doc[i].lemma_ == 'が' or doc[i].lemma_ == 'は' or doc[i].lemma_ == 'に' or doc[i].lemma_ == 'で':
                break
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
            for i in reversed(range(0, doc[end].head.i)):
                if i != end:
                    if doc[i].head.i == doc[end].head.i and doc[i].lemma_ == '共同':
                        ret = self.para_get(i, i, *doc)
                        return ret
            ret.append({'lemma': '', 'lemma_start': -1, 'lemma_end': -1})
        return ret


