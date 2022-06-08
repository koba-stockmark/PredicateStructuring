from chunker import ChunkExtractor

class MainVerbChek:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.verb_chunk = chunker.verb_chunk


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
        if doc[pt].pos_ == 'VERB':
            comp_verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
            for i in range(comp_verb['lemma_start'], comp_verb['lemma_end']):
                if predic_head < doc[i].head.i:
                    predic_head = doc[i].head.i
        #
        # 述部が最終述部の場合
        #
        if (doc[predic_head].i == doc[predic_head].head.i and (doc[predic_head].pos_ == "VERB" or doc[predic_head].pos_ == "ADV") or  # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
                (len(doc) > doc[predic_head].i + 1 and (doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[doc[predic_head].i + 1].lemma_ == 'する'))):  # 普通名詞　＋　する が文末の場合
            rule_id = 100
        #
        # 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
        #
        elif doc[predic_head].pos_ == "VERB" and doc[doc[predic_head].i].head.i == doc[doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB":  # 最後の動詞を修飾する動詞？
            rule_id = 102
            """
        #
        # 最終述部でない場合 (終止形は主述部とする)  多くですぎるので要検討
        #
        elif ((len(doc) > predic_head + 1 and doc[predic_head].pos_ == "VERB" and doc[predic_head + 1].pos_ == "AUX" and doc[predic_head + 1].morph.get("Inflection") and '終止形' in doc[predic_head + 1].morph.get("Inflection")[0]) or
            (doc[predic_head].morph.get("Inflection") and '終止形' in doc[predic_head].morph.get("Inflection")[0])):
            rule_id = 106
        """
        #
        #  最終術部が名詞から形成される場合
        #
        elif len(doc) > doc[predic_head].i + 1 and doc[predic_head].head.head.lemma_ == "する" and doc[doc[predic_head].i + 1].lemma_ == '決定':  # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
            rule_id = 104
        elif doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[predic_head].i == doc[predic_head].head.i:  # 文末が　体言止
            rule_id = 105
        elif doc[predic_head].head.tag_ == '名詞-普通名詞-サ変可能' and doc[predic_head].head.dep_ == 'ROOT' and doc[predic_head].head.i == doc[doc[predic_head].head.i].head.i:  # 文末が　体言止
            rule_id = 107
        return rule_id
