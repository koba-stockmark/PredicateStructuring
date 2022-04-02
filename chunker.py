import re
from pyknp import KNP

class ChunkExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        self.knp = KNP()  # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)



    """
    headを辿ってc_ptがh_ptにたどり着くかのチェック
    つながる場合はc_ptはh_ptの修飾部
    """

    def head_connect_check(self, h_pt, c_pt, *doc):
        if h_pt == c_pt:
            return True
        head_pt = doc[c_pt].head.i
        while doc[head_pt].i != doc[head_pt].head.i:
            if h_pt == head_pt:
                return True
            else:
                head_pt = doc[head_pt].head.i
        return False

    """
    表層格の獲得
    """
    def case_get(self, pt, *doc):
        for token in doc[pt:]:
            if token.dep_ == "case":
                if(doc[token.i + 1].dep_ == "case"):
                    return token.lemma_ + token.head.lemma_
                else:
                    return token.lemma_
            if token.pos_ == "AUX" or token.pos_ == "VERB" or token.pos_ == "ADV" or token.pos_ == "ADJ" or token.pos_ == "DET" or token.pos_ == "PUNCT":
                return token.pos_
        return ''

    """
    KNPによるモダリティー処理
    """
    def modality_get(self, text):

        result = self.knp.parse(text)
        ret = []
        for tag in result.tag_list():  # 各基本句へのアクセス
            ret = ret + re.findall("<時制.+?>", tag.fstring)
            ret = ret + re.findall("<モダリティ.+?>", tag.fstring)
        return ret


    """
    動詞のチャンキング
        複合動詞は作るが助動詞は接続しない
        return  = [チャンク原型　チャンク原型スタート　チャンク原型エンド　動詞句　動詞句スタート　動詞句エンド モダリティ]
    """

    def verb_chunk(self, pt, *doc):
        start_pt = pt
        end_pt = pt
        pre = ''
        for i in reversed(range(0, pt)):
            if (pt == doc[i].head.i or pt == doc[i].head.head.i) and doc[i].pos_ != 'PUNCT' and doc[i].tag_ != '接頭辞' and (doc[i].pos_ != 'AUX' or doc[i].orth_ == 'する') and\
                    (doc[i].pos_ != 'ADP' or (doc[i].tag_ == '助詞-副助詞' and doc[i].lemma_ != 'まで')) and doc[i].pos_ != 'ADV' and doc[i].pos_ != 'ADJ' and doc[i].pos_ != 'SCONJ' and\
                    doc[i].norm_ != 'から' and\
                    doc[i].tag_ != '名詞-普通名詞-副詞可能' and doc[i].tag_ != '名詞-普通名詞-助数詞可能' and doc[i].tag_ != '接尾辞-名詞的-助数詞' and doc[i].tag_ != '名詞-普通名詞-助数詞可能':
                pre = doc[i].orth_ + pre
                start_pt = i
            elif len(doc) > i + 1 and doc[i].pos_ == 'ADJ' and doc[i + 1].lemma_ == 'する':    # 形容詞　＋　する
                pre = doc[i].orth_ + pre
                start_pt = i
            elif i != 0 and (doc[i].tag_ == '補助記号-読点' and doc[i - 1].head.i == doc[i].i + 1 and doc[i - 1].tag_ != '名詞-普通名詞-助数詞可能'):      # 〇〇、〇〇する　などの並列術部
                pre = doc[i].orth_ + pre
                start_pt = i
            else:
                break
        find_f = False
        append_o = ''
        append_l = ''
        tail_o = ''
        tail_ct = 0
        ret = ''
        for token in doc[pt + 1:]:
            if (tail_ct == 0 and pt == token.head.i and token.pos_ != 'ADP'  and token.pos_ != 'SCONJ'  and token.pos_ != 'PART'  and token.pos_ != 'AUX' and token.pos_ != 'VERB' and token.pos_ != 'PUNCT' and token.pos_ != 'SYM'):
                if(find_f):
                    ret = ret + append_o
                find_f = True
                append_o = token.orth_
                append_l = token.lemma_
                end_pt = end_pt + 1
            # 動詞　＋　接尾辞
            elif (tail_ct == 0 and token.head.i == token.head.head.i and (token.tag_ == '接尾辞-名詞的-サ変可能' or (token.pos_ == 'VERB' and token.tag_ == '名詞-普通名詞-サ変可能'))):
                if(find_f):
                    ret = ret + append_o
                find_f = True
                append_o = token.orth_
                append_l = token.lemma_
                end_pt = end_pt + 1
            # 読点による述部の並列　「森の箱」を開発、受注販売を始めた。
            elif tail_ct == 0 and ((token.tag_ == '補助記号-読点' and pt == token.head.i and doc[token.i - 1].tag_ == '名詞-普通名詞-サ変可能' and (self.case_get(doc[token.i + 1].i, *doc) == 'を' or self.case_get(doc[token.i + 1].i, *doc) == 'VERB')) or
                                   ((self.case_get(doc[token.i].i, *doc) == 'を' or self.case_get(doc[token.i].i, *doc) == 'VERB') and find_f == True and doc[token.i].pos_ != 'AUX' and doc[token.i].pos_ != 'ADP')):
                if (find_f):
                    ret = ret + append_o
                find_f = True
                append_o = token.orth_
                append_l = token.lemma_
                end_pt = end_pt + 1
            # 語幹以外の助動詞部の追加
            elif(token.pos_ == 'AUX' or token.pos_ == 'SCONJ' or token.pos_ == 'VERB'  or token.pos_ == 'PART' or token.pos_ == 'ADJ' or token.tag_  ==  '名詞-普通名詞-サ変可能'):          # 句情報用に助動詞を集める。  〇〇開始　〇〇する計画　などの時制も　含める
                tail_o = tail_o + token.orth_
                tail_ct = tail_ct + 1
            else:
                break
        if(find_f):
            ret_lemma = pre + doc[pt].orth_ + ret + append_l
            org_str = pre + doc[pt].orth_ + ret + append_o + tail_o
        else:
            ret_lemma = pre + doc[pt].lemma_
            org_str = pre + doc[pt].orth_ + append_o + tail_o
