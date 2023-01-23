from predicate_phrase_analysis import PredicatePhraseExtractor
from chunker import ChunkExtractor

class PredicateGet:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """



        p_x = PredicatePhraseExtractor()
        self.predicate_phrase_get = p_x.predicate_phrase_get
        chunker = ChunkExtractor()
        self.rentai_check = chunker.rentai_check


    """
    指定された形態素を含む述部の可能性をチェックして述部の場合は述部の取得を行う
    """

    def predicate_get(self, pt, *doc):
        token = doc[pt]
        if doc[pt].tag_ == "補助記号-一般":
            return {}
        if (len(doc) > token.i + 1 and doc[token.i + 1].tag_ == '接尾辞-名詞的-一般') or (len(doc) > token.i + 2 and doc[token.i + 1].pos_ == 'AUX' and doc[token.i + 2].tag_ == '接尾辞-名詞的-一般'):     # 生成名詞はNG
            return {}
        if (token.pos_ == 'VERB' or token.pos_ == 'ADJ' or token.pos_ == 'ADV' or token.dep_ == 'ROOT' or token.dep_ == 'ROOT' or token.dep_ == 'obl' or token.dep_ == 'acl' or token.dep_ == 'advcl' or token.tag_ == '名詞-普通名詞-副詞可能' or
                (token.dep_ == 'nmod' and token.tag_ == "名詞-普通名詞-助数詞可能") or
                (token.pos_ == 'NOUN' and doc[token.head.i].norm_ == '為る' and doc[token.head.i - 1].lemma_ != 'に') or
                (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX') or
                (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能') or
                (len(doc) > token.i + 1 and token.tag_ == '名詞-普通名詞-形状詞可能' and doc[token.i + 1].tag_ == '補助記号-読点') or
                (len(doc) > token.i + 2 and token.tag_ == '名詞-普通名詞-サ変可能' and token.dep_ == 'nmod' and token.head.dep_ == 'obj' and doc[token.i + 1].lemma_ == 'や' and self.rentai_check(token.i + 2, *doc)) or
                (len(doc) > token.i + 1 and token.tag_ == '名詞-普通名詞-サ変可能' and token.dep_ == 'nmod' and (doc[token.i + 1].lemma_ == '、' or doc[token.i + 1].lemma_ == '：'))):
            is_meishi_syuusyoku = False
            if len(doc) > pt + 1 and doc[pt + 1].pos_ != "VERB" and doc[pt + 1].lemma_ != "に":
                for chp in range(0, pt):
                    if doc[chp].head.i == pt and pt > chp + 1 and doc[pt + 1].tag_ != "助詞-副助詞" and doc[chp + 1].pos_ == "ADP" and doc[chp + 1].lemma_ != "の" and doc[chp + 1].lemma_ != "や" and doc[chp + 1].lemma_ != "と":
                        is_meishi_syuusyoku = True
                        break
            if token.dep_ == 'fixed':
                return {}
#            if token.dep_ == 'compound':
#                return {}
            if token.tag_ == '接頭辞':
                return {}
            if doc[token.i - 1].lemma_ != 'を' and doc[token.i - 1].lemma_ != 'に' and doc[token.i - 1].lemma_ != 'と' and doc[token.i - 1].pos_ != 'ADJ' and doc[token.i].morph.get("Inflection") and '連用形' in doc[token.i].morph.get("Inflection")[0] and len(doc) > token.i + 1 and doc[token.i + 1].pos_ == 'NOUN':   # 連用名　お届けキャンペーン　
                return {}
            if token.pos_ == 'VERB' or token.pos_ == 'ADJ' or (token.dep_ == 'nmod' and token.i > 0 and doc[token.i - 1].pos_ == 'ADP') or (token.dep_ == 'ROOT' and token.tag_ == '名詞-普通名詞-サ変可能'):
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'obl' and (doc[token.i - 1].lemma_ == 'を' and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'に'):
                return self.predicate_phrase_get(token.i, *doc)
            elif token.tag_ == '名詞-普通名詞-副詞可能' and (token.lemma_ == 'ため') and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'の':    # 〜ための
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'acl' and token.lemma_ == 'する':  # 〜を〇〇する〇〇
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'acl' and token.tag_ == '動詞-一般':  # 連体修飾
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'advcl' and token.pos_ == 'NOUN' and token.tag_ != "補助記号-一般" and len(doc) > token.i + 1 and doc[token.i + 1].tag_ == '補助記号-読点':  # 〇〇が〇〇円
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'nmod' and token.pos_ == 'NOUN' and doc[token.head.i].dep_ == 'ROOT' and len(doc) > token.i + 1 and doc[token.i + 1].tag_ == '補助記号-読点':  # 〇〇を〇〇円、〇〇を〇〇円
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'obl' and len(doc) > token.i + 2 and doc[token.i + 1].lemma_ == 'と' and doc[token.i + 2].pos_ == 'AUX':  # 〇〇とする
                return self.predicate_phrase_get(token.i, *doc)
            elif len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX':
                return self.predicate_phrase_get(token.i, *doc)
            elif len(doc) > token.i + 2 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'PUNCT' and doc[token.i + 2].pos_ == 'AUX':
                return self.predicate_phrase_get(token.i, *doc)
            elif is_meishi_syuusyoku:     # 〇〇が〇〇で、　名詞が格を伴って名詞を修飾している場合
                return self.predicate_phrase_get(token.i, *doc)
            elif token.tag_ == '名詞-普通名詞-サ変可能' and ((len(doc) > token.i + 1 and doc[token.i + 1].pos_ == 'ADP') or (len(doc) > token.i + 2 and doc[token.i + 1].pos_ == 'PUNCT' and doc[token.i + 2].pos_ == 'ADP')):
                return {}
            elif token.tag_ == '名詞-普通名詞-サ変可能' and (len(doc) <= token.i + 1 or doc[token.i + 1].pos_ != 'ADP') and (not doc[token.i - 1].morph.get("Inflection") or '連体形' not in doc[token.i - 1].morph.get("Inflection")[0]):
                return self.predicate_phrase_get(token.i, *doc)
            elif token.pos_ == 'ADV' and (len(doc) <= token.i + 1 or doc[token.i + 1].lemma_ == '、') and (doc[token.i - 1].lemma_ == 'は'):
                return self.predicate_phrase_get(token.i, *doc)
            ###################
            #
            #   普通名詞 + する　のかたちの最終述部
            #
            elif len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'VERB') and token.dep_ == 'ROOT' and doc[token.i + 1].lemma_ == 'する':
                return self.predicate_phrase_get(token.i, *doc)
            #   〇〇 + を + 〇〇 + に、... 　
            #
            elif token.i > 0 and doc[token.i - 1].lemma_ == 'を' and len(doc) > token.i + 2 and token.pos_ == 'NOUN' and doc[token.i + 1].lemma_ == 'に' and doc[token.i + 2].tag_ == '補助記号-読点':
                return self.predicate_phrase_get(token.i, *doc)
            #   〇〇 + を + 〇〇 + の... 　
            #
            elif token.i > 0 and doc[token.i - 1].lemma_ == 'を' and len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and doc[token.i + 1].lemma_ == 'の':
                return self.predicate_phrase_get(token.i, *doc)
            #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
            #
            elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and (len(doc) > token.i + 1 and (token.pos_ == 'NOUN' and token.tag_ != '接尾辞-名詞的-副詞可能' and token.tag_ != '接尾辞-名詞的-助数詞' and token.tag_ != '名詞-普通名詞-助数詞可能' and token.tag_ != '名詞-普通名詞-形状詞可能' and token.tag_ != '名詞-普通名詞-副詞可能') and doc[token.i + 1].tag_ == '補助記号-読点'):
                return self.predicate_phrase_get(token.i, *doc)
            #   〇〇　＋　を　＋　普通名詞。　　　体言止 連用中止
            #
            if doc[token.i].lemma_ == 'もの' or doc[token.i].lemma_ == 'こと' or doc[token.i].lemma_ == 'ため' or doc[token.i].lemma_ == 'とき' or doc[token.i].lemma_ == '際' or doc[token.i].lemma_ == '人' or doc[token.i].lemma_ == '場合':
                return {}
            elif token.i > 0 and (doc[token.i - 1].pos_ == 'ADP' or doc[token.i - 1].pos_ == 'SCONJ') and (token.pos_ == 'NOUN' and ((token.dep_ == 'ROOT' and token.i == token.head.i) or (len(doc) > token.i + 1 and doc[token.i + 1].pos_ == 'SYM'))):
                return self.predicate_phrase_get(token.i, *doc)
            elif len(doc) > token.i + 1 and token.tag_ == '形状詞-一般' and doc[token.i + 1].tag_ == '助動詞':
                return self.predicate_phrase_get(token.i, *doc)
            elif len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能':
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'ROOT' and doc[len(doc) - 1].head.i == token.i:
                return self.predicate_phrase_get(token.i, *doc)
            elif len(doc) > token.i + 2 and token.tag_ == '名詞-普通名詞-サ変可能' and token.dep_ == 'nmod' and token.head.dep_ == 'obj' and doc[token.i + 1].lemma_ == 'や' and self.rentai_check(token.i + 2, *doc):
                return self.predicate_phrase_get(token.i, *doc)
            elif token.dep_ == 'ROOT' and token.head.i == token.i:
                return self.predicate_phrase_get(token.i, *doc)
            else:
                return {}

        else:
            return {}
