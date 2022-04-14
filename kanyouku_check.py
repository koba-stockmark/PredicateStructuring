from chunker import ChunkExtractor

class KanyoukuExtractor:

    kanyouku_dic = [
        ["力", "を", "入れる"],
        ["力", "が", "入る"],
        ["日の目", "を", "見る"]
    ]

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word
        self.num_chunk = chunker.num_chunk
        self.compaound = chunker.compaound


    def kanyouku_chek(self, pt, *doc):
        pass_data = []
        for chek_kannyouku in self.kanyouku_dic:
            chek_pt = pt
            c_pt = 0
            find_f = False
            for chek_w in chek_kannyouku:
                find_f = False
                for i in range(c_pt, chek_pt + 1):
                    if doc[i].norm_ == chek_w and (i == pt or doc[i].head.i == pt or doc[i].head.i in pass_data):
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