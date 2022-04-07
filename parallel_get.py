import re
from chunker import ChunkExtractor
from subject_get import SubjectExtractor

class ParallelExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        subj_get = SubjectExtractor()
        self.rentai_check = subj_get.rentai_check



    def para_get(self, start, end, *doc):
        """
        並列句の取得
        並立対象句（startからend）に係っている名詞句を並立句とする
        """
        ret = []
        sp = start
        ep = end
        find_ct = 0
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
                    if (doc[i].head.i >= sp and doc[i].head.i <= ep):
                        if not find_ct:
                            ret.append(('', 0, 0))
                        return ret
                    else:
                        continue
#                if token.tag_ == '名詞-普通名詞-サ変可能' and (doc[token.i + 1].pos_ == 'PUNCT' or doc[token.i + 1].pos_ == 'SYM'):  # サ変名詞、〇〇　は並列扱いしない
#                    return '', 0, 0
                if (doc[i].head.i >= sp and doc[i].head.i <= ep) and (doc[i + 1].lemma_ == 'と' or doc[i + 1].lemma_ == 'や' or doc[i + 1].lemma_ == 'など' or doc[i + 1].pos_ == 'PUNCT'):
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1][1]
                    ep = ret[find_ct - 1][2]
                    continue
                if (doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ != 'など'):
                    break
                if (doc[i].head.head.i >= ep or doc[i].head.head.i < sp) and (doc[i].pos_ == 'NOUN' or doc[i].pos_ == 'PROPN') and\
                        (doc[i + 1].lemma_ == '、' or doc[doc[i].head.i].i == i + 1) and doc[doc[i].head.i].norm_ == '他' and doc[doc[i].head.i + 1].pos_ != 'ADP':
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1][1]
                    ep = ret[find_ct - 1][2]
                    continue
                if(doc[i].head.i == doc[ep].head.i and (doc[i].tag_ != '名詞-普通名詞-サ変可能' or doc[i + 1].tag_ != '補助記号-読点')):
                    ret.append((self.num_chunk(i, *doc)))
                    find_ct = find_ct + 1
                    sp = ret[find_ct - 1][1]
                    ep = ret[find_ct - 1][2]
                    continue

        if not find_ct:
            for i in reversed(range(0, doc[end].head.i)):
                if i != end:
                    if doc[i].head.i == doc[end].head.i and doc[i].lemma_ == '共同':
                        ret = self.para_get(i, i, *doc)
                        return ret
            ret.append(('', 0, 0))
        return ret


