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
            c_pt = 0
            find_f = False
            for chek_w in chek_kannyouku:
                find_f = False
                chek_w2 = chek_w
                chek_w3 = chek_w
                if chek_w == "が":
                    chek_w2 = "も"
                    chek_w3 = "は"
                for i in range(c_pt, chek_pt + 1):
                    if ((doc[i].norm_ == chek_w or doc[i].norm_ == chek_w2 or doc[i].norm_ == chek_w3) and
                            (i == pt or doc[i].head.i == pt or doc[i].head.head.i == pt or doc[i].head.i in pass_data or doc[i].head.i == doc[i].i + 1)):
                        pass_data.append(i)
                        c_pt = i + 1
                        find_f = True
                        break
                if not find_f:
                    break
            if find_f:
                break
            pass_data = []
        return pass_data

    def kanyouku_get(self, kanyouku_pass, *doc):
        ret = ''
        for i in kanyouku_pass:
            if i == kanyouku_pass[-1]:
                ret = ret + doc[i].lemma_
            else:
                ret = ret + doc[i].orth_
        return ret
