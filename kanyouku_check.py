from chunker import ChunkExtractor
from kanyouku_dic import KanyoukuDic


class KanyoukuExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word
        self.num_chunk = chunker.num_chunk
        self.compaound = chunker.compaound

    def kanyouku_chek(self, pt, *doc):
        k_dic = KanyoukuDic
        pass_data = []
        for chek_kannyouku in k_dic.kanyouku_dic:
            chek_pt = pt
            find_f = False
            chek_w_pt = len(chek_kannyouku) - 1
            while chek_pt > 0 and chek_w_pt >= 0:
                chek_w = chek_kannyouku[chek_w_pt]
                chek_w2 = chek_w
                chek_w3 = chek_w
                if chek_w == "が":
                    chek_w2 = "も"
                    chek_w3 = "は"
                if ((doc[chek_pt].norm_ == chek_w or doc[chek_pt].norm_ == chek_w2 or doc[chek_pt].norm_ == chek_w3) and
                        (chek_pt == pt or doc[chek_pt].head.i == pt or doc[chek_pt].head.head.i == pt) and
                        (not pass_data or doc[chek_pt].head.i in pass_data or doc[chek_pt].i + 1 in pass_data or doc[chek_pt].head.i == doc[pt].head.i)):
                    pass_data.append(chek_pt)
                    chek_w_pt = chek_w_pt - 1
                    chek_pt = chek_pt - 1
                    find_f = True
                    continue
                elif find_f and (doc[chek_pt].head.i == doc[chek_pt - 1].head.i or doc[chek_pt].head.i == doc[pt].head.i):
                    chek_pt = chek_pt - 1
                    continue
                else:
                    find_f = False
                    pass_data = []
                    break
            if find_f:
                break
            pass_data = []
        return pass_data[::-1]

    def kanyouku_get(self, kanyouku_pass, *doc):
        ret = ''
        for i in kanyouku_pass:
            if i == kanyouku_pass[-1]:
                ret = ret + doc[i].lemma_
            else:
                ret = ret + doc[i].orth_
        return ret
