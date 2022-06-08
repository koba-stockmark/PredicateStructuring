class CaseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

    """
    表層格の獲得    
    """
    def case_get(self, pt, *doc):
        ret = ''
        open_f = False

        if doc[pt - 1].norm_ == 'の' and doc[pt].norm_ == '為':
            return 'のため(に)'
        elif doc[pt - 1].norm_ == 'の' and doc[pt].norm_ == '下':
            return 'のもと(に)'
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
#            if (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.i == pt and len(doc) > token.i + 1 and doc[token.i + 1].tag_ != '補助記号-括弧閉':
            if (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.i <= pt:
                for i in range(token.i, len(doc)):
                    if (doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞') and doc[i].lemma_ != '～':
                        if doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                            ret = ret + doc[i].lemma_ + 'して'
                            return ret
                        elif doc[i].lemma_ == 'や':
                            ret = self.case_get(doc[i].head.head.i, *doc)
                        elif len(doc) > i + 2 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'おい' and doc[i + 2].orth_ == 'て':
                            ret = 'において'
                        elif len(doc) > i + 2 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'つい' and doc[i + 2].orth_ == 'て':
                            ret = 'について'
                        elif len(doc) > i + 2 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == '関し' and doc[i + 2].orth_ == 'て':
                            ret = 'に関して'
                        elif len(doc) > i + 2 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == '対し' and doc[i + 2].orth_ == 'て':
                            ret = 'に対して'
                        elif len(doc) > i + 2 and doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'よっ' and doc[i + 2].orth_ == 'て':
                            ret = 'によって'
                        elif doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                            ret = 'により'
                        elif doc[i].lemma_ == 'の' and doc[i + 1].norm_ == '為':
                            ret = 'のため(に)'
                        elif doc[i].lemma_ == 'の' and doc[i + 1].norm_ == '下':
                            ret = 'のもと(に)'
                        else:
                            ret = ret + doc[i].orth_
                    else:
                        return ret
            elif (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.head.i == pt and token.head.pos_ == 'NOUN' and token.lemma_ != 'の':  # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                for i in range(token.i, len(doc)):
                    if doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞':
                        if doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                            ret = ret + doc[i].lemma_ + 'して'
                            return ret
                        elif doc[i].lemma_ == 'や':
                            ret = doc[doc[i].head.head.i - 1].lemma_
                        elif doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                            ret = 'により'
                        else:
                            ret = ret + doc[i].lemma_
                    else:
                        return ret
#            elif token.dep_ == "case" and token.head.head.i == doc[pt].head.i:    # 括弧書きを挟んだ係り受けの場合　ex.新事業としてフローズンミール定期配送サービス「nonpi A.R.U.」を開始すると発表した。
#               for i in range(token.i, len(doc)):
#                    if doc[i].dep_ == "case":
#                        ret = ret + doc[i].lemma_
#                    else:
#                        return ret
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
                                return ret
                            elif doc[i].lemma_ == 'や':
                                ret = doc[doc[i].head.head.i - 1].lemma_
                            elif doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                                ret = 'により'
                            else:
                                ret = ret + doc[i].lemma_
                        else:
                            return ret
                elif (token.dep_ == "case" or token.tag_ == '助詞-格助詞') and token.tag_ != '名詞-普通名詞-一般' and token.head.head.i == pt and token.head.pos_ == 'NOUN':    # 括弧書きを挟んだ係り受けの場合　ex.SaaSソリューション「Ecomedia」を開発する
                    for i in range(token.i, len(doc)):
                        if doc[i].dep_ == "case" or doc[i].tag_ == '助詞-格助詞':
                            if doc[i].lemma_ == 'と' and doc[i + 1].lemma_ == 'する' and doc[i + 2].lemma_ == 'て':
                                ret = ret + doc[i].lemma_ + 'して'
                                return ret
                            elif doc[i].lemma_ == 'や':
                                ret = doc[doc[i].head.head.i - 1].lemma_
                            elif doc[i].lemma_ == 'に' and doc[i + 1].orth_ == 'より':
                                ret = 'により'
                            else:
                                ret = ret + doc[i].lemma_
                        else:
                            return ret
        if not ret: # 直後に格助詞がない場合
            if len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].lemma_ == '・' and doc[doc[pt].head.i].pos_ == 'VERB':
                for i in reversed(range(0, doc[doc[pt].head.i].i)):
                    if doc[i].pos_ == 'ADP':
                        ret = doc[i].lemma_ + ret
                    else:
                        break
        return ret

