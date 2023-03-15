from chunker import ChunkExtractor
from case_information_get import CaseExtractor

class MainVerbChek:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.verb_chunk = chunker.verb_chunk
        case_get = CaseExtractor()
        self.case_get = case_get.case_get


    def main_verb_chek(self, pt, *doc):
        ##########################################################################################################################################
        #    メイン述部の判断
        #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
        #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
        ##########################################################################################################################################
        rule_id = -1
        #                """
        # 複合動詞の場合、複合動詞間のかかり受けがあるのでそれを排除して最終かかり先を求める
        predic_head = pt
        if doc[predic_head].pos_ == "AUX" and predic_head > 0 and doc[predic_head - 1].pos_ == "VERB":
            predic_head = predic_head - 1
        if doc[pt].pos_ == 'VERB':
            comp_verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
            for i in range(comp_verb['lemma_start'], comp_verb['lemma_end']):
                if predic_head < doc[i].head.i:
                    predic_head = doc[i].head.i
        case = self.case_get(predic_head, *doc)
        #
        # 述部が最終述部の場合
        #
        if (doc[predic_head].i == doc[predic_head].head.i and (doc[predic_head].pos_ == "VERB" or doc[predic_head].pos_ == "ADV") or  # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
                (len(doc) > doc[predic_head].i + 1 and (doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[doc[predic_head].i + 1].lemma_ == 'する'))):  # 普通名詞　＋　する が文末の場合
            rule_id = 100
        #
        # 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
        #
#        elif doc[predic_head].pos_ == "VERB" and doc[doc[predic_head].i].head.i == doc[doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB":  # 最後の動詞を修飾する動詞？
        elif (doc[predic_head].pos_ == "VERB" and "には" not in case) and doc[doc[predic_head].i].head.i == doc[doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB":  # 最後の動詞を修飾する動詞？
            rule_id = 102
        elif len(doc) > doc[doc[predic_head].i].head.i + 1 and doc[predic_head].pos_ == "VERB" and doc[doc[predic_head].i].head.pos_ == "VERB" and doc[doc[doc[predic_head].i].head.i + 1].lemma_ == "と" and doc[doc[predic_head].i].head.head.dep_ == "ROOT":  # 〇〇し、〇〇すると〇〇した
            rule_id = 115
        #
        #  最終術部が名詞から形成される場合
        #
        elif len(doc) > doc[predic_head].i + 1 and doc[predic_head].head.head.lemma_ == "する" and doc[doc[predic_head].i + 1].lemma_ == '決定':  # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
            rule_id = 104
        elif (doc[predic_head].pos_ == 'NOUN' or doc[predic_head].pos_ == 'PROPN') and doc[predic_head].dep_ == 'ROOT' and doc[predic_head].i == doc[predic_head].head.i:  # 文末が　体言止
            rule_id = 105
        elif doc[predic_head].head.tag_ == '名詞-普通名詞-サ変可能' and doc[predic_head].head.dep_ == 'ROOT' and doc[predic_head].head.i == doc[doc[predic_head].head.i].head.i and (len(doc) > predic_head + 1 and doc[predic_head + 1].orth_ != 'で'):  # 文末が　体言止
            rule_id = 107
        elif len(doc) > predic_head + 2 and doc[predic_head].pos_ == 'NOUN' and doc[predic_head + 1].pos_ == 'AUX' and doc[predic_head + 1].lemma_ == 'する' and doc[predic_head + 2].lemma_ == 'ます':  # 〇〇します
            rule_id = 108
        elif doc[predic_head].pos_ == 'AUX' and doc[predic_head].head.dep_ == 'ROOT' and (doc[predic_head].lemma_ == 'だ' or doc[predic_head].lemma_ == 'です'):  # 名詞＋です。
            rule_id = 109
        elif len(doc) > predic_head + 3 and doc[predic_head].pos_ == 'NOUN' and doc[predic_head + 1].lemma_ == 'と' and doc[predic_head + 2].lemma_ == 'する' and doc[predic_head + 3].lemma_ == 'て':  # 〇〇としている
            rule_id = 110
        elif doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].dep_ == 'ROOT' and doc[doc[predic_head].head.i].pos_ == 'NOUN':  # 〇〇する〇〇。　体言止への最後の動詞
            rule_id = 111
        elif doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].lemma_ == 'こと' and doc[doc[doc[predic_head].head.i].head.i].dep_ == 'ROOT':  # 〇〇することを[動詞]。
            rule_id = 112
        elif len(doc) > doc[predic_head].i + 1 and doc[predic_head].pos_ == 'NOUN' and doc[doc[predic_head].i + 1].lemma_ == 'いたす':  # 〇〇いたします。
            rule_id = 113