#        return ret_lemma, start_pt, end_pt, org_str, start_pt, end_pt + tail_ct
#        print('◎',org_str, *self.modality_get(org_str))
#        return ret_lemma, start_pt, end_pt, org_str, start_pt, end_pt + tail_ct, *self.modality_get(org_str)
        return {'lemma':ret_lemma, 'lemma_start':start_pt, 'lemma_end':end_pt, 'org_str':org_str, 'org_start':start_pt, 'org_end':end_pt + tail_ct, 'modality':[*self.modality_get(org_str)]}

    """
    名詞のチャンキング
    """

    def num_chunk(self, pt, *doc):
        start_pt = pt
        end_pt = pt
        ret = doc[pt].orth_
        if doc[pt].lemma_ == 'こと' or doc[pt].lemma_ == '人' or doc[pt].lemma_ == 'もの' or doc[pt].lemma_ == 'とき' or doc[pt].lemma_ == 'ため' or doc[pt].lemma_ == '方':
            if (doc[pt + 1].tag_ == '補助記号-括弧閉' or doc[pt + 1].lemma_ == '＂') and doc[pt + 1].head.i == doc[pt].i:
                ret = ret + doc[pt + 1].orth_
                for i in reversed(range(0, pt)):
                    if doc[i].tag_ == '補助記号-括弧開':
                        start_pt = i
                        ret = doc[i].orth_ + ret
                        break
                    start_pt = i
                    ret = doc[i].orth_ + ret
                for i in reversed(range(0, i)):
                    if doc[i].pos_ != 'ADP' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点':
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    elif (doc[i].orth_ == 'の' or (doc[i].orth_ == 'に' and doc[i + 1].lemma_ == 'する')):
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    elif doc[i].orth_ == 'て' and doc[i + 1].tag_ == '動詞-非自立可能':     # 〜していること
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    else:
                        break
            else:
                for i in reversed(range(0, pt)):
                    if doc[i].pos_ != 'ADP' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点':
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    elif (doc[i].orth_ == 'の' or (doc[i].orth_ == 'に' and doc[i + 1].lemma_ == 'する')):
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    elif doc[i].orth_ == 'て' and doc[i + 1].tag_ == '動詞-非自立可能':     # 〜していること
                        ret = doc[i].orth_ + ret
                        start_pt = i
                    else:
                        break
        # 動詞の名詞化
        elif (doc[pt].pos_ == 'VERB'):
            for token in doc[0:]:
                if(token.head.i == pt):
                    start_pt = token.i
                    break
            for i in reversed(range(start_pt, pt)):
                ret = doc[i].orth_ + ret
        # 一般の名詞
        else:
            punc_o_f = False
            punc_c_f = False
            punc_ct = 0
            # 後方のチャンク
            for token in doc[pt+1:]:
                if (self.head_connect_check(pt, token.head.i, *doc)):
                    if not punc_o_f:
                        if (token.pos_ == 'ADP' and (token.lemma_ == 'を' or token.lemma_ == 'は' or token.lemma_ == 'が' or token.lemma_ == 'で' or token.lemma_ == 'も' or token.lemma_ == 'に' or token.lemma_ == 'にて')):  # 名詞の名詞　名詞と名詞　は接続させたい
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'と' and doc[token.i + 1].tag_ == '補助記号-読点'):    # 名詞と、名愛　は切り離す　
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'と'):    # 名詞と名詞　は切り離して並列処理にまかせる
                            break
                        if token.lemma_ == '。' or token.lemma_ == '、':
                            break
                    if token.tag_ == '補助記号-括弧閉':
                        if punc_o_f:
                            punc_o_f = False
                            punc_c_f = False
                        else:
                            punc_c_f = True
                        punc_ct = punc_ct + 1
                    elif not punc_c_f and token.tag_ == '補助記号-括弧開':
                        punc_ct = punc_ct - 1
                        punc_o_f = True
                    end_pt = end_pt + 1
                    ret = ret + token.orth_
            # 前方のチャンク
            for i in reversed(range(0, pt)):
                if pt < doc[i].head.i and doc[i].head.i != doc[pt].head.i:
                    break
                if punc_c_f and not punc_o_f:
                    if doc[i].tag_ != '補助記号-括弧開':
                        start_pt = i
                        ret = doc[i].orth_ + ret
                        if doc[i].tag_ == '補助記号-括弧閉':
                            punc_c_f = True
                            punc_ct = punc_ct + 1
                        continue
                    else:
                        punc_ct = punc_ct - 1
                        if(punc_ct != 0):
                            start_pt = i
                            ret = doc[i].orth_ + ret
                            continue
                    punc_o_f = False
                    punc_c_f = False
                elif not punc_c_f and not punc_o_f:
                    if doc[i].tag_ == '補助記号-括弧開':
                        break
                if(doc[i].head.i == pt and doc[i].pos_ != 'VERB' and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'DET' and doc[i].tag_ != '補助記号-読点' and
                        (doc[i].tag_ != '名詞-普通名詞-副詞可能' or doc[i].lemma_ != 'なか')):
                    if doc[i].tag_ == '補助記号-括弧開':
                        punc_o_f = True
                    if doc[i].tag_ == '補助記号-括弧閉':
                        punc_ct = punc_ct + 1
                        punc_c_f = True
                    start_pt = i
                    ret = doc[i].orth_ + ret
                elif (doc[i].pos_ != 'DET' and doc[i].pos_ != 'VERB'  and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'SCONJ' and doc[i].pos_ != 'PART' and doc[i].pos_ != 'PRON' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点' and
                        (doc[i].pos_ != 'ADP' or doc[i].orth_ == 'の' or doc[i].orth_ == 'や' or doc[i].orth_ == 'と' or                  # 名詞　＋　の[や]　＋　〇〇
                         (doc[i].pos_ == 'ADP' and doc[i + 1].orth_ == 'の'))):                                                           # 名詞 +  格助詞　＋　の　＋　〇〇
                    if (doc[i].orth_ == 'の' and (doc[i - 1].pos_ == 'ADP' or doc[i - 1].pos_ == 'SCONJ') and (doc[i - 2].pos_ == 'VERB' or doc[i - 2].pos_ == 'AUX')):  # 動詞 +  助詞　＋　の　/　〇〇     前が動詞の場合は「〜の」の連体修飾では繋げない
                        break
                    if(doc[i].pos_ == 'SYM' and doc[i].lemma_ == '〜'):
                        break
                    if doc[i].pos_ == 'SYM' and doc[i].tag_ == '助詞-格助詞':      # 〜　が格助詞の朱鷺　
                        break
                    if(doc[i].pos_ == 'SYM' and (not self.head_connect_check(pt, doc[i].head.i, *doc) and doc[pt].head.i !=  doc[i].head.i)):
                        break
                    if(doc[i].tag_ == '接尾辞-名詞的-助数詞' and (doc[i].lemma_ == '日' or doc[i].lemma_ == '月' or doc[i].lemma_ == '年')):
                        break
                    if doc[i].orth_ == 'の' and doc[i - 1].lemma_ == 'ため':
                        break
                    if doc[i].tag_ == '名詞-普通名詞-副詞可能' and (doc[i].lemma_ == 'なか' or  doc[i].lemma_ == 'ため' or doc[i].lemma_ == 'もと' ):
                        break
                    if(doc[i].pos_ == 'ADJ' and not self.head_connect_check(pt, i, *doc)):   # objを修飾しない形容詞
                        break
                    if(doc[i].pos_ == 'CCONJ' and doc[i].norm_ != '及び'):
                        break
                    if not self.head_connect_check(pt, i, *doc) and doc[pt].head.i != doc[i].head.i:
                        break
