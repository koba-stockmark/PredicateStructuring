import spacy
from spacy.symbols import obj
from chunker import ChunkExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from verb_split import VerbSpliter
from phase_chek import PhaseCheker
from kanyouku_check import KanyoukuExtractor

class VerbPhraseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.case_get = chunker.case_get
        self.compaound = chunker.compaound
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get_from_object
        self.rentai_check = s_g.rentai_check
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.sub_verb_chek = v_s.sub_verb_chek
        self.object_devide = v_s.object_devide
        p_c = PhaseCheker()
        self.phase_chek = p_c.phase_chek
        k = KanyoukuExtractor()
        self.kanyouku_chek = k.kanyouku_chek
        self.kanyouku_get = k.kanyouku_get


    """
    動詞節の生成
    """
    def verb_phrase_get(self, pt,  *doc):
        verb_w = ''
        rule_id = 0
        verb = {}
        modality_w = ''
        if (doc[pt].lemma_ == "する"):
            #
            #             述部が  名詞＋（と、に）する（目標とする　など）
            #
            if (doc[doc[pt].i - 1].orth_ == 'に' or doc[doc[pt].i - 1].orth_ == 'と') and doc[pt].i != doc[pt].i - 2:  # 【名詞】に(と)する
                verb = self.verb_chunk(doc[pt].i - 2, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                modality_w = verb["modality"]
                if (doc[doc[pt].i - 2].tag_ == '補助記号-括弧閉'):
                    verb = self.verb_chunk(doc[pt].i - 3, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    modality_w = verb["modality"]
                rule_id = 1
            #
            #             述部が  ○○の＋名詞＋を＋する（調査をする　など）、　名詞＋サ変名詞＋する（内部調査をする　など）
            #
            elif doc[doc[pt].i - 1].orth_ == 'を' and doc[doc[pt].i - 2].pos_ == 'PRON':  # 何をする　　→　候補から外す
                verb_w = ''
                rule_id = 2
            elif (doc[doc[pt].i - 1].orth_ == 'を' and (doc[doc[pt].i - 2].tag_ == '名詞-普通名詞-サ変可能' or doc[doc[pt].i - 2].pos_ == 'PUNCT' or doc[doc[pt].i - 2].lemma_ == 'など')):
                # 名詞＋を＋する、　名詞＋など＋を＋する
                if (doc[doc[pt].i - 3].orth_ == 'の' or (doc[doc[pt].i - 3].orth_ == 'を' and doc[pt].i != doc[doc[pt].i - 2].i)):
                    # OBJ以外の名詞が「する」の前にある場合は「名詞＋する」をまとめる
                    ret_obj = self.num_chunk(doc[pt].i - 4, *doc)  # 内部の調査をする -> 内部を　調査する, 緊急使用を承認をする -> 緊急使用を　承認する
#                    obj_w = ret_obj['lemma']
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    verb_w = verb["lemma"] + doc[pt].lemma_
                    modality_w = verb["modality"]
                    rule_id = 3
                elif (doc[doc[pt].i - 3].pos_ == 'NOUN' and doc[doc[pt].i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                      (doc[doc[pt].i - 4].orth_ == 'の' or doc[doc[pt].i - 4].orth_ == 'を')):
                    ret_obj = self.num_chunk(doc[pt].i - 5, *doc)
#                    obj_w = ret_obj['lemma']
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    verb_w = verb["lemma"] + doc[pt].lemma_
                    modality_w = verb["modality"]
                    rule_id = 4
                elif (doc[doc[pt].i - 3].pos_ == 'NOUN' and doc[doc[pt].i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                      (doc[doc[pt].i - 3].tag_ != '名詞-普通名詞-形状詞可能' and doc[doc[pt].i - 3].tag_ != '接頭辞')):
                    # 内部調査をする -> 内部を　調査する　でも　緊急調査をする -> 緊急を　調査する　ではない!!　組み合わせで判断する必要あり！
                    ret_obj = self.num_chunk(doc[pt].i - 3, *doc)
#                    obj_w = ret_obj['lemma']
                    verb_w = doc[doc[pt].i - 2].orth_ + doc[pt].lemma_  # 文の形を変えているので手動
                    verb = self.verb_chunk(doc[pt].i, *doc)  # 複合語を分割したのでモダリティを取るための例外処理
                    verb["lemma"] = doc[doc[pt].i - 2].orth_
                    verb["lemma_start"] = doc[doc[pt].i - 2].i
                    verb["lemma_end"] = doc[doc[pt].i - 2].i
                    modality_w = verb["modality"]
                    rule_id = 5
                elif (doc[doc[pt].i - 3].pos_ == 'VERB' and doc[doc[pt].i - 3].head.i == doc[doc[pt].i - 3].i):
                    ret_obj = self.num_chunk(doc[pt].i - 3, *doc)  # 内部調査をする -> 内部を　調査する
#                    obj_w = ret_obj['lemma']
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 6
                #
                #             述部が  名詞＋を＋する（調査をする　など）  メイン術部にならない候補
                #
                else:
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 7
            #
            #             述部が  形容詞＋する（少なくする　など）
            #
            elif (doc[doc[pt].i - 1].pos_ == 'AUX'):
                if (doc[pt].i - 4 >= 4 and (doc[doc[pt].i - 1].tag_ == '接尾辞-形容詞的' or doc[doc[pt].i - 1].tag_ == '助動詞') and doc[doc[pt].i - 2].pos_ == 'VERB'):
                    # ○○を使いやすくする -> 使いやすくする
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = doc[doc[pt].i - 2].orth_ + doc[doc[pt].i - 1].orth_ + verb["lemma"]
                    verb["lemma_start"] = doc[doc[pt].i - 2].i
                    modality_w = verb["modality"]
                    rule_id = 8
            elif (doc[doc[pt].i - 1].pos_ == 'ADJ'):
                if (doc[pt].i - 4 >= 4 and doc[doc[pt].i - 1].tag_ == '形容詞-非自立可能' and doc[
                    doc[pt].i - 2].pos_ == 'NOUN'):
                    # ○○を余儀なくする -> 余儀なくする
                    verb = self.verb_chunk(doc[pt].i - 2, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 9
                elif (doc[doc[pt].i - 1].tag_ == '形容詞-一般' or doc[doc[pt].i - 1].tag_ == '形容詞-非自立可能' or (doc[doc[pt].i - 1].tag_ == '副詞' and doc[doc[pt].i - 1].lemma_ == 'よく')):
                    # ○○を少なくする -> 少なくする
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 10
                else:
 #                   obj_w = ''
                    rule_id = 11
            #
            #     「〇〇」する　→　〇〇する
            #
            elif (doc[doc[pt].i - 1].pos_ == 'PUNCT'):
                verb = self.verb_chunk(doc[pt].i - 2, *doc)
                verb_w = verb["lemma"] + doc[pt].lemma_
                verb["lemma_end"] = doc[pt].i
                modality_w = verb["modality"]
                rule_id = 12
            #
            #   どうする、そうする...
            #
            elif (doc[doc[pt].i - 1].pos_ == 'ADV'):
                verb = self.verb_chunk(doc[pt].i - 1, *doc)
                verb_w = verb["lemma"] + doc[pt].lemma_
                verb["lemma_end"] = doc[pt].i
                modality_w = verb["modality"]
                rule_id = 13
            #
            #   〇〇の〇〇を〇〇で（と、から..）する　　　「…をする」の変形版　　→　〇〇の〇〇を〇〇する　と同じ処理　目的語は　更に前の　「〇〇の」　ex.エンジンの開発を東京でする
            #
            elif (doc[doc[pt].i - 1].pos_ == 'ADP' and doc[doc[pt].i - 1].lemma_ != 'を' and doc[doc[pt].i - 1].lemma_ != 'に' and doc[doc[pt].i - 1].lemma_ != 'と'):
                verb_w = ''
                ret_obj = self.num_chunk(doc[pt].i, *doc)
                for k in range(ret_obj["lemma_start"], ret_obj["lemma_end"]):
                    if doc[k].lemma_ == 'の' and doc[k].pos_ == 'ADP':
#                        obj_w = self.compaound(ret_obj["lemma_start"], k - 1, *doc)
                        verb_w = self.compaound(k + 1, ret_obj["lemma_end"], *doc)
                        verb["lemma_start"] = k + 1
                        verb["lemma_end"] = ret_obj["lemma_end"]
                        rule_id = 14
                        break
                if not verb_w:
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 15
            #
            #   〇〇の（名詞）をする　ex.　小学校の教員をする弟
            #
            else:
                verb = self.verb_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = verb["modality"]
#koba                if not subject_w and self.rentai_check(doc[pt].i, *doc) and case == 'を':
                    #                            subject_w = ret_obj = self.num_chunk(doc[pt].head.i, *doc)[0].rstrip('の')
#koba                    subject_w = ret_obj = self.num_chunk(doc[pt].head.i, *doc)['lemma']
                rule_id = 40

        #
        #   普通名詞 + する　のかたちの最終述部
        #
        elif len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' or doc[pt].pos_ == 'VERB') and doc[pt].dep_ == 'ROOT' and doc[doc[pt].i + 1].lemma_ == 'する':
            verb = self.verb_chunk(doc[pt].i, *doc)
#koba            if verb["lemma_start"] <= doc[pt].i:  # 目的語が述部の一部の場合は候補なし
#koba                continue
            verb_w = verb["lemma"] + 'する'
            modality_w = verb["modality"]
            rule_id = 16
        #
        #   〇〇 + を + 〇〇 + に、... 　
        #
        elif len(doc) > doc[pt].i + 2 and doc[pt].pos_ == 'NOUN' and doc[doc[pt].i + 1].lemma_ == 'に' and doc[doc[pt].i + 2].tag_ == '補助記号-読点':
            verb = self.verb_chunk(doc[pt].i, *doc)
            verb_w = verb["lemma"] + doc[doc[pt].i + 1].lemma_ + '(する)'
            verb["lemma_end"] = doc[doc[pt].i + 1].i
            modality_w = verb["modality"]
            rule_id = 17
        #
        #   〇〇 + を + 〇〇 + の... 　
        #
        elif len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' or doc[pt].pos_ == 'PROPN') and doc[doc[pt].i + 1].lemma_ == 'の':
            if (doc[pt].tag_ == '名詞-普通名詞-副詞可能'):  # 〇〇　＋　を　＋　ため　＋　の
                verb = self.verb_chunk(doc[pt].i, *doc)
                verb_w = verb["lemma"]
                modality_w = verb["modality"]
                rule_id = 18
#koba            else:
#koba                continue
        #
        #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
        #
        elif (len(doc) > doc[pt].i + 1 and (doc[pt].pos_ == 'NOUN' and doc[pt].tag_ != '接尾辞-名詞的-副詞可能' and doc[pt].tag_ != '接尾辞-名詞的-助数詞' and doc[pt].tag_ != '名詞-普通名詞-助数詞可能') and doc[pt].tag_ != '名詞-普通名詞-形状詞可能' and doc[doc[pt].i + 1].tag_ == '補助記号-読点'):
            verb = self.verb_chunk(doc[pt].i, *doc)
            verb_w = verb["lemma"] + '(する)'
            modality_w = verb["modality"]
            rule_id = 19
        #
        #   〇〇　＋　を　＋　普通名詞。　　　体言止 連用中止
        #
        elif (doc[pt].pos_ == 'NOUN' and ((doc[pt].dep_ == 'ROOT' and doc[pt].i == doc[pt].head.i) or (len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].pos_ == 'SYM'))):
            verb = self.verb_chunk(doc[pt].i, *doc)
            if (len(doc) > doc[pt].i + 1 and doc[doc[pt].i + 1].lemma_ == 'です'):
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].lemma_
                verb["lemma_end"] = doc[doc[pt].i + 1].i
            elif verb["lemma"].endswith('中'):
                verb_w = verb["lemma"] + '(です)'
            elif doc[doc[pt].i].morph.get("Inflection") and '連用形' in doc[doc[pt].i].morph.get("Inflection")[0]:
                verb_w = verb["lemma"]
            else:
                verb_w = verb["lemma"] + '(する)'
            modality_w = verb["modality"]
            rule_id = 20
        #
        #           ○○する　以外の一般の動詞
        #
        else:
            ###############################
            #    形式動詞
            ###############################
            if (doc[pt].lemma_ == 'なる' and doc[pt - 1].lemma_ != 'に' and doc[pt - 1].lemma_ != 'と'):  # 形式動詞
                if (doc[doc[pt].i - 1].pos_ == 'ADP' or (doc[doc[pt].i - 1].pos_ == 'AUX' and doc[doc[pt].i - 1].orth_ == 'に')):  # 〜となる　〜になる
                    verb = self.verb_chunk(doc[doc[pt].i - 1].i - 1, *doc)
                    verb_w = verb["lemma"] + doc[doc[pt].i - 1].orth_ + doc[pt].lemma_
                    verb["lemma_end"] = doc[pt].i
                    modality_w = verb["modality"]
                    rule_id = 21
                else:
                    verb = self.verb_chunk(doc[pt].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 22
            elif len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].tag_ == '動詞-非自立可能'):  # 動詞　＋　補助動詞
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                if (doc[doc[pt].i].tag_ != '動詞-一般' and
                        (doc[doc[pt].i + 1].lemma_ == 'する' or doc[doc[pt].i + 1].lemma_ == 'できる' or doc[doc[pt].i].tag_ == '名詞-普通名詞-サ変可能' or
                         doc[doc[pt].i].tag_ == '名詞-普通名詞-サ変形状詞可能' or doc[doc[pt].i].tag_ == '名詞-普通名詞-一般')):
                    verb_w = verb["lemma"] + 'する'
                else:
                    verb_w = verb["lemma"]
                modality_w = verb["modality"]
                rule_id = 23
            ###############################
            #    形式名詞
            ###############################
            elif (doc[pt].lemma_ == 'ため'):  # 形式名詞
                if (doc[doc[pt].i - 1].pos_ == 'AUX' and doc[doc[pt].i - 1].lemma_ == 'する'):
                    verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 24
                elif doc[doc[pt].i - 1].pos_ == 'VERB':
                    verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = 25
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...） + する
            ###############################
            elif len(doc) > doc[pt].i + 2 and doc[pt].tag_ == '名詞-普通名詞-一般' and doc[doc[pt].i + 1].pos_ == 'ADP' and doc[doc[pt].i + 2].lemma_ == 'する':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].orth_ + doc[doc[pt].i + 2].lemma_
                verb["lemma_end"] = doc[doc[pt].i + 2].i
                modality_w = verb["modality"]
                rule_id = 26
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇 + 化　＋　する
            ###############################
            elif len(doc) > doc[pt].i + 2 and doc[pt].tag_ == '名詞-普通名詞-一般' and doc[doc[pt].i + 1].head.i != doc[doc[pt].i + 1].i and doc[doc[pt].i + 1].tag_ == '接尾辞-名詞的-サ変可能' and doc[doc[pt].i + 2].lemma_ == 'する':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].i + 1].orth_ + doc[doc[pt].i + 2].lemma_
                verb["lemma_end"] = doc[doc[pt].i + 2].i
                modality_w = verb["modality"]
                rule_id = 27
            ###############################
            #    単独の動詞　普通名詞　〇〇　＋　を　＋　形容動詞
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '形状詞-一般' and doc[doc[pt].i + 1].orth_ == 'に':
                verb = self.verb_chunk(doc[doc[pt].i].i, *doc)
                verb_w = verb["lemma"] + 'にする'
                modality_w = verb["modality"]
                rule_id = 30
            ###############################
            #    単独の動詞　普通名詞　〇〇　＋　を　＋　動詞　＋　形容詞　＋　〇〇　＋　する　ex.　使いやすくバージョンアップする。
            ###############################
            elif (len(doc) > doc[pt].head.i + 1 and doc[doc[pt].i + 1].pos_ == 'AUX' and doc[doc[pt].i + 1].morph.get("Inflection") and '連用形' and doc[pt].head.pos_ == 'NOUN' and doc[doc[pt].head.i + 1].lemma_ == 'する'):
                verb = self.verb_chunk(doc[pt].head.i, *doc)
                verb_w = verb["lemma"] + 'する'
                modality_w = verb["modality"]
                rule_id = 31
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日　＋　から
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-普通名詞-副詞可能' and doc[doc[pt].i + 1].pos_ == 'ADP' and doc[doc[pt].i + 1].lemma_ == 'から':
                verb = self.verb_chunk(doc[doc[pt].head.i].i, *doc)
                verb_w = verb["lemma"] + doc[doc[pt].head.i + 1].orth_
                verb["lemma_end"] = doc[doc[pt].head.i + 1].i
                modality_w = verb["modality"]
                rule_id = 28
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...）
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-普通名詞-一般' and (doc[doc[pt].i + 1].pos_ == 'ADP' or doc[doc[pt].i + 1].pos_ == 'SCONJ'):
                verb_w = ''
            elif len(doc) > doc[pt].i + 2 and doc[pt].tag_ == '名詞-普通名詞-一般' and doc[doc[pt].i + 1].pos_ == 'PUNCT' and doc[doc[pt].i + 2].pos_ == 'ADP':
                verb_w = ''
            ###############################
            #    普通名詞　〇〇　＋　を　＋　接尾
            ###############################
            elif doc[pt].tag_ == '接尾辞-名詞的-副詞可能' or doc[pt].tag_ == '名詞-普通名詞-形状詞可能':
                verb_w = ''
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日
            ###############################
            elif doc[pt].tag_ == '接尾辞-名詞的-助数詞' or doc[pt].tag_ == '名詞-普通名詞-助数詞可能' or doc[pt].tag_ == '名詞-普通名詞-副詞可能':
                verb_w = ''
            ###############################
            #    普通名詞　〇〇　＋　を　＋　〇〇日
            ###############################
            elif len(doc) > doc[pt].i + 1 and doc[pt].tag_ == '名詞-数詞' and doc[doc[pt].i + 1].pos_ == 'PUNCT':
                verb_w = ''
            ###########################################################
            ##   慣用句処理  　（「日の目を見る」など）
            ###########################################################
            ###############################
            #    〜にある
            ###############################
            elif doc[pt].lemma_ == 'ある' and (((doc[doc[pt].i - 1].lemma_ == 'に' or doc[doc[pt].i - 1].lemma_ == 'が') and
                doc[doc[pt].i - 1].tag_ == '助詞-格助詞') or (doc[doc[pt].i - 2].lemma_ == 'に' and doc[doc[pt].i - 1].lemma_ == 'は') or
                (doc[doc[pt].i - 1].lemma_ == 'で' and doc[doc[pt].i - 1].tag_ == '助動詞') or (doc[doc[pt].i - 2].lemma_ == 'で' and doc[doc[pt].i - 1].lemma_ == 'は')):
                if doc[pt].i != doc[pt].i - 2 and doc[pt].i != doc[pt].i - 3:
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
                    rule_id = 41
                else:
                    verb_w = ''
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
                if len(kanyouku) > 0 and doc[pt].i < kanyouku[0]:
                    verb_w = self.kanyouku_get(kanyouku, *doc)
                    verb["lemma_start"] = kanyouku[0]
                    verb["lemma_end"] = kanyouku[-1]
                    rule_id = 50
                else:
                    if len(doc) > doc[pt].i + 1 and (doc[doc[pt].i + 1].tag_ == '接尾辞-名詞的-サ変可能' or (len(doc) > doc[pt].i + 2 and (doc[doc[pt].i + 1].pos_ == 'VERB' and doc[doc[pt].i + 2].lemma_ == 'する'))
                                                         or (doc[doc[pt].i + 1].pos_ == 'VERB' and doc[doc[pt].i + 1].tag_ == '名詞-普通名詞-サ変可能' and doc[doc[pt].i + 1].head.i == doc[doc[pt].i].head.i)):  # 〇〇化する   〇〇いたす
                        verb_w = verb_w + 'する'
                    rule_id = 29
        if verb_w:
            return {'lemma':verb_w, 'lemma_start':verb["lemma_start"], 'lemma_end':verb["lemma_end"], 'modality':modality_w, 'rule_id':rule_id}
        else:
            return {'lemma':'', 'lemma_start':-1, 'lemma_end':-1, 'modality':'', 'rule_id':-1}

