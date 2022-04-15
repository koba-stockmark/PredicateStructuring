from chunker import ChunkExtractor

class KanyoukuExtractor:

    kanyouku_dic = [
        ["タッグ", "を", "組む"],
        ["委託", "を", "受ける"],
        ["一翼", "を", "担う"],
        ["運", "が", "いい"],
        ["影響", "を", "受ける"],
        ["影響力", "を", "持つ"],
        ["間", "も", "ない"],
        ["機能", "を", "果たす"],
        ["機能", "を", "持つ"],
        ["気", "を", "つける"],
        ["拠点", "を", "置く"],
        ["許諾", "を", "受ける"],
        ["共感", "に", "つながる"],
        ["強み", "が", "ある"],
        ["口", "を", "くわえる"],
        ["支持", "を", "受ける"],
        ["支障", "を", "きたす"],
        ["次代", "を", "担う"],
        ["主眼", "を", "置く"],
        ["手", "を", "下す"],
        ["手", "を", "取る"],
        ["手", "を", "組む"],
        ["重点", "を", "置く"],
        ["心", "が", "弾む"],
        ["身", "に", "つける"],
        ["成果", "を", "出す"],
        ["成功", "を", "収める"],
        ["先陣", "を", "切る"],
        ["知見", "を", "持つ"],
        ["知識", "を", "つける"],
        ["定評", "が", "ある"],
        ["電話", "を", "切る"],
        ["糖度", "が", "高い"],
        ["動き", "を", "見せる"],
        ["日の目", "を", "見る"],
        ["能力", "を", "持つ"],
        ["背景", "を", "受ける"],
        ["役目", "を", "終える"],
        ["理解", "を", "深める"],
        ["力", "が", "入る"],
        ["力", "を", "つける"],
        ["力", "を", "注ぐ"],
        ["力", "を", "入れる"]
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