#        elif len(doc) > doc[predic_head].i + 1 and doc[predic_head].pos_ == 'NOUN' and doc[doc[predic_head].head.i].dep_ == 'ROOT' and (doc[doc[predic_head].i + 1].pos_ == 'AUX' or doc[doc[predic_head].i + 1].pos_ == 'PUNCT'):  # 〇〇します。 がROOTになっていないときの例外処理
        elif (len(doc) > doc[predic_head].i + 1 and doc[predic_head].pos_ == 'NOUN' and doc[doc[predic_head].head.i].dep_ == 'ROOT' and
              ((doc[doc[predic_head].i + 1].pos_ == 'AUX' and (not doc[predic_head + 1].morph.get("Inflection") or (doc[predic_head + 1].morph.get("Inflection") and '仮定形' not in doc[predic_head + 1].morph.get("Inflection")[0]))) or
               doc[doc[predic_head].i + 1].pos_ == 'PUNCT')):  # 〇〇します。 がROOTになっていないときの例外処理
            rule_id = 114
        elif doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].lemma_ == '方向' and doc[doc[predic_head].head.i + 1].lemma_ == 'で' and doc[doc[doc[predic_head].head.i].head.i].dep_ == 'ROOT':  # 〇〇する方向で[動詞]。
            rule_id = 116
        elif doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].lemma_ == '方針' and doc[doc[predic_head].head.i + 1].lemma_ == 'を' and doc[doc[doc[predic_head].head.i].head.i].dep_ == 'ROOT':  # 〇〇する方向で[動詞]。
            rule_id = 117
        elif len(doc) > predic_head + 2 and doc[predic_head].pos_ == 'VERB' and doc[predic_head + 1].pos_ == 'AUX' and (doc[predic_head + 1].lemma_ == 'た' or doc[predic_head + 1].lemma_ == 'だ') and doc[predic_head + 2].lemma_ == 'が':  # 〇〇したが、
            rule_id = 118
        elif doc[predic_head].pos_ == 'ADJ' and doc[predic_head].dep_ == 'ROOT':  # 形容詞
            rule_id = 119
        elif len(doc) > doc[predic_head].head.i + 2 and doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].pos_ == 'VERB' and doc[doc[predic_head].head.i + 1].pos_ == 'AUX' and doc[doc[predic_head].head.i + 1].lemma_ != 'ない' and (doc[doc[predic_head].head.i + 2].lemma_ == 'た' or doc[doc[predic_head].head.i + 2].lemma_ == 'だ'):  # 〇〇すると〇〇したと[動詞]。
            rule_id = 120
        elif len(doc) > predic_head + 1 and doc[predic_head].pos_ == 'VERB' and doc[predic_head + 1].lemma_ == 'する' and doc[doc[predic_head].head.i].lemma_ == 'する':  # 〇〇し〇〇する。
            rule_id = 121
        elif (doc[predic_head].pos_ == 'NOUN' or doc[predic_head].pos_ == 'PRON')and doc[predic_head].head.i <= predic_head:  # 体言どめ
            rule_id = 122
        elif doc[predic_head].pos_ == 'ADP' and doc[doc[predic_head].head.i].dep_ == "ROOT":  # 体言どめ + 助詞
            rule_id = 123
        elif doc[predic_head].pos_ == 'SCONJ' and doc[doc[predic_head].head.i].pos_ == 'ADP' and doc[doc[doc[predic_head].head.i].head.i].dep_ == "ROOT":  # 体言どめ + 助詞
            rule_id = 124
        elif doc[predic_head].pos_ == 'NUM' and doc[doc[predic_head].head.i].dep_ == "ROOT":  # 体言どめ
            rule_id = 125
        elif doc[predic_head].pos_ == 'PUNCT' and doc[doc[predic_head].head.i].dep_ == "ROOT":  # カッコ付きの体言どめ
            rule_id = 126
        elif doc[predic_head].pos_ == 'VERB' and doc[doc[predic_head].head.i].pos_ == 'ADJ' and doc[doc[predic_head].head.i].dep_ == "ROOT":  # 形容詞語幹 + 動詞
            rule_id = 127
        elif doc[predic_head].pos_ == 'ADJ' and doc[doc[predic_head].head.i].dep_ == 'ROOT':  # 必要なこととは
            rule_id = 128
        return rule_id
