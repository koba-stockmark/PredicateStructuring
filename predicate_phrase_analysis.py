from chunker import ChunkExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from predicate_split import VerbSpliter
from phase_check import PhaseCheker
from kanyouku_check import KanyoukuExtractor
from case_information_get import CaseExtractor

class PredicatePhraseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.compaound = chunker.compaound
        self.rentai_check = chunker.rentai_check
        c_g = CaseExtractor()
        self.case_get = c_g.case_get
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.object_devide = v_s.object_devide
        p_c = PhaseCheker()
        self.phase_chek = p_c.phase_chek
        k = KanyoukuExtractor()
        self.kanyouku_chek = k.kanyouku_chek
        self.kanyouku_get = k.kanyouku_get


    """
    述部の生成
    """
    def predicate_phrase_get(self, pt,  *doc):
        verb_w = ''
        rule_id = 0
        verb = {}
        modality_w = ''
        tonaru_dic = ['可能', 'ゼロ', '原料']
        #
        #    形容詞
        #
        if doc[pt].tag_ == '形容詞-一般' and (len(doc) <= pt + 1 or doc[pt + 1].tag_ != '接尾辞-名詞的-一般'):
            verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
            verb_w = verb["lemma"]
            modality_w = verb["modality"]
            rule_id = 1
        elif doc[pt].norm_ == "為る":
            if doc[pt - 1].lemma_ == 'たり':
                return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1, 'modality': '', 'rule_id': -1}
            #
            #             述部が  名詞＋（と、に）する（目標とする　など）
            #
            if (doc[doc[pt].i - 1].orth_ == 'に' or doc[doc[pt].i - 1].orth_ == 'と') and doc[pt].i != doc[pt].i - 2 and doc[doc[pt].i - 2].tag_ != '助動詞' and doc[doc[pt].i - 2].orth_ != 'よう' and doc[doc[pt].i - 2].norm_ != '出来る' and doc[doc[pt].i - 2].pos_ != 'PUNCT':  # 【名詞】に(と)する
                verb = self.verb_chunk(doc[pt].i - 2, *doc)
                verb["lemma_end"] = pt
                verb_w = self.compaound(verb["lemma_start"], pt, *doc)
                modality_w = verb["modality"]
                if doc[doc[pt].i - 2].tag_ == '補助記号-括弧閉':
                    verb = self.verb_chunk(doc[pt].i - 3, *doc)
                    verb["lemma_end"] = pt
                    verb_w = self.compaound(verb["lemma_start"], pt, *doc)
                    modality_w = verb["modality"]
                rule_id = 2
            #
            #             述部が  ○○の＋名詞＋を＋する（調査をする　など）、　名詞＋サ変名詞＋する（内部調査をする　など）
            #
            elif doc[doc[pt].i - 1].orth_ == 'を':
                if doc[doc[pt].i - 2].pos_ == 'PRON':  # 何をする　　→　候補から外す
                    verb_w = ''
                else:
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    if doc[doc[pt].i - 2].tag_ == '名詞-普通名詞-サ変可能':
                        verb_w = verb["lemma"] + doc[pt].lemma_
                    else:
                        verb_w = verb["lemma"] + doc[pt - 1].lemma_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 3
            #
            #             述部が  形容詞＋する（少なくする　など）
            #
            elif doc[doc[pt].i - 1].pos_ == 'AUX':
                if doc[pt].i - 4 >= 4 and (doc[doc[pt].i - 1].tag_ == '接尾辞-形容詞的' or doc[doc[pt].i - 1].tag_ == '助動詞') and doc[doc[pt].i - 2].pos_ == 'VERB':
                    # ○○を使いやすくする -> 使いやすくする
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = doc[doc[pt].i - 2].orth_ + doc[doc[pt].i - 1].orth_ + verb["lemma"]
                    verb["lemma_start"] = doc[doc[pt].i - 2].i
                    modality_w = verb["modality"]
                    rule_id = 4
            elif doc[doc[pt].i - 1].pos_ == 'ADJ':
                if doc[pt].i - 4 >= 4 and doc[doc[pt].i - 1].tag_ == '形容詞-非自立可能' and doc[doc[pt].i - 2].pos_ == 'NOUN':
                    # ○○を余儀なくする -> 余儀なくする
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 5
                elif doc[doc[pt].i - 1].tag_ == '形容詞-一般' or doc[doc[pt].i - 1].tag_ == '形容詞-非自立可能' or (doc[doc[pt].i - 1].tag_ == '副詞' and doc[doc[pt].i - 1].lemma_ == 'よく'):
                    # ○○を少なくする -> 少なくする
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 6
                else:
                    rule_id = 7
            #
            #     「〇〇」する　→　〇〇する
            #
            elif doc[doc[pt].i - 1].pos_ == 'PUNCT':
                verb = self.verb_chunk(doc[pt].i - 2, *doc)
                verb_w = verb["lemma"] + doc[pt].lemma_
                verb["lemma_end"] = doc[pt].i
                modality_w = verb["modality"]
                rule_id = 8
            #
            #   どうする、そうする...
            #
            elif doc[doc[pt].i - 1].pos_ == 'ADV':
                verb = self.verb_chunk(doc[pt].i - 1, *doc)
                verb_w = verb["lemma"] + doc[pt].lemma_
                verb["lemma_end"] = doc[pt].i
                modality_w = verb["modality"]
                rule_id = 9
            #
            #   〇〇の〇〇を〇〇で（と、から..）する　　　「…をする」の変形版　　→　〇〇の〇〇を〇〇する　と同じ処理　目的語は　更に前の　「〇〇の」　ex.エンジンの開発を東京でする
            #
            elif (doc[doc[pt].i - 1].pos_ == 'ADP' and doc[doc[pt].i - 1].lemma_ != 'を' and doc[doc[pt].i - 1].lemma_ != 'に' and doc[doc[pt].i - 1].lemma_ != 'と') and doc[doc[pt].i - 2].tag_ != '助詞-接続助詞':
                verb_w = ''
                ret_obj = self.num_chunk(doc[pt].i, *doc)
                for k in range(ret_obj["lemma_start"], ret_obj["lemma_end"]):
                    if doc[k].lemma_ == 'の' and doc[k].pos_ == 'ADP':
                        verb_w = self.compaound(k + 1, ret_obj["lemma_end"], *doc)
                        verb["lemma_start"] = k + 1
                        verb["lemma_end"] = ret_obj["lemma_end"]
                        rule_id = 10
                        break
                if not verb_w:
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 11
            #
            #   〇〇の（名詞）をする（主語）　ex.　小学校の教員をする弟
            #
            else:
                verb = self.verb_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = verb["modality"]
                rule_id = 12

        #
        #   普通名詞 + する　のかたちの最終述部
        #
        elif len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' or doc[pt].pos_ == 'VERB') and doc[pt].dep_ == 'ROOT' and doc[doc[pt].i + 1].lemma_ == 'する':
            verb = self.verb_chunk(doc[pt].i, *doc)
            verb_w = verb["lemma"] + 'する'
            modality_w = verb["modality"]
            rule_id = 13
        #
        #   〇〇 + を + 〇〇 + に、... 　
        #
        elif len(doc) > doc[pt].i + 2 and doc[pt].pos_ == 'NOUN' and doc[doc[pt].i + 1].lemma_ == 'に' and \
                ((doc[doc[pt].i + 2].tag_ == '補助記号-読点' or doc[doc[pt].i + 2].pos_ == 'NOUN' or doc[doc[pt].i + 2].tag_ == '名詞-普通名詞-副詞可能') and (len(doc) <= doc[pt].i + 2 or doc[doc[pt].i + 3].lemma_ != 'に')):
            verb = self.verb_chunk(doc[pt].i, *doc)
            verb_w = verb["lemma"] + doc[doc[pt].i + 1].lemma_ + '(する)'
            verb["lemma_end"] = doc[doc[pt].i + 1].i
            modality_w = verb["modality"]
            rule_id = 14
        #
        #   〇〇 + を + 〇〇 + の... 　
        #
        elif len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' or doc[pt].pos_ == 'PROPN') and doc[doc[pt].i + 1].lemma_ == 'の':
            if doc[pt].tag_ == '名詞-普通名詞-副詞可能':  # 〇〇　＋　を　＋　ため　＋　の
                verb = self.verb_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"] + '(だ)'
                modality_w = verb["modality"]
                rule_id = 15
        #
        #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
        #
        elif (len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' and doc[pt].tag_ != '接尾辞-名詞的-副詞可能' and doc[pt].tag_ != '接尾辞-名詞的-助数詞' and doc[pt].tag_ != '名詞-普通名詞-助数詞可能') and
              doc[pt].tag_ != '名詞-普通名詞-形状詞可能' and doc[pt].tag_ != '名詞-普通名詞-副詞可能' and doc[doc[pt].i + 1].tag_ == '補助記号-読点' and doc[doc[pt].i - 1].lemma_ != 'の'):
            verb = self.verb_chunk(doc[pt].i, *doc)
            verb_w = verb["lemma"] + '(する)'
            rule_id = 16
        #
        #   〇〇　＋　を　＋　普通名詞。　　　体言止 連用中止
        #
        elif doc[pt].pos_ == 'NOUN' and ((doc[pt].dep_ == 'ROOT' and doc[pt].i == doc[pt].head.i) or (len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].pos_ == 'SYM')):
            if doc[pt - 1].lemma_ == '日' or doc[pt - 1].tag_ == '名詞-普通名詞-副詞可能':
                verb = self.verb_chunk(doc[pt].i, *doc)
            else:
                verb = self.verb_chunk(doc[pt].i, *doc)
                if doc[verb["lemma_end"]].tag_ == '補助記号-句点':
                    verb["lemma"] = verb["lemma"][:-1]
                    verb["lemma_end"] = verb["lemma_end"] - 1
            if len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].lemma_ == 'です' or doc[doc[pt].i + 1].lemma_ == 'だ'):
                verb_w = verb["lemma"] + 'です'
                verb["lemma_end"] = doc[doc[pt].i + 1].i
            elif verb["lemma"].endswith('中'):
                verb_w = verb["lemma"] + '(です)'
            elif doc[verb["lemma_end"]].tag_ == '接尾辞-名詞的-助数詞' or doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-助数詞可能' or doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-形状詞可能' or doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-副詞可能' or (doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-一般' and doc[verb["lemma_end"]].lemma_ != 'お知らせ'):
                verb_w = verb["lemma"] + '(です)'
            elif doc[doc[pt].i].morph.get("Inflection") and '連用形' in doc[doc[pt].i].morph.get("Inflection")[0]:
                verb_w = verb["lemma"]
            else:
                verb_w = verb["lemma"] + '(する)'
            rule_id = 17
        #
        #           ○○する　以外の一般の動詞
        #
        else:
            ###############################
            #    形式動詞
            ###############################
            if doc[pt].lemma_ == 'なる' and doc[pt - 1].lemma_ != 'に' and doc[pt - 1].lemma_ != 'と' and (doc[pt - 2].pos_ != 'AUX' or (doc[pt - 3].lemma_ != 'の' and doc[pt - 3].pos_ != 'AUX')):  # 形式動詞   〜のようになる　は例でNG
                if doc[doc[pt].i - 2].pos_ != 'PUNCT' and doc[doc[pt].i - 1].pos_ == 'ADP' and doc[doc[pt].i - 1].orth_ == 'は' and doc[doc[pt].i - 2].pos_ == 'AUX' and doc[doc[pt].i - 2].orth_ == 'に':  # 〜となる　〜になる
                    verb = self.verb_chunk(doc[doc[pt].i].i - 3, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 2].orth_ + doc[doc[pt].i - 1].orth_ +doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 18
                elif doc[doc[pt].i - 2].pos_ != 'PUNCT' and doc[doc[pt].i - 2].orth_ != 'よう' and (doc[doc[pt].i - 1].pos_ == 'ADP' or (doc[doc[pt].i - 1].pos_ == 'AUX' and doc[doc[pt].i - 1].orth_ == 'に')):  # 〜となる　〜になる
                    verb = self.verb_chunk(doc[doc[pt].i - 1].i - 1, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 18
                elif doc[pt - 1].pos_ == "ADJ":  # 安く＋なる
                    verb = self.verb_chunk(pt - 1, *doc)
                    verb_w = doc[pt - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 18
                else:
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 19
            elif len(doc) > doc[pt].i + 3 and doc[doc[pt].i - 1].lemma_ != 'に' and (doc[doc[pt].i + 1].tag_ == '動詞-非自立可能') and (doc[doc[pt].i + 2].tag_ == '助詞-接続助詞' and (doc[doc[pt].i + 2].lemma_ == 'て' or doc[doc[pt].i + 2].lemma_ == 'で')) and (doc[doc[pt].i + 3].pos_ == 'VERB' and doc[doc[pt].i + 3].tag_ != '動詞-非自立可能'):  # 〇〇して〇〇する
                verb1 = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb2 = self.verb_chunk(doc[doc[pt].i + 3].i, *doc)
                verb["lemma"] = ''
                for i in range(verb1["lemma_start"], verb2["lemma_end"]):
                    verb["lemma"] = verb["lemma"] + doc[i].orth_
                verb["lemma"] = verb["lemma"] + doc[verb2["lemma_end"]].lemma_
                verb["lemma_start"] = verb1["lemma_start"]
                verb["lemma_end"] = verb2["lemma_end"]
                if doc[verb2["lemma_end"]].tag_ == '名詞-普通名詞-サ変可能' or doc[verb2["lemma_end"]].tag_ == '名詞-普通名詞-サ変形状詞可能':
                    verb_w = verb["lemma"] + 'する'
                else:
                    verb_w = verb["lemma"]
                modality_w = verb2["modality"]
                rule_id = 20
            elif len(doc) > doc[pt].i + 2 and doc[doc[pt].i - 1].lemma_ != 'に' and (doc[doc[pt].i + 1].tag_ == '助詞-接続助詞' and (doc[doc[pt].i + 1].lemma_ == 'て' or doc[doc[pt].i + 1].lemma_ == 'で')) and (doc[doc[pt].i + 2].pos_ == 'VERB' and doc[doc[pt].i + 2].tag_ != '動詞-非自立可能' and doc[doc[pt].i + 2].tag_ != '名詞-普通名詞-サ変可能'):  # 〇〇て(で)〇〇る
                verb1 = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb2 = self.verb_chunk(doc[doc[pt].i + 2].i, *doc)
                verb["lemma"] = ''
                for i in range(verb1["lemma_start"], verb2["lemma_end"]):
                    verb["lemma"] = verb["lemma"] + doc[i].orth_
                verb["lemma"] = verb["lemma"] + doc[verb2["lemma_end"]].lemma_
                verb["lemma_start"] = verb1["lemma_start"]
                verb["lemma_end"] = verb2["lemma_end"]
                if doc[verb2["lemma_end"]].tag_ == '名詞-普通名詞-サ変可能':
                    verb_w = verb["lemma"] + 'する'
                else:
                    verb_w = verb["lemma"]
                modality_w = verb2["modality"]
                rule_id = 21
            elif len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].tag_ == '動詞-非自立可能'):  # 動詞　＋　補助動詞
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                if len(doc) > doc[pt].i + 3 and doc[doc[pt].i + 2].tag_ == '形状詞-助動詞語幹' and doc[doc[pt].i + 3].orth_ == 'に' and doc[doc[pt].i + 4].pos_ == 'VERB':  # 動詞　＋　補助動詞 +  ように + 動詞
                    verb2 = self.verb_chunk(doc[doc[pt].i].i + 4, *doc)
                    if verb2["lemma_start"] <= verb["lemma_start"]:
                        verb["lemma_start"] = verb2["lemma_start"]
                        verb_w = verb2["lemma"]
                        verb_w = self.compaound(verb["lemma_start"], verb2["lemma_end"], *doc)
                    else:
                        verb_w = verb["lemma"] + doc[doc[pt].i + 2].orth_ + "に" + verb2["lemma"]
                        verb_w = self.compaound(verb["lemma_start"], verb2["lemma_end"], *doc)
                    verb["lemma_end"] = verb2["lemma_end"]
                    modality_w = verb2["modality"]
                    rule_id = 42
                else:
                    if doc[verb["lemma_end"]].lemma_ == 'ため' or doc[verb["lemma_end"]].lemma_ == 'もの' or doc[verb["lemma_end"]].lemma_ == 'とき' or doc[verb["lemma_end"]].lemma_ == '際' or doc[verb["lemma_end"]].lemma_ == 'こと' or doc[verb["lemma_end"]].lemma_ == '場合':
                        verb_w = verb["lemma"] + '(です)'
                    elif (doc[doc[pt].i].tag_ != '動詞-一般' and doc[doc[pt].i].tag_ != '形容詞-一般' and
                            (doc[verb["lemma_end"] + 1].lemma_ == 'する' or doc[verb["lemma_end"] + 1].lemma_ == 'できる' or doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-サ変可能' or
                             doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-サ変形状詞可能' or doc[verb["lemma_end"]].tag_ == '名詞-普通名詞-一般')):
                        verb_w = verb["lemma"] + 'する'
                        verb["lemma_end"] = verb["lemma_end"] + 1
                    else:
                        verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 22
            ###############################
            #    形式名詞
            ###############################
            elif doc[pt].lemma_ == 'ため':  # 形式名詞
                if doc[doc[pt].i - 1].pos_ == 'AUX' and doc[doc[pt].i - 1].lemma_ == 'する':
                    verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 23
                elif doc[doc[pt].i - 1].pos_ == 'VERB':
                    verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 24
            ###############################
            #    普通名詞　〇〇　＋　です
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-普通名詞-形状詞可能' and doc[doc[pt].i + 1].lemma_ == 'です':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].orth_
                verb["lemma_end"] = doc[doc[pt].i + 1].i
                modality_w = verb["modality"]
                rule_id = 42
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...） + する
            ###############################
            elif len(doc) > doc[pt].i + 2 and (doc[pt].tag_ == '名詞-普通名詞-一般' or doc[pt].tag_ == '接尾辞-名詞的-一般') and doc[doc[pt].i + 1].pos_ == 'ADP' and doc[doc[pt].i + 1].lemma_ != 'に' and doc[doc[pt].i + 2].lemma_ == 'する':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].orth_ + doc[doc[pt].i + 2].lemma_
                verb["lemma_end"] = doc[doc[pt].i + 2].i
                modality_w = verb["modality"]
                rule_id = 25
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇 + 化　＋　する
            ###############################
            elif len(doc) > doc[pt].i + 2 and doc[pt].tag_ == '名詞-普通名詞-一般' and doc[doc[pt].i + 1].head.i != doc[doc[pt].i + 1].i and doc[doc[pt].i + 1].tag_ == '接尾辞-名詞的-サ変可能' and doc[doc[pt].i + 2].lemma_ == 'する':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].orth_ + doc[doc[pt].i + 2].lemma_
                verb["lemma_end"] = doc[doc[pt].i + 2].i
                modality_w = verb["modality"]
                rule_id = 26
            ###############################
            #    単独の動詞　普通名詞　〇〇　＋　を　＋　形容動詞(連用形以外)
            ###############################
            elif (len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '形状詞-一般' and doc[doc[pt].i + 1].lemma_ == 'だ' and
                    (doc[doc[pt].i + 1].head.morph.get("Inflection") and '連用形' not in doc[doc[pt].i + 1].head.morph.get("Inflection")[0]) and
                    (len(doc) < doc[pt].i + 2 or (len(doc) > doc[pt].i + 2 and doc[pt + 2].lemma_ != 'する'))):
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + 'にする'
                verb["lemma_end"] = verb["lemma_end"] + 2
                modality_w = verb["modality"]
                rule_id = 27
            ###############################
            #    単独の動詞　普通名詞　A〇〇　＋　を　＋　B動詞(使い)　＋　形容詞(やすく)　＋　C〇〇　＋　する　ex.　使いやすくバージョンアップする。  A-B の係り関係から A-C を作る
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].pos_ == 'AUX'  and doc[pt].head.pos_ == 'NOUN' and len(doc) > doc[pt].head.i + 1 and doc[doc[pt].head.i + 1].lemma_ == 'する':
                verb = self.verb_chunk(doc[pt].head.i, *doc)
                verb_w = verb["lemma"] + 'する'
                verb["lemma_end"] = verb["lemma_end"]
                modality_w = verb["modality"]
                rule_id = 28
                #### このルールだけ特別
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日　＋　から
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-普通名詞-副詞可能' and doc[doc[pt].i + 1].pos_ == 'ADP' and doc[doc[pt].i + 1].lemma_ == 'から':
                verb = self.verb_chunk(doc[doc[pt].head.i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].head.i + 1].orth_
                verb["lemma_end"] = doc[doc[pt].head.i + 1].i
                modality_w = verb["modality"]
                rule_id = 29
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...）
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-普通名詞-一般' and (doc[doc[pt].i + 1].pos_ == 'ADP' or doc[doc[pt].i + 1].pos_ == 'SCONJ'):
                verb_w = ''
                verb = self.num_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = ""
                verb_w = ''
                rule_id = 30
            elif len(doc) > doc[pt].i + 2 and doc[pt].tag_ == '名詞-普通名詞-一般' and doc[doc[pt].i + 1].pos_ == 'PUNCT' and doc[doc[pt].i + 2].pos_ == 'ADP':
                verb_w = ''
                verb = self.num_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = ""
                verb_w = ''
                rule_id = 31
            ###############################
            #    普通名詞　〇〇　＋　を　＋　接尾
            ###############################
            elif doc[pt].tag_ == '接尾辞-名詞的-副詞可能' or doc[pt].tag_ == '名詞-普通名詞-形状詞可能':
                verb_w = ''
                verb = self.num_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = ""
                verb_w = ''
                rule_id = 32
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日
            ###############################
            elif (doc[pt].tag_ == '接尾辞-名詞的-助数詞' or doc[pt].tag_ == '名詞-普通名詞-助数詞可能' or doc[pt].tag_ == '名詞-普通名詞-副詞可能') and (len(doc) <= doc[pt].i + 1 or (doc[doc[pt].i + 1].lemma_ != '」' and doc[doc[pt].i + 1].pos_ != "AUX")):
                verb_w = ''
                verb = self.num_chunk(doc[pt].i, *doc)
                verb["lemma"] = ""
                for ch in reversed(range(verb["lemma_start"], verb["lemma_end"] + 1)):
                    if doc[ch].lemma_ == "の":
                        verb["lemma_start"] = ch + 1
                        break
                    verb["lemma"] = doc[ch].orth_ + verb["lemma"]
                verb_w = verb["lemma"]
                modality_w = ""
                rule_id = 33
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-数詞' and doc[doc[pt].i + 1].pos_ == 'PUNCT':
                verb_w = ''
                verb = self.num_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = ""
                rule_id = 34
            ###############################
            #    〜を　形容詞　＋　できる
            ###############################
            elif doc[doc[pt].i - 1].tag_ == '形容詞-一般' and doc[pt].lemma_ == 'できる':
                verb = self.verb_chunk(doc[pt].i, *doc)
                modality_w = verb["modality"]
                verb_w = doc[doc[pt].i - 1].orth_ + verb["lemma"]
                verb["lemma"] = verb_w
                verb["lemma_start"] = verb["lemma_start"] - 1
                rule_id = 35
            ###############################
            #    〜にある
            ###############################
            elif doc[pt].i > 2 and doc[doc[pt].i - 2].pos_ != 'PUNCT' and doc[doc[pt].i - 2].pos_ != "PART" and doc[pt].lemma_ == 'ある' and (((doc[doc[pt].i - 1].lemma_ == 'に' or doc[doc[pt].i - 1].lemma_ == 'が') and
                doc[doc[pt].i - 1].tag_ == '助詞-格助詞') or (doc[doc[pt].i - 2].lemma_ == 'に' and doc[doc[pt].i - 1].lemma_ == 'は') or
                (doc[doc[pt].i - 1].lemma_ == 'で' and doc[doc[pt].i - 1].tag_ == '助動詞') or (doc[doc[pt].i - 2].lemma_ == 'で' and doc[doc[pt].i - 1].lemma_ == 'は')):
                if doc[doc[pt].i - 2].lemma_ == 'に' or doc[doc[pt].i - 2].lemma_ == 'で':
                    pre_verb = self.num_chunk(doc[pt].i - 3, *doc)
                else:
                    pre_verb = self.num_chunk(doc[pt].i - 2, *doc)
                verb = self.verb_chunk(doc[pt].i, *doc)
                modality_w = verb["modality"]
                if doc[doc[pt].i - 1].lemma_ == 'が':
                    verb_w = pre_verb["lemma"] + 'が' + verb["lemma"]
                else:
                    verb_w = pre_verb["lemma"] + 'に' + verb["lemma"]
                verb["lemma"] = verb_w
                verb["lemma_start"] = pre_verb["lemma_start"]
                rule_id = 36

            ###############################
            #    普通名詞　〇〇　＋ の　＋ 〇〇　＋　だ
            ###############################
                """
            elif len(doc) > pt + 1 and doc[pt - 1].lemma_ == 'の' and doc[pt].pos_ == 'NOUN' and doc[pt + 1].pos_ == 'AUX':
                verb = self.num_chunk(doc[pt].i, *doc)
                if doc[pt + 1].lemma_ == "だ":
                    verb_w = verb["lemma"] + '(だ)'
                else:
                    verb_w = verb["lemma"] + '(する)'
                modality_w = ""
                rule_id = 37
            """

            ###############################
            #    単独の動詞
            ###############################
            else:
                verb = self.verb_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = verb["modality"]
                #
                #  慣用句と普通動詞の処理の分離
                #
                kanyouku = self.kanyouku_chek(doc[pt].i, *doc)
                if len(kanyouku) > 0:
                    verb_w = self.kanyouku_get(kanyouku, *doc)
                    verb["lemma_start"] = kanyouku[0]
                    verb["lemma_end"] = kanyouku[-1]
                    rule_id = 38
                else:
                    if len(doc) > doc[pt].i + 2 and doc[doc[pt].i + 1].lemma_ == 'と' and (doc[doc[pt].i + 2].norm_ == '為る' or doc[doc[pt].i + 2].norm_ == '成る'):
                        verb_w = ''
                        rule_id = 42
                    elif doc[pt].i > 2 and doc[doc[pt].i - 2].lemma_ == 'よう' and (doc[doc[pt].i - 1].norm_ == 'に' or doc[doc[pt].i].norm_ == '成る'):
                            verb_w = ''
                            rule_id = 43
                    elif len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].pos_ != 'VERB' or doc[doc[pt].i + 1].tag_ == '名詞-普通名詞-サ変可能'):  # 動詞の連続でない
                        if (len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].tag_ == '接尾辞-名詞的-サ変可能' or
                                                          (len(doc) > verb["lemma_end"] + 1 and (doc[doc[pt].i + 1].pos_ == 'VERB' and doc[verb["lemma_end"] + 1].lemma_ == 'する')) or
                                                          (doc[doc[pt].i + 1].pos_ == 'VERB' and doc[doc[pt].i + 1].tag_ == '名詞-普通名詞-サ変可能' and doc[doc[pt].i + 1].head.i == doc[doc[pt].i].head.i))):  # 〇〇化する   〇〇いたす
                            verb_w = verb_w + 'する'
                        elif doc[pt].tag_ == '形状詞-一般' or doc[pt].pos_ == 'ADV':
                            if len(doc) > pt + 1 and doc[pt + 1].pos_ == 'NOUN':
                                return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1, 'modality': '', 'rule_id': -1}
                            verb_w = verb_w + '(だ)'
                        elif len(doc) > pt + 1 and doc[pt + 1].tag_ != '助詞-格助詞' and doc[pt + 1].lemma_ != "だ" and (doc[pt].pos_ == 'NOUN' and doc[pt].tag_ != '動詞-一般') and doc[doc[pt].head.i].norm_ == '為る':
                            add_p = doc[pt].head.i
                            for add_p in range(pt + 1, doc[pt].head.i):
                                if doc[add_p].pos_ == "NOUN":
                                    break
                                if doc[add_p].pos_ != "PUNCT":
                                    verb_w = verb_w + doc[add_p].orth_
                            verb["lemma_end"] = add_p
                            verb_w = verb_w + 'する'
                        elif (pt == verb["lemma_end"] or doc[verb["lemma_end"]].tag_ == "接尾辞-形状詞的") and ((doc[pt].pos_ == 'NOUN' and doc[pt].tag_ != '動詞-一般') or doc[pt].pos_ == 'PROPN') and (doc[pt].dep_ == 'obl' or doc[pt].dep_ == 'advcl' or doc[pt].dep_ == 'acl'):
                            verb_w = verb_w + '(です)'
                        elif pt == verb["lemma_end"] and ((doc[pt].pos_ == 'NOUN' and doc[pt].tag_ != '動詞-一般') or doc[pt].pos_ == 'PROPN') and doc[pt].dep_ == 'nmod':
                            verb_w = verb_w + '(する)'
                        elif doc[verb["lemma_end"]].lemma_ == "ところ" and len(doc) > verb["lemma_end"] + 1 and doc[verb["lemma_end"] + 1].lemma_ == 'です':
                            verb_w = verb_w + 'です'
                            verb["lemma_end"] = verb["lemma_end"] + 1
                        rule_id = 39
                    elif len(doc) == doc[pt].i + 1:
                        rule_id = 40
                    else:
                        verb_w = ''
                        rule_id = 41
        if verb_w:
            return {'lemma':verb_w, 'lemma_start':verb["lemma_start"], 'lemma_end':verb["lemma_end"], 'modality':modality_w, 'rule_id':rule_id}
        else:
            return {'lemma':'', 'lemma_start':-1, 'lemma_end':-1, 'modality':'', 'rule_id':-1}