#                    if(doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と'):
#                        break
                    if doc[i].tag_ == '補助記号-括弧閉':
                        punc_ct = punc_ct + 1
                        punc_c_f = True
                    start_pt = i
                    ret = doc[i].orth_ + ret
#                elif (doc[i].pos_ == 'VERB' or doc[i].pos_ == 'AUX' and (doc[i + 1].orth_ == 'ため' or doc[i + 1].orth_ == 'もの' or doc[i + 1].orth_ == 'とき' or doc[i + 1].orth_ == '人')):
#                    start_pt = i
#                    ret = doc[i].orth_ + ret
                elif((doc[i].pos_ == 'VERB' and doc[i + 1].pos_ == 'AUX' and doc[i + 2].orth_ == 'か') or
                    ((doc[i].pos_ == 'AUX' or doc[i].pos_ == 'VERB') and doc[i + 1].orth_ == 'か')):  # 〇〇か〇〇
                    start_pt = i
                    ret = doc[i].orth_ + ret
                #elif(doc[i].tag_ == '補助記号-読点' and (doc[i + 1].tag_ == '補助記号-括弧開' or doc[i - 1].tag_ == '補助記号-括弧閉' or doc[i - 1].orth_ == '株式会社') and
                elif (doc[i].tag_ == '補助記号-読点' and (doc[i + 1].tag_ == '補助記号-括弧開' or doc[i - 1].tag_ == '補助記号-括弧閉') and
                        (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
                    start_pt = i
                    ret = doc[i].orth_ + ret
#                elif(doc[i].pos_ == 'PUNCT' and doc[i - 1].pos_ != 'VERB'  and doc[i - 1].pos_ != 'ADV'  and doc[i - 1].pos_ != 'ADP' and
#                     doc[i - 1].tag_ != '名詞-普通名詞-副詞可能' and doc[i - 1].tag_ != '接尾辞-名詞的-助数詞' and
#                     doc[i - 1].tag_ != '名詞-普通名詞-助数詞可能' and doc[i - 1].tag_ != '名詞-数詞' and
#                     (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
#                    start_pt = i
#                    ret = doc[i].orth_ + ret
                elif(doc[i].pos_ == 'ADP' and doc[i].orth_ == 'に' and doc[i + 1].orth_ == 'なる'):
                    start_pt = i
                    ret = doc[i].orth_ + ret
                else:
                     break
            #      print(doc[pt].orth_)
            #      return doc[pt].orth_
        return ret, start_pt, end_pt