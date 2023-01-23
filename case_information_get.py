from chunker import ChunkExtractor
class CaseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.rentai_check = chunker.rentai_check



    """
    表層格の獲得    
    """
    def case_get(self, pt, *doc):
        ret = ''
        open_f = False
        fixed_type = 0
        is_fukushiteki = False
        if pt < 0:
            return ret
        # 副詞系
        if doc[pt].pos_ == "VERB" or doc[pt].pos_ == "AUX" or doc[pt].pos_ == "ADJ":
            is_fukushiteki = True
        if ((doc[pt].dep_ == 'advmod' and doc[pt].pos_ == 'ADV') or doc[pt].tag_ == '名詞-普通名詞-助数詞可能' or doc[pt].tag_ == '助詞-副助詞') and (len(doc) > pt + 1 and doc[pt + 1].pos_ != 'ADP'):
            return "副詞的"
        # 動詞系　格と修飾関係
        if len(doc) > pt + 1 and doc[pt].lemma_ == "を":   # 〇〇をする　の対応
            pt = pt + 1
        if len(doc) > pt + 1 and (doc[pt].pos_ == 'VERB' or (doc[pt].pos_ == 'AUX' and doc[pt + 1].pos_ != "AUX")) and doc[pt + 1].tag_ != "助詞-準体助詞" and doc[pt + 1].tag_ != "名詞-普通名詞-副詞可能" and doc[pt + 1].tag_ != "形状詞-助動詞語幹" and doc[pt].morph.get("Inflection") and '連体形' in doc[pt].morph.get("Inflection")[0]:
            return ret + '連体修飾'
        if len(doc) > pt + 1 and (doc[pt].pos_ == 'VERB' or doc[pt].pos_ == 'AUX' or doc[pt].pos_ == 'ADJ') and (doc[pt + 1].pos_ == 'AUX' or doc[pt + 1].pos_ == 'SCONJ'):
            if doc[pt + 1].pos_ == 'AUX' and (doc[pt + 1].orth_ == 'た' or doc[pt + 1].orth_ == 'だ' or doc[pt + 1].orth_ == 'です' or doc[pt + 1].orth_ == 'ます'):
                sp = pt + 2
            else:
                sp = pt + 1
            cpt = sp
            for cpt in range(sp, len(doc)):
                if (len(doc) > cpt + 1 and doc[cpt].lemma_ == 'て' and doc[cpt + 1].lemma_ == 'いる') or (doc[cpt - 1].lemma_ == 'て' and doc[cpt].lemma_ == 'いる'):     # 〇〇ている＋「格助詞」　は特別　ex.　できなくなっていると発表した
                    ret = ret + doc[cpt].orth_
                    continue
                if len(doc) > cpt + 1 and doc[cpt - 1].orth_ == 'で' and doc[cpt].lemma_ == 'ある'and doc[cpt + 1].pos_ == 'SCONJ':     # 〇〇であれば
                    ret = ret + doc[cpt].orth_
                    continue
                if doc[cpt].tag_ == "補助記号-括弧閉":
                    continue
                if doc[cpt].pos_ != 'SCONJ' and doc[cpt].pos_ != 'AUX' and doc[cpt].pos_ != 'ADP' and doc[cpt].pos_ != 'PART':
                    break
                ret = ret + doc[cpt].orth_
            if doc[cpt - 1].morph.get("Inflection") and '連体形' in doc[cpt - 1].morph.get("Inflection")[0]:
                if doc[cpt].orth_ == "こと" and len(doc) > cpt + 2 and doc[cpt + 1].pos_ == "ADP" and doc[cpt + 2].tag_ == "動詞-非自立可能":
                    if len(doc) > cpt + 4 and doc[cpt + 3].pos_ == "PUNCT" and doc[cpt + 4].pos_ == "ADP":
                        return ret + "こと" + doc[cpt + 1].orth_ + doc[cpt + 2].orth_ + doc[cpt + 4].orth_ + '-副詞的'
                    else:
                        return ret + "こと" + doc[cpt + 1].orth_ + doc[cpt + 2].orth_ + '-副詞的'
                if ret:
                    return ret + '-連体修飾'
                else:
                    return '連体修飾'
            if ret:
                return ret + '-副詞的'
            else:
                return '副詞的'
        if doc[pt].norm_ == "出来る":
            fixed_type = 1
        # 名詞系　格関係
        if pt >= 2 and doc[pt - 2].norm_ == 'まで' and doc[pt - 1].norm_ == 'の' and doc[pt].norm_ == '為':
            return 'までのため(に)'
        if pt >= 1 and doc[pt - 1].norm_ == 'の' and doc[pt].norm_ == '為':
            return 'のため(に)'
        elif pt >= 1 and doc[pt - 1].norm_ == 'の' and (doc[pt].norm_ == '下' or doc[pt].norm_ == 'もと'):
            return 'のもと(に)'
        elif doc[pt].norm_ == '為':
            return 'に'
        for token in doc[pt + 1:]:
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
            if (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.i <= pt:
                for i in range(token.i, len(doc)):
                    if (doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞') and doc[i].lemma_ != '～':
                        if len(doc) > i + 2 and doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                            ret = ret + doc[i].lemma_ + 'して'
                            return ret + '-副詞的'
                        elif doc[i].lemma_ == 'や':
                            if doc[i + 1].pos_ == 'PUNCT':
                                re_nun = self.num_chunk(i + 2, *doc)
                            else:
                                re_nun = self.num_chunk(i + 1, *doc)
                            ret = self.case_get(re_nun["lemma_end"], *doc)
                            if ret == 'との':
                                ret = self.case_get(re_nun["lemma_end"] + 3, *doc)
                            elif len(doc) > i + 1 and doc[i + 1].pos_ == 'ADJ':
                                ret = ''
                                for np in reversed(range(0, doc[i - 1].head.i)):
                                    if doc[np].pos_ != 'ADP':
                                        break
                                    ret = doc[np].orth_ + ret
                        elif len(doc) > i + 3 and doc[i - 1].pos_ != 'ADJ' and doc[i].lemma_ == 'の' and doc[i + 1].pos_ == 'NOUN' and doc[i + 2].lemma_ == 'を' and doc[i + 3].norm_ == '為る':
                            ret = 'を'
                        else:
                            ret = ret + doc[i].orth_
                    elif doc[i].dep_ == "fixed":
                        fixed_type = 1
                        if doc[i].morph.get("Inflection") and '連体形' in doc[i].morph.get("Inflection")[0]:
                            fixed_type = 2
                        ret = ret + doc[i].orth_
                    else:
                        if fixed_type == 1:
                            return ret + '-副詞的'
                        elif fixed_type == 2:
                            return ret + '-連体修飾'
                        elif is_fukushiteki:
                            return ret + '-副詞的'
                        return ret
            elif (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.head.i == pt and token.head.pos_ == 'NOUN' and token.lemma_ != 'の':  # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                for i in range(token.i, len(doc)):
                    if doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞':
                        if len(doc) > i + 2 and doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                            ret = ret + doc[i].lemma_ + 'して'
                            return ret + '-副詞的'
                        elif doc[i].lemma_ == 'や':
                            ret = doc[doc[i].head.head.i - 1].lemma_
                        elif len(doc) > i + 1 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                            ret = 'により'
                        else:
                            ret = ret + doc[i].lemma_
                    else:
                        if fixed_type == 1:
                            return ret + '-副詞的'
                        elif fixed_type == 2:
                            return ret + '-連体修飾'
                        elif is_fukushiteki:
                            return ret + '-副詞的'
                        return ret
            elif token.dep_ == "case" and token.head.head.i == doc[pt].head.i:    # 括弧書きを挟んだ係り受けの場合　ex.新事業としてフローズンミール定期配送サービス「nonpi A.R.U.」を開始すると発表した。
                if doc[pt].norm_ == '日' or doc[pt].norm_ == '月' or doc[pt].norm_ == '年' or doc[pt].norm_ == '期間':
                    return 'に'
                for i in range(token.i, len(doc)):
                    if doc[i].dep_ == "case":
                        ret = ret + doc[i].lemma_
                    else:
                        if fixed_type == 1:
                            return ret + '-副詞的'
                        elif fixed_type == 2:
                            return ret + '-連体修飾'
                        elif is_fukushiteki:
                            return ret + '-副詞的'
                        return ret
            elif len(doc) > token. i + 1 and token.orth_ == 'だ' and doc[token.i + 1].orth_ == 'が':
                ret = 'だが'
                break
            elif token.tag_ == '助詞-副助詞' and token.orth_ == 'まで':
                ret = ret + token.orth_
            elif token.pos_ == 'PART':
                ret = ret + token.orth_
            elif token.tag_ == '助動詞' and (token.orth_ == 'に' or token.orth_ == 'で'):
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.tag_ == '助動詞' and token.dep_ == "cop":   # 〜なら
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.tag_ == '助動詞' and token.lemma_ == "た":  # 〜た
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.pos_ == 'SCONJ':  # 〜ば
                ret = ret + token.orth_
                is_fukushiteki = True
            elif len(doc) > token.i + 1 and doc[token.i - 1].lemma_ == "だ" and token.lemma_ == 'ある' and doc[token.i + 1].pos_ == "SCONJ":  # 〜であれば
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.lemma_ == 'ない' and doc[token.i - 1].lemma_ == "は" and doc[token.i - 2].lemma_ == "だ":  # 〜ではなく
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.lemma_ == 'は' and doc[token.i - 1].lemma_ == "だ":  # 〜ではなく
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.lemma_ == "する" and doc[token.i - 1].lemma_ == "たり":
                ret = ret + token.orth_
                is_fukushiteki = True
            elif token.head.i > pt:
                break
        if open_f and not ret:  # カッコのバランスが悪い場合は、カッコ内も対象にする
            for token in doc[pt:]:
                if len(doc) > token.i + 2 and doc[token.i + 1].tag_ == '補助記号-句点' and doc[token.i + 2].tag_ == '補助記号-括弧閉':
                    continue
                if (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.i == pt and len(doc) > token.i + 1 and doc[token.i + 1].tag_ != '補助記号-括弧閉':
                    for i in range(token.i, len(doc)):
                        if doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞':
                            if doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                                ret = ret + doc[i].lemma_ + 'して'
                                return ret + '-副詞的'
                            elif doc[i].lemma_ == 'や':
                                ret = doc[doc[i].head.head.i - 1].lemma_
                            elif doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                                ret = 'により'
                            else:
                                ret = ret + doc[i].lemma_
                        else:
                            if fixed_type == 1:
                                return ret + '-副詞的'
                            elif fixed_type == 2:
                                return ret + '-連体修飾'
                            elif is_fukushiteki:
                                return ret + '-副詞的'
                            return ret
                elif (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.head.i == pt and token.head.pos_ == 'NOUN':    # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                    for i in range(token.i, len(doc)):
                        if doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞':
                            if len(doc) > i + 2 and doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                                ret = ret + doc[i].lemma_ + 'して'
                                return ret + '-副詞的'
                            elif doc[i].lemma_ == 'や':
                                ret = doc[doc[i].head.head.i - 1].lemma_
                            elif len(doc) > i + 1 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                                ret = 'により'
                            else:
                                ret = ret + doc[i].lemma_
                        else:
                            if fixed_type == 1:
                                return ret + '-副詞的'
                            elif fixed_type == 2:
                                return ret + '-連体修飾'
                            elif is_fukushiteki:
                                return ret + '-副詞的'
                            return ret
        if not ret: # 直後に格助詞がない場合
            if len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].lemma_ == '・' and doc[doc[pt].head.i].pos_ == 'VERB':
                for i in reversed(range(0, doc[doc[pt].head.i].i)):
                    if doc[i].pos_ == 'ADP':
                        ret = doc[i].lemma_ + ret
                    else:
                        break
            if doc[pt].norm_ == "中" and doc[pt].tag_ == "名詞-普通名詞-副詞可能":
                return "なか-副詞的"
            if doc[pt].norm_ == "うち" and doc[pt].tag_ == "名詞-普通名詞-副詞可能":
                return "うち-副詞的"
        if doc[pt].pos_ == 'VERB' or doc[pt].pos_ == 'AUX' and doc[pt].dep_ != "advcl" and "副詞的" not in ret:
            if ret.endswith("する"):
                ret2 = "連体修飾"
            else:
                ret2 = "副詞的"
            if ret:
                if "副詞的" in ret:
                    return ret
                return ret + '-' + ret2
            else:
                return ret2
        if fixed_type == 1 and "副詞的" not in ret:
            return ret + '-副詞的'
        elif fixed_type == 2:
            return ret + '-連体修飾'
        elif is_fukushiteki:
            if ret:
                return ret + '-副詞的'
            else:
                return "副詞的"
        if not ret:
            return "連接"
        return ret

