from predicate_phrase_analysis import PredicatePhraseExtractor
class PredicateGet:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """



        p_x = PredicatePhraseExtractor()
        self.predicate_phrase_get = p_x.predicate_phrase_get

    """
    主述部と補助術部に別れた述語項構造の取得
    """

    def predicate_get(self, pt, *doc):
        token = doc[pt]
        if (token.pos_ == 'VERB' or token.pos_ == 'ADJ' or token.dep_ == 'ROOT' or token.dep_ == 'ROOT' or token.dep_ == 'obl' or token.dep_ == 'acl' or token.dep_ == 'advcl' or token.tag_ == '名詞-普通名詞-副詞可能' or
                (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX') or
                (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能') or
                (len(doc) > token.i + 1 and token.tag_ == '名詞-普通名詞-サ変可能' and token.dep_ == 'nmod' and (doc[token.i + 1].lemma_ == '、' or doc[token.i + 1].lemma_ == '：'))):
            if token.dep_ == 'fixed':
                return {}
            verb = self.predicate_phrase_get(token.i, *doc)
            if token.pos_ == 'VERB' or token.pos_ == 'ADJ' or (token.dep_ == 'nmod' and token.i > 0 and doc[token.i - 1].pos_ == 'ADP') or (token.dep_ == 'ROOT' and token.tag_ == '名詞-普通名詞-サ変可能'):
                return verb
            elif token.dep_ == 'obl' and (doc[token.i - 1].lemma_ == 'を' and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'に'):
                return verb
            elif token.tag_ == '名詞-普通名詞-副詞可能' and (token.lemma_ == 'ため') and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'の':    # 〜ための
                return verb
            elif token.dep_ == 'acl' and token.lemma_ == 'する':  # 〜を〇〇する〇〇
                return verb
            elif (token.dep_ == 'obl' and len(doc) > token.i + 2 and doc[token.i + 1].lemma_ == 'と' and doc[token.i + 2].pos_ != 'NOUN'):  # 〇〇とする
                return verb
            elif len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX':
                return verb
            elif token.tag_ == '名詞-普通名詞-サ変可能' and (len(doc) <= token.i + 1 or doc[token.i + 1].pos_ != 'ADP') and (not doc[token.i - 1].morph.get("Inflection") or '連体形' not in doc[token.i - 1].morph.get("Inflection")[0]):
                return verb
            ###################
            #
            #   普通名詞 + する　のかたちの最終述部
            #
            elif len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'VERB') and token.dep_ == 'ROOT' and doc[token.i + 1].lemma_ == 'する':
                return verb
            #   〇〇 + を + 〇〇 + に、... 　
            #
            elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and len(doc) > token.i + 2 and token.pos_ == 'NOUN' and doc[token.i + 1].lemma_ == 'に' and doc[token.i + 2].tag_ == '補助記号-読点':
                return verb
            #   〇〇 + を + 〇〇 + の... 　
            #
            elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and doc[token.i + 1].lemma_ == 'の':
                return verb
            #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
            #
            elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and (len(doc) > token.i + 1 and (token.pos_ == 'NOUN' and token.tag_ != '接尾辞-名詞的-副詞可能' and token.tag_ != '接尾辞-名詞的-助数詞' and token.tag_ != '名詞-普通名詞-助数詞可能') and token.tag_ != '名詞-普通名詞-形状詞可能' and doc[token.i + 1].tag_ == '補助記号-読点'):
                return verb
            #   〇〇　＋　を　＋　普通名詞。　　　体言止 連用中止
            #
            elif token.i > 0 and (doc[token.i - 1].pos_ == 'ADP' or doc[token.i - 1].pos_ == 'SCONJ') and (token.pos_ == 'NOUN' and ((token.dep_ == 'ROOT' and token.i == token.head.i) or (len(doc) > token.i + 1 and doc[token.i + 1].pos_ == 'SYM'))):
                return verb
            elif (len(doc) > token.i + 1 and token.tag_ == '形状詞-一般' and doc[token.i + 1].tag_ == '助動詞'):
                return verb
            elif (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能'):
                return verb
            else:
                return {}

        else:
            return {}
