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
        ret = ''
        open_f = False
        for token in doc[pt:]:
            if token.tag_ == '補助記号-括弧開' or open_f:
                if token.tag_ == '補助記号-括弧閉':
                    open_f = False
                else:
                    if token.tag_ == '補助記号-括弧開' and open_f:  # ２個めの左カッコが来たらエラー
                        break
                    else:
                        open_f = True
                continue
            if len(doc) > token.i + 2 and doc[token.i + 1].tag_ == '補助記号-句点' and doc[token.i + 2].tag_ == '補助記号-括弧閉':
                continue
            if token.dep_ == "case" and token.head.i == pt and len(doc) > token.i + 1 and doc[token.i + 1].tag_ != '補助記号-括弧閉':
                for i in range(token.i, len(doc)):
                    if doc[i].dep_ == "case":
                        ret = ret + doc[i].lemma_
                    else:
                        return ret
            elif token.dep_ == "case" and token.head.head.i == pt and token.head.pos_ == 'NOUN':  # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                for i in range(token.i, len(doc)):
                    if doc[i].dep_ == "case":
                        ret = ret + doc[i].lemma_
                    else:
                        return ret
#            elif token.dep_ == "case" and token.head.head.i == doc[pt].head.i:    # 括弧書きを挟んだ係り受けの場合　ex.新事業としてフローズンミール定期配送サービス「nonpi A.R.U.」を開始すると発表した。
#               for i in range(token.i, len(doc)):
#                    if doc[i].dep_ == "case":
#                        ret = ret + doc[i].lemma_
#                    else:
#                        return ret
        if open_f and not ret:  # カッコのバランスが悪い場合は、カッコ内も対象にする
            for token in doc[pt:]:
                if len(doc) > token.i + 2 and doc[token.i + 1].tag_ == '補助記号-句点' and doc[token.i + 2].tag_ == '補助記号-括弧閉':
                    continue
                if token.dep_ == "case" and token.head.i == pt and len(doc) > token.i + 1 and doc[token.i + 1].tag_ != '補助記号-括弧閉':
                    for i in range(token.i, len(doc)):
                        if doc[i].dep_ == "case":
                            ret = ret + doc[i].lemma_
                        else:
                            return ret
                elif token.dep_ == "case" and token.head.head.i == pt and token.head.pos_ == 'NOUN':    # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                    for i in range(token.i, len(doc)):
                        if doc[i].dep_ == "case":
                            ret = ret + doc[i].lemma_
                        else:
                            return ret
        return ret

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
    英語スペースを考慮した単語結合
    """

    def connect_word(self, str1, str2):
        if not str1 or not str2:
            return str1 + str2
        if re.compile(r'^[a-zA-Z]+$').search(str1[-1]) and re.compile(r'^[a-zA-Z]+$').search(str2[0]):
            return str1 + ' ' + str2
        else:
            return str1 + str2

    """
    始点から終点までの単語の結合
    """
    def compaound(self, start, end, *doc):
        ret = ''
        for i in range(start, end):
            ret = self.connect_word(ret, doc[i].orth_)
        ret = ret + doc[end].lemma_
        return ret

    """
    動詞のチャンキング
        複合動詞は作るが助動詞は接続しない
        return  = [チャンク原型　チャンク原型スタート　チャンク原型エンド　動詞句　動詞句スタート　動詞句エンド モダリティ]
    """

    def verb_chunk(self, pt, *doc):
        start_pt = pt   # 始点
        end_pt = pt     # 終点
        pre = ''        # 前方文字
        # 前方を結合
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
            elif (len(doc) > i + 1 and doc[i - 1].pos_ == 'ADJ' and doc[i].orth_ == 'に' and doc[i + 1].lemma_ == 'する') or\
                    (len(doc) > i + 2 and doc[i].pos_ == 'ADJ' and doc[i + 1].orth_ == 'に' and doc[i + 2].lemma_ == 'する'):  # 形容動詞　＋　に　＋　する
                pre = doc[i].orth_ + pre
                start_pt = i
            elif i != 0 and (doc[i].tag_ == '補助記号-読点' and doc[i - 1].head.i == doc[i].i + 1 and doc[i - 1].tag_ != '名詞-普通名詞-助数詞可能' and doc[i - 1].tag_ != '接尾辞-名詞的-助数詞'):      # 〇〇、〇〇する　などの並列術部
                pre = doc[i].orth_ + pre
                start_pt = i
            else:
                break
        # 後方を結合
        find_f = False  # すでに結合する対象が見つかっているか否か。見つかっている場合は残りの付属語を収集
        append_o = ''   # 追加表記
        append_l = ''   # 追加原型
        tail_o = ''     # モダリティ解析用の付属語
        tail_ct = 0     # 末尾単語数
        ret = ''        # チャンク結果
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
                ret = self.connect_word(ret, doc[pt + 1].orth_)
                for i in reversed(range(0, pt)):
                    if doc[i].tag_ == '補助記号-括弧開':
                        start_pt = i
                        ret = self.connect_word(doc[i].orth_, ret)
                        break
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
                for i in reversed(range(0, i)):
                    if doc[i].pos_ != 'ADP' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点':
                        ret = self.connect_word(doc[i].orth_, ret)
                        start_pt = i
                    elif (doc[i].orth_ == 'の' or (doc[i].orth_ == 'に' and doc[i + 1].lemma_ == 'する')):
                        ret = self.connect_word(doc[i].orth_, ret)
                        start_pt = i
                    elif doc[i].orth_ == 'て' and doc[i + 1].tag_ == '動詞-非自立可能':     # 〜していること
                        ret = self.connect_word(doc[i].orth_, ret)
                        start_pt = i
                    else:
                        break
            else:
                for i in reversed(range(0, pt)):
                    if doc[i].pos_ != 'ADP' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点':
                        ret = self.connect_word(doc[i].orth_, ret)
                        start_pt = i
                    elif (doc[i].orth_ == 'の' or (doc[i].orth_ == 'に' and doc[i + 1].lemma_ == 'する')):
                        ret = self.connect_word(doc[i].orth_, ret)
                        start_pt = i
                    elif doc[i].orth_ == 'て' and doc[i + 1].tag_ == '動詞-非自立可能':     # 〜していること
                        ret = self.connect_word(doc[i].orth_, ret)
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
                ret = self.connect_word(doc[i].orth_, ret)
        # 一般の名詞
        else:
            punc_o_f = False
            punc_c_f = False
            punc_ct = 0
            # 後方のチャンク
            for token in doc[pt+1:]:
                if (self.head_connect_check(pt, token.head.i, *doc)) or punc_ct < 0:
                    if not punc_o_f:
                        if (token.pos_ == 'ADP' and (token.lemma_ == 'を' or token.lemma_ == 'は' or token.lemma_ == 'が' or token.lemma_ == 'で' or token.lemma_ == 'も' or token.lemma_ == 'に' or token.lemma_ == 'にて' or token.orth_ == 'で' or token.orth_ == 'より')):  # 名詞の名詞　名詞と名詞　は接続させたい
                            if len(doc) > token.i + 1 and doc[token.i + 1].tag_ != '補助記号-括弧閉':
                                break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'と' and doc[token.i + 1].tag_ == '補助記号-読点'):    # 名詞と、名愛　は切り離す　
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'と'):    # 名詞と名詞　は切り離して並列処理にまかせる
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'など'):    # 名詞など名詞　は切り離して並列処理にまかせる
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'や'):    # 名詞や名詞　は切り離して並列処理にまかせる
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'から'):    # 名詞から名詞　は切り離す
                            break
                        if(token.pos_ == 'ADP' and token.lemma_ == 'の' and token.head.i != doc[token.i + 1].head.i):    # 後方は　の　で切る　ただし、その先の語が　の　の前にかかるときはつなげる
                            break
                        if (token.lemma_ == '。' or token.lemma_ == '、') and doc[token.i + 1].tag_ != '補助記号-括弧閉':
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
                    ret = self.connect_word(ret, token.orth_)
            # 後方が開カッコのほうが多い場合
            if punc_ct < 0:
                ret = ''
                for token in doc[pt + 1:]:
                    if token.tag_ == '補助記号-括弧開':
                        break
                    end_pt = end_pt + 1
                    ret = self.connect_word(ret, token.orth_)
                punc_c_f = False
                punc_ct = 0

            # 前方のチャンク
            for i in reversed(range(0, pt)):
                if pt < doc[i].head.i and doc[i].head.i != doc[pt].head.i:
                    break
                if punc_ct != 0:
                    if doc[i].tag_ != '補助記号-括弧開':
                        start_pt = i
                        ret = self.connect_word(doc[i].orth_, ret)
                        if doc[i].tag_ == '補助記号-括弧閉':
                            punc_ct = punc_ct + 1
                        continue
                    else:
                        punc_ct = punc_ct - 1
                        if(punc_ct != 0):       # カッコのバランスが悪い？
                            start_pt = i
                            ret = self.connect_word(doc[i].orth_, ret)
                            continue
                elif punc_c_f == 0:
                    if doc[i].tag_ == '補助記号-括弧開':
                        break
                #
                #  自立後の連続
                #
                if((doc[i].head.i == pt or doc[i].head.head.i == doc[pt].head.i) and
                        doc[i].pos_ != 'VERB' and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'DET' and doc[i].pos_ != 'CCONJ' and doc[i].tag_ != '補助記号-読点' and
                        doc[i].pos_ != 'ADP' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '助詞-副助詞' and
#                        doc[i].tag_ != '名詞-普通名詞-助数詞可能' and
                        (not doc[i].morph.get("Inflection") or (doc[i].morph.get("Inflection")  and '連体形' not in doc[i].morph.get("Inflection")[0])) and
                        (doc[i].tag_ != '名詞-普通名詞-副詞可能' or (doc[i].lemma_ != 'なか' and doc[i].lemma_ != 'ため' and doc[i].lemma_ != 'もと')) and doc[i].norm_ != '～' and doc[i].norm_ != '・' and doc[i].norm_ != '＊'):
                    if doc[i].tag_ == '補助記号-括弧閉':
                        punc_ct = punc_ct + 1
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
                #
                #  付属語を含むチャンク
                #
                #  名詞　＋　の[や]　＋　〇〇 名詞 +  格助詞　＋　の　＋　〇〇
                #  動詞 +  助詞　＋　の　/　〇〇  前が動詞の場合は「〜の」の連体修飾では繋げない
                #
                elif (doc[i].pos_ != 'DET' and doc[i].pos_ != 'VERB'  and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'SCONJ' and
                      doc[i].pos_ != 'PART' and doc[i].pos_ != 'PRON' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点' and
                      (doc[i].pos_ != 'ADP' or doc[i].orth_ == 'の' or doc[i].orth_ == 'や' or doc[i].orth_ == 'と' or
                       (doc[i].pos_ == 'ADP' and doc[i + 1].orth_ == 'の'))):
                    if (doc[i].orth_ == 'の' and (doc[i - 1].pos_ == 'ADP' or doc[i - 1].pos_ == 'SCONJ') and (doc[i - 2].pos_ == 'VERB' or doc[i - 2].pos_ == 'AUX')):
                        break
                    if(doc[i].pos_ == 'SYM' and (doc[i].lemma_ == '〜' or doc[i].lemma_ == '～' or doc[i].lemma_ == '＊')):
                        break
                    if doc[i].pos_ == 'SYM' and doc[i].tag_ == '助詞-格助詞':      # 〜　が格助詞の朱鷺　
                        break
                    if doc[i].pos_ == 'SYM' and doc[i -1].pos_ == 'ADP':      # いつでも・どこでも　
                        break
                    if(doc[i].pos_ == 'SYM' and (not self.head_connect_check(pt, doc[i].head.i, *doc) and doc[pt].head.i !=  doc[i].head.i)):
                        break
                    if(doc[i].tag_ == '接尾辞-名詞的-助数詞' and (doc[i].lemma_ == '日' or doc[i].lemma_ == '月' or doc[i].lemma_ == '年')):
#                    if((doc[i].tag_ == '接尾辞-名詞的-助数詞' or doc[i].tag_ == '名詞-普通名詞-助数詞可能') and (doc[i].lemma_ == '日' or doc[i].lemma_ == '月' or doc[i].lemma_ == '年')):
                        break
#                    if doc[i].orth_ == 'の' and doc[i - 1].pos_ == 'ADV':
#                        break
                    if doc[i].orth_ == 'の' and doc[i - 1].lemma_ == 'ため':
                        break
                    if doc[i].orth_ == 'の' and doc[i - 1].lemma_ == 'で':
                        break
                    if (doc[i].pos_ == 'NOUN' or doc[i].pos_ == 'ADV') and (doc[i].lemma_ == 'なか' or  doc[i].lemma_ == 'ため' or doc[i].lemma_ == 'もと' or doc[i].lemma_ == '今後'):
                        break
                    if(doc[i].pos_ == 'ADJ' and not self.head_connect_check(pt, i, *doc)):   # objを修飾しない形容詞
                        break
#                    if(doc[i].pos_ == 'CCONJ' and doc[i].norm_ != '及び'):
                    if(doc[i].pos_ == 'CCONJ'):
                        break
                    if(doc[i].pos_ == 'ADP' and ((doc[i].lemma_ == 'と' and doc[i + 1].lemma_ != 'の') or doc[i].lemma_ == 'や')):
                        break
                    if doc[i].tag_ == '補助記号-括弧閉':
                        punc_ct = punc_ct + 1
                    elif doc[i].tag_ == '補助記号-括弧開':
                        start_pt = i
                        ret = self.connect_word(doc[i].orth_, ret)
                        continue
                    if not self.head_connect_check(pt, i, *doc) and doc[pt].head.i != doc[i].head.i:
                        break
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
#                elif (doc[i].pos_ == 'VERB' or doc[i].pos_ == 'AUX' and (doc[i + 1].orth_ == 'ため' or doc[i + 1].orth_ == 'もの' or doc[i + 1].orth_ == 'とき' or doc[i + 1].orth_ == '人')):
#                    start_pt = i
#                    ret = self.connect_word(doc[i].orth_, ret)
                elif((doc[i].pos_ == 'VERB' and doc[i + 1].pos_ == 'AUX' and doc[i + 2].orth_ == 'か') or
                    ((doc[i].pos_ == 'AUX' or doc[i].pos_ == 'VERB') and doc[i + 1].orth_ == 'か')):  # 〇〇か〇〇
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
                elif (doc[i].tag_ == '補助記号-読点' and doc[i - 1].tag_ == '補助記号-括弧閉' and
                        (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
                elif(doc[i].tag_ == '補助記号-読点' and  doc[i - 1].orth_ == '株式会社' and doc[i - 2].pos_ != 'NOUN' and doc[i - 2].pos_ != 'PROPN' and
                        (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
#                elif(doc[i].pos_ == 'PUNCT' and doc[i - 1].pos_ != 'VERB'  and doc[i - 1].pos_ != 'ADV'  and doc[i - 1].pos_ != 'ADP' and
#                     doc[i - 1].tag_ != '名詞-普通名詞-副詞可能' and doc[i - 1].tag_ != '接尾辞-名詞的-助数詞' and
#                     doc[i - 1].tag_ != '名詞-普通名詞-助数詞可能' and doc[i - 1].tag_ != '名詞-数詞' and
#                     (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
#                    start_pt = i
#                    ret = self.connect_word(doc[i].orth_, ret)
                elif(doc[i].pos_ == 'ADP' and doc[i].orth_ == 'に' and doc[i + 1].orth_ == 'なる'):
                    start_pt = i
                    ret = self.connect_word(doc[i].orth_, ret)
                else:
                     break
        return {'lemma': ret, 'lemma_start': start_pt, 'lemma_end': end_pt}
