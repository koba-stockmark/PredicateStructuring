import spacy
from spacy.symbols import obj
import re
from pyknp import KNP

class VerbExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        # self.nlp = spacy.load('ja_ginza') # Ginzaのロード
        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        self.knp = KNP()  # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)

    def obj_get(self, text):
        """
          目的語の取得
        """
        doc = self.nlp(text)  # 文章を解析

        for tok in doc:
            if tok.dep == obj:  # トークンが目的語なら
                print(tok.text)  # テキストを表示
        return
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
    動詞のチャンキング
        複合動詞は作るが助動詞は接続しない
        return  = [チャンク原型　チャンク原型スタート　チャンク原型エンド　動詞句　動詞句スタート　動詞句エンド モダリティ]
    """

    def verb_chunk(self, pt, *doc):
        start_pt = pt
        end_pt = pt
        pre = ''
        for i in reversed(range(0, pt)):
            if (pt == doc[i].head.i or pt == doc[i].head.head.i) and doc[i].pos_ != 'PUNCT' and (doc[i].pos_ != 'AUX' or doc[i].orth_ == 'する') and\
                    (doc[i].pos_ != 'ADP' or (doc[i].tag_ == '助詞-副助詞' and doc[i].lemma_ != 'まで')) and doc[i].pos_ != 'ADV' and doc[i].pos_ != 'SCONJ' and doc[i].tag_ != '名詞-普通名詞-副詞可能':
                pre = doc[i].orth_ + pre
                start_pt = i
            elif(doc[i].tag_ == '補助記号-読点' and doc[i - 1].head.i == doc[i].i + 1):      # 〇〇、〇〇する　などの並列術部
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
            elif (tail_ct == 0 and token.head.i == token.head.head.i and (token.tag_  ==  '接尾辞-名詞的-サ変可能')):
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
        if doc[pt].lemma_ == 'こと' or doc[pt].lemma_ == '人' or doc[pt].lemma_ == 'もの' or doc[pt].lemma_ == 'とき' or doc[pt].lemma_ == 'ため':
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
            # 後方のチャンク
            for token in doc[pt+1:]:
                if (pt == token.head.i):
                    if (token.pos_ == 'ADP' and (token.lemma_ == 'を' or token.lemma_ == 'は' or token.lemma_ == 'が' or token.lemma_ == 'で' or token.lemma_ == 'も')):  # 名詞の名詞　は接続させたい
                        break
                    if token.tag_ == '補助記号-括弧閉':
                        punc_c_f = True
                    if token.tag_ == '補助記号-括弧開':
                        punc_o_f = True
                    end_pt = end_pt + 1
                    ret = ret + token.orth_
            # 前方のチャンク
            for i in reversed(range(0, pt)):
                if punc_c_f and not punc_o_f:
                    if doc[i].tag_ != '補助記号-括弧開':
                        start_pt = i
                        ret = doc[i].orth_ + ret
                        continue
                    punc_o_f = False
                    punc_c_f = False
                if(doc[i].head.i == pt and doc[i].pos_ != 'VERB' and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'DET'):
                    start_pt = i
                    ret = doc[i].orth_ + ret
#                elif (doc[i].pos_ == 'PUNCT' and doc[i].lemma_ == '「'):  # 「＋名詞
#                    if "」" not in ret:
#                        find_f = False
#                        for token in doc[pt+1:]:
#                            if(token.lemma_ == '」' and token.head.i == pt):
#                                find_f = True
#                                break
#                        if(find_f):
#                            start_pt = i
#                            ret = doc[i].orth_ + ret
#                        else:
#                            break
#                    else:
#                        start_pt = i
#                        ret = doc[i].orth_ + ret
                elif (doc[i].pos_ != 'DET' and doc[i].pos_ != 'VERB'  and doc[i].pos_ != 'AUX' and doc[i].pos_ != 'SCONJ' and doc[i].pos_ != 'PART' and doc[i].pos_ != 'PRON' and doc[i].tag_ != '補助記号-読点' and doc[i].tag_ != '補助記号-句点' and
                        (doc[i].pos_ != 'ADP' or doc[i].orth_ == 'の' or doc[i].orth_ == 'や' or doc[i].orth_ == 'と' or                  # 名詞　＋　の[や]　＋　〇〇
                         (doc[i].pos_ == 'ADP' and doc[i + 1].orth_ == 'の'))):                                                           # 名詞 +  格助詞　＋　の　＋　〇〇
                    if (doc[i].orth_ == 'の' and (doc[i - 1].pos_ == 'ADP' or doc[i - 1].pos_ == 'SCONJ') and (doc[i - 2].pos_ == 'VERB' or doc[i - 2].pos_ == 'AUX')):  # 動詞 +  助詞　＋　の　/　〇〇     前が動詞の場合は「〜の」の連体修飾では繋げない
                        break
                    if(doc[i].pos_ == 'SYM' and doc[i].lemma_ == '～'):
                        break
                    if(doc[i].tag_ == '接尾辞-名詞的-助数詞' and (doc[i].lemma_ == '日' or doc[i].lemma_ == '月' or doc[i].lemma_ == '年')):
                        break
                    if doc[i].orth_ == 'の' and doc[i - 1].lemma_ == 'ため':
                        break
                    if doc[i].tag_ == '補助記号-括弧閉':
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
                elif(doc[i].pos_ == 'PUNCT' and doc[i - 1].pos_ != 'VERB'  and doc[i - 1].pos_ != 'ADV' and
                     (doc[i - 1].head.i == doc[i + 1].head.i or doc[i - 1].head.i == pt or doc[i - 1].head.i == i + 1)):     # 〇〇、〇〇　の場合はまとめる
                    start_pt = i
                    ret = doc[i].orth_ + ret
                elif(doc[i].pos_ == 'ADP' and doc[i].orth_ == 'に' and doc[i + 1].orth_ == 'なる'):
                    start_pt = i
                    ret = doc[i].orth_ + ret
                else:
                     break
            #      print(doc[pt].orth_)
            #      return doc[pt].orth_
        return ret, start_pt, end_pt

    """
        主語の取得
    """
    def subject_get(self, verb_pt, *doc):
        ret = ''
        for token in doc:
            if token.dep_ == "nsubj" and token.head.i == verb_pt:  # トークンが主語で述部が同じ
                ret = self.num_chunk(token.i, *doc)[0]
        return ret

    """
    O-Vの取得
    """

    def v_o_get(self, text):

        ret = ''
        modality_w = ''
        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析
        doc_len = len(doc)

        for token in doc:
            obj_w = ''
            rule_id = 0
            if (token.dep_ == "obj" and token.head.dep_ != "obj"):  # トークンが目的語なら
                subject_w = self.subject_get(token.head.i, *doc)
                if(doc[token.i + 1].orth_ == 'に'):      #　〇〇には〇〇の などの文は「を」でなくてもobjで解析される場合がある
                    continue
                obj_w = self.num_chunk(token.i, *doc)[0]
                if (token.head.lemma_ == "する"):
                    #
                    #             述部が  名詞＋（と、に）する（目標とする　など）
                    #
                    if (doc[token.head.i - 1].orth_ == 'に' or doc[token.head.i - 1].orth_ == 'と'):  # 【名詞】に(と)する
                        verb = self.verb_chunk(token.head.i - 2, *doc)
                        verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                        modality_w = verb["modality"]
                        obj_w = self.num_chunk(token.i, *doc)[0]
                        if (doc[token.head.i - 2].tag_ == '補助記号-括弧閉'):
                            verb = self.verb_chunk(token.head.i - 3, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                        rule_id = 1
                    #
                    #             述部が  ○○の＋名詞＋を＋する（調査をする　など）、　名詞＋サ変名詞＋する（内部調査をする　など）
                    #
                    elif doc[token.head.i - 1].orth_ == 'を' and doc[token.head.i - 2].pos_ == 'PRON':       # 何をする　　→　候補から外す
                        verb_w = ''
                        obj_w = ''
                        rule_id = 2
                    elif (doc[token.head.i - 1].orth_ == 'を' and (doc[token.head.i - 2].pos_ == 'NOUN' or doc[token.head.i - 2].pos_ == 'PUNCT' or doc[token.head.i - 2].lemma_ == 'など')):   # 名詞＋を＋する、　名詞＋など＋を＋する
                        if (doc[token.head.i - 3].orth_ == 'の' or
                                (doc[token.head.i - 3].orth_ == 'を' and token.i != doc[token.head.i - 2].i)):   # OBJ以外の名詞が「する」の前にある場合は「名詞＋する」をまとめる
                            obj_w = self.num_chunk(token.head.i - 4, *doc)[0]  # 内部の調査をする -> 内部を　調査する, 緊急使用を承認をする -> 緊急使用を　承認する
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 3
                        elif (doc[token.head.i - 3].pos_ == 'NOUN' and doc[token.head.i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                                (doc[token.head.i - 4].orth_ == 'の' or doc[token.head.i - 4].orth_ == 'を')):
                            obj_w = self.num_chunk(token.head.i - 5, *doc)[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 4
                        elif (doc[token.head.i - 3].pos_ == 'NOUN' and doc[token.head.i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                              (doc[token.head.i - 3].tag_ != '名詞-普通名詞-形状詞可能' and doc[token.head.i - 3].tag_ != '接頭辞')):  # 内部調査をする -> 内部を　調査する　でも　緊急調査をする -> 緊急を　調査する　ではない!!　組み合わせで判断する必要あり！
                            obj_w = self.num_chunk(token.head.i - 3, *doc)[0]
                            verb_w = doc[token.head.i - 2].orth_ + token.head.lemma_        # 文の形を変えているので手動
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            modality_w = verb["modality"]
                            rule_id = 5
                        elif (doc[token.head.i - 3].pos_ == 'VERB' and doc[token.head.i - 3].head.i == doc[token.head.i - 3].i):
                            obj_w = self.num_chunk(token.head.i - 3, *doc)[0]      # 内部調査をする -> 内部を　調査する
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 6
                        #
                        #             述部が  名詞＋を＋する（調査をする　など）  メイン術部にならない候補
                        #
                        else:
                            obj_w = self.num_chunk(token.i, *doc)[0]
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 7
                    #
                    #             述部が  形容詞＋する（少なくする　など）
                    #
                    elif (doc[token.head.i - 1].pos_ == 'AUX'):
                        if (token.head.i - 4 >= 4 and (doc[token.head.i - 1].tag_ == '接尾辞-形容詞的'  or doc[token.head.i - 1].tag_ == '助動詞' )and doc[token.head.i - 2].pos_ == 'VERB'):
                            # ○○を使いやすくする -> 使いやすくする
                            obj_w = self.num_chunk(token.i, *doc)[0]
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 8
                        else:
                            obj_w = ''
                    elif (doc[token.head.i - 1].pos_ == 'ADJ'):
                        if (token.head.i - 4 >= 4 and doc[token.head.i - 1].tag_ == '形容詞-非自立可能' and doc[token.head.i - 2].pos_ == 'NOUN'):
                            # ○○を余儀なくする -> 余儀なくする
                            obj_w = self.num_chunk(token.head.i - 4, *doc)[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 9
                        elif (doc[token.head.i - 1].tag_ == '形容詞-一般' or doc[token.head.i - 1].tag_ == '形容詞-非自立可能' or (doc[token.head.i - 1].tag_ == '副詞' and doc[token.head.i - 1].lemma_ == 'よく')):
                            # ○○を少なくする -> 少なくする
                            obj_w = self.num_chunk(token.i, *doc)[0]
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 10
                        else:
                            obj_w = ''
                            rule_id = 200
                    #
                    #     「〇〇」する　→　〇〇する
                    #
                    elif (doc[token.head.i - 1].pos_ == 'PUNCT'):
                        verb = self.verb_chunk(token.head.i - 2, *doc)
                        verb_w = verb["lemma"] + token.head.lemma_
                        modality_w = verb["modality"]
                        rule_id = 11
                    #
                    #   どうする、そうする...
                    #
                    elif (doc[token.head.i - 1].pos_ == 'ADV'):
                        verb = self.verb_chunk(token.head.i - 1, *doc)
                        verb_w = verb["lemma"] + token.head.lemma_
                        modality_w = verb["modality"]
                        rule_id = 12
                    #
                    #   〇〇の〇〇を〇〇で（と、から..）する　　　「…をする」の変形版　　→　〇〇の〇〇を〇〇する　と同じ処理　目的語は　更に前の　「〇〇の」　ex.エンジンの開発を東京でする
                    #
                    elif (doc[token.head.i - 1].pos_ == 'ADP' and doc[token.head.i - 1].lemma_ != 'を'):
                        if 'の' in obj_w:
                            verb_w = obj_w.split('の')[1]
                            obj_w = obj_w.split('の')[0]
                            rule_id = 13
                        else:
                            verb = self.verb_chunk(token.head.i , *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 30
                #
                #   普通名詞 + する　のかたちの最終述部
                #
                elif doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' or token.head.pos_ == 'VERB') and token.head.dep_ == 'ROOT' and doc[token.head.i + 1].lemma_ == 'する':
                    obj_w = self.num_chunk(token.i, *doc)[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_
                    modality_w = verb["modality"]
                    rule_id = 14
                #
                #   〇〇 + を + 〇〇 + に、... 　
                #
                elif doc_len > token.head.i + 2 and token.head.pos_ == 'NOUN' and doc[token.head.i + 1].lemma_ == 'に' and doc[token.head.i + 2].tag_ == '補助記号-読点':
                    obj_w = self.num_chunk(token.i, *doc)[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_ + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 22
                #
                #   〇〇 + を + 〇〇 + の... 　
                #
                elif doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' or token.head.pos_ == 'PROPN') and doc[token.head.i + 1].lemma_ == 'の':
                    if(token.head.tag_ == '名詞-普通名詞-副詞可能'):     # 〇〇　＋　を　＋　ため　＋　の
                        verb = self.verb_chunk(token.head.i, *doc)
                        verb_w = verb["lemma"]
                        modality_w = verb["modality"]
                        rule_id = 23
                    else:
                        continue
                #
                #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
                #
                elif doc_len > token.head.i + 1 and token.head.pos_ == 'NOUN' and doc[token.head.i + 1].tag_ == '補助記号-読点':
                    obj_w = self.num_chunk(token.i, *doc)[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 24
                #
                #   〇〇　＋　を　＋　普通名詞。　　　体言止
                #
                elif token.head.pos_ == 'NOUN' and token.head.dep_ == 'ROOT' and token.head.i == token.head.head.i:
                    obj_w = self.num_chunk(token.i, *doc)[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 15
                #                        obj_w = ''  # デバッグ用
                #
                #           ○○する　以外の一般の動詞
                #
                else:
                    ###############################
                    #    形式動詞
                    ###############################
                    if(token.head.lemma_ == 'なる'):                                # 形式動詞
                        if(doc[token.head.i - 1].pos_ == 'ADP' or (doc[token.head.i - 1].pos_ == 'AUX' and doc[token.head.i - 1].orth_ == 'に')):     # 〜となる　〜になる
                            verb = self.verb_chunk(doc[token.head.i - 1].i - 1, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 16
                        else:
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 17
                    elif  doc_len > token.head.i + 1 and (doc[token.head.i + 1].tag_ == '動詞-非自立可能'):          # 動詞　＋　補助動詞
                        verb = self.verb_chunk(doc[token.head.i].i, *doc)
                        verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_
                        modality_w = verb["modality"]
                        rule_id = 18
                    ###############################
                    #    形式名詞
                    ###############################
                    elif (token.head.lemma_ == 'ため'):  # 形式名詞
                        if(doc[token.head.i - 1].pos_ == 'AUX' and doc[token.head.i - 1].lemma_ == 'する'):
                            verb = self.verb_chunk(doc[token.head.i].i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 19
                        elif doc[token.head.i - 1].pos_ == 'VERB':
                            verb = self.verb_chunk(doc[token.head.i].i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 20
                    else:                                                           # 単独の動詞
                        verb_w = token.head.lemma_
                        verb = self.verb_chunk(token.head.i, *doc)
                        verb_w = verb["lemma"]
                        modality_w = verb["modality"]
                        rule_id = 21
                    obj_w = self.num_chunk(token.i, *doc)[0]
#                    obj_w = ''  # デバッグ用

                ###########################################################
                ##   TBD 慣用句処理  　（「日の目を見る」など）　#############
                ###########################################################


                ##########################################################################################################################################
                #    メイン述部の判断
                #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
                #              出力は　目的語　＋　メイン術部　にする
                ##########################################################################################################################################

                #"""
                # デバッグ用
                if (obj_w ):
                    print(text)
                    modal = ', '.join([str(x) for x in modality_w])
                    print('all = 【%s - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, verb_w, subject_w, modal, rule_id))
                    ret = ret + text + '\n' + 'all = 【' + obj_w + ' - ' + verb_w + '】 modality = ' +  modal + ' rule_id = ' + str(rule_id) + '\n'
                #"""
                # デバッグ用

                main_verb = False
                if (token.head.i == token.head.head.i and
                        (token.head.pos_ == "VERB" or token.head.pos_ == "ADV") or              # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
                        (doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' and token.head.dep_ == 'ROOT' and doc[token.head.i + 1].lemma_ == 'する'))): # 普通名詞　＋　する が文末の場合
                    main_verb = True
                    #
                    #           〇〇したと〇〇した　（一時停止したと明らかにした）
                    #           誤解析により補助術部に対して目的語がかかっている場合の処理
                    #
                    if doc_len > token.head.i + 3 and (doc[token.i + 2].head.i == token.head.i and doc[token.i + 2].pos_ == 'VERB' and doc[token.i + 3].lemma_ == "する"):
                        verb_w = doc[token.i + 2].lemma_
                        rule_id = 100
#                        obj_w = ''  # デバッグ用
                #
                # 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
                #
                elif (doc[token.head.i].pos_ == "VERB" and doc[token.head.i].head.i == doc[token.head.i].head.head.i and doc[token.head.i].head.pos_ == "VERB"):  # 最後の動詞を修飾する動詞？
                    #            print(doc[token.head.i].head.lemma_ , doc[doc[token.head.i].head.i - 1].lemma_)
                    if (doc[token.head.i].head.lemma_ == 'する' and doc[doc[token.head.i].head.i - 1].pos_ != 'ADP'):  # かかり先の動詞が　○○をする　ではなく　単独の動詞か○○する
                        obj_w = self.num_chunk(token.i, *doc)[0]
                        if(doc[token.head.i + 1].lemma_ == 'する'):
                            verb_w = token.head.lemma_ + doc[token.head.i + 1].lemma_
                        else:
                            verb_w = token.head.lemma_
                        rule_id = 101
                        main_verb = True
                    else:
                        main_verb = True
                #
                #  最終術部が名詞から形成される場合
                #
                elif (token.head.head.head.lemma_ == "する" and doc[token.head.i + 1].lemma_ == '決定'):        # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
                    verb_w = token.head.lemma_
                    obj_w = self.num_chunk(token.i, *doc)[0]
                    rule_id = 102
                    main_verb = True
                elif token.head.pos_ == 'NOUN' and token.head.dep_ == 'ROOT' and token.head.i == token.head.head.i:        # 文末が　体言止
                    rule_id = 103
                    main_verb = True
                #
                #   目的語がない場合は文脈（前の文）から目的語を持ってくる　　　TBD
                #
                #



                #"""
                # デバッグ用
                if (obj_w and main_verb):
                    print(text)
                    modal = ', '.join([str(x) for x in modality_w])
                    print('【%s - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, verb_w, subject_w, modal, rule_id))
                    ret = ret + text + '\n' + '【' + obj_w + ' - ' + verb_w + '】 modality = ' +  modal + ' rule_id = ' + str(rule_id) + '\n'
                # デバッグ用
                #"""
        return ret


    def verb_get(self, text):
        """
         動詞の塊を抽出する
        """

        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析

        """
        デバッグ用に結果を表示
        """
        for token in doc:
            print(
                token.i,
                token.orth_,
                token.lemma_,
                token.norm_,
                token.morph.get("Reading"),
                token.pos_,
                token.morph.get("Inflection"),
                token.tag_,
                token.dep_,
                token.head.i,
            )

        """
        形態素をチェック
        """
        for token in doc:
            if token.dep == obj:
                """
                 かかり先による例外処理
                """
                if token.head.orth_ == "行う":
                    print(token.head.i, token.head.orth_, token.head.head.orth_)
                """
                一般処理
                """
                print(token.i, token.orth_, token.head.orth_)
        return
