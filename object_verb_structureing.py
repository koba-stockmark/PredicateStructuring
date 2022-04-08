import spacy
from spacy.symbols import obj
from chunker import ChunkExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from verb_split import VerbSpliter
from phase_chek import PhaseCheker

class VerbExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get_from_object
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.sub_verb_chek = v_s.sub_verb_chek
        self.object_devide = v_s.object_devide
        p_c = PhaseCheker()
        self.phase_chek = p_c.phase_chek


    """
    述部のかかり先の取得
    """
    def predic_hea(self, s_pt, e_pt, *doc):
        return ret

    """
    O-Vの取得
    """

    def v_o_get(self, text):

        ret = ''
        modality_w = ''
        dummy_subject = ''
        para_subj = [['',0 ,0 ]]
        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析
        doc_len = len(doc)

        for token in doc:
            obj_w = ''
            subject_w = ''
            rule_id = 0
            verb = {}
            next_head_use = False
            phase = ''
            if ((token.dep_ == "obj" and token.head.dep_ != "obj") or
                    (doc_len > token.i + 1 and token.dep_ == "nsubj" and doc[token.i + 1].lemma_ == "も" and token.tag_ != '名詞-普通名詞-助数詞可能') or
                    (doc_len > token.i + 2 and  doc[token.i + 1].lemma_ == "に" and doc[token.i + 2].lemma_ == "も")):  # トークンが目的語なら　〇〇も　＋　できる　などは主語と目的語の可能性がある
#                if(doc_len > token.i + 1 and doc[token.i + 1].orth_ == 'に'):      #　〇〇には〇〇の などの文は「を」でなくてもobjで解析される場合がある
#                    continue

                if token.lemma_ == ' ':
                    continue
                ret_obj = self.num_chunk(token.i, *doc)
                obj_w = ret_obj[0]
                para_obj = self.para_get(ret_obj[1], ret_obj[2], *doc)

                ret_subj = self.subject_get(token.i, *doc)
                if not token.dep_ == "nsubj" or doc[ret_subj[2] + 1].lemma_ != 'も':   # 〇〇も　の例外処理でsubjを目的語にしている場合は自分自身をsubjにしない（省略されていると考える）
                    subject_w = ret_subj[0]
                if subject_w:
                    dummy_subject = subject_w
                    para_subj = self.para_get(ret_subj[1], ret_subj[2], *doc)

                if(token.dep_ == "nsubj"):
                    if subject_w == obj_w:
                        subject_w = ''
                if (token.head.lemma_ == "する"):
                    #
                    #             述部が  名詞＋（と、に）する（目標とする　など）
                    #
                    if (doc[token.head.i - 1].orth_ == 'に' or doc[token.head.i - 1].orth_ == 'と'):  # 【名詞】に(と)する
                        verb = self.verb_chunk(token.head.i - 2, *doc)
                        verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                        modality_w = verb["modality"]
                        ret_obj = self.num_chunk(token.i, *doc)
                        obj_w = ret_obj[0]
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
                            ret_obj = self.num_chunk(token.head.i - 4, *doc)  # 内部の調査をする -> 内部を　調査する, 緊急使用を承認をする -> 緊急使用を　承認する
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 3
                        elif (doc[token.head.i - 3].pos_ == 'NOUN' and doc[token.head.i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                                (doc[token.head.i - 4].orth_ == 'の' or doc[token.head.i - 4].orth_ == 'を')):
#                            obj_w = self.num_chunk(token.head.i - 5, *doc)[0]
                            ret_obj = self.num_chunk(token.i - 5, *doc)
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 4
                        elif (doc[token.head.i - 3].pos_ == 'NOUN' and doc[token.head.i - 2].tag_ == '名詞-普通名詞-サ変可能' and
                              (doc[token.head.i - 3].tag_ != '名詞-普通名詞-形状詞可能' and doc[token.head.i - 3].tag_ != '接頭辞')):  # 内部調査をする -> 内部を　調査する　でも　緊急調査をする -> 緊急を　調査する　ではない!!　組み合わせで判断する必要あり！
#                            obj_w = self.num_chunk(token.head.i - 3, *doc)[0]
                            ret_obj = self.num_chunk(token.i - 3, *doc)
                            obj_w = ret_obj[0]
                            verb_w = doc[token.head.i - 2].orth_ + token.head.lemma_        # 文の形を変えているので手動
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            modality_w = verb["modality"]
                            rule_id = 5
                        elif (doc[token.head.i - 3].pos_ == 'VERB' and doc[token.head.i - 3].head.i == doc[token.head.i - 3].i):
#                            obj_w = self.num_chunk(token.head.i - 3, *doc)[0]      # 内部調査をする -> 内部を　調査する
                            ret_obj = self.num_chunk(token.i - 3, *doc)      # 内部調査をする -> 内部を　調査する
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 6
                        #
                        #             述部が  名詞＋を＋する（調査をする　など）  メイン術部にならない候補
                        #
                        else:
#                            obj_w = self.num_chunk(token.i, *doc)[0]
                            ret_obj = self.num_chunk(token.i, *doc)
                            obj_w = ret_obj[0]
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
#                            obj_w = self.num_chunk(token.i, *doc)[0]
                            ret_obj = self.num_chunk(token.i, *doc)
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 8
                        else:
                            obj_w = ''
                    elif (doc[token.head.i - 1].pos_ == 'ADJ'):
                        if (token.head.i - 4 >= 4 and doc[token.head.i - 1].tag_ == '形容詞-非自立可能' and doc[token.head.i - 2].pos_ == 'NOUN'):
                            # ○○を余儀なくする -> 余儀なくする
#                            obj_w = self.num_chunk(token.head.i - 4, *doc)[0]
                            ret_obj = self.num_chunk(token.i - 4, *doc)
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i - 2, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 9
                        elif (doc[token.head.i - 1].tag_ == '形容詞-一般' or doc[token.head.i - 1].tag_ == '形容詞-非自立可能' or (doc[token.head.i - 1].tag_ == '副詞' and doc[token.head.i - 1].lemma_ == 'よく')):
                            # ○○を少なくする -> 少なくする
#                            obj_w = self.num_chunk(token.i, *doc)[0]
                            ret_obj = self.num_chunk(token.i, *doc)
                            obj_w = ret_obj[0]
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 10
                        else:
                            obj_w = ''
                            rule_id = 11
                    #
                    #     「〇〇」する　→　〇〇する
                    #
                    elif (doc[token.head.i - 1].pos_ == 'PUNCT'):
                        verb = self.verb_chunk(token.head.i - 2, *doc)
                        verb_w = verb["lemma"] + token.head.lemma_
                        modality_w = verb["modality"]
                        rule_id = 12
                    #
                    #   どうする、そうする...
                    #
                    elif (doc[token.head.i - 1].pos_ == 'ADV'):
                        verb = self.verb_chunk(token.head.i - 1, *doc)
                        verb_w = verb["lemma"] + token.head.lemma_
                        modality_w = verb["modality"]
                        rule_id = 13
                    #
                    #   〇〇の〇〇を〇〇で（と、から..）する　　　「…をする」の変形版　　→　〇〇の〇〇を〇〇する　と同じ処理　目的語は　更に前の　「〇〇の」　ex.エンジンの開発を東京でする
                    #
                    elif (doc[token.head.i - 1].pos_ == 'ADP' and doc[token.head.i - 1].lemma_ != 'を'):
                        if 'の' in obj_w:
                            verb_w = obj_w.split('の')[1]
                            obj_w = obj_w.split('の')[0]
                            rule_id = 14
                        else:
                            verb = self.verb_chunk(token.head.i , *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 15
                #
                #   普通名詞 + する　のかたちの最終述部
                #
                elif doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' or token.head.pos_ == 'VERB') and token.head.dep_ == 'ROOT' and doc[token.head.i + 1].lemma_ == 'する':
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ret_obj = self.num_chunk(token.i, *doc)
                    obj_w = ret_obj[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + 'する'
                    modality_w = verb["modality"]
                    rule_id = 16
                #
                #   〇〇 + を + 〇〇 + に、... 　
                #
                elif doc_len > token.head.i + 2 and token.head.pos_ == 'NOUN' and doc[token.head.i + 1].lemma_ == 'に' and doc[token.head.i + 2].tag_ == '補助記号-読点':
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ret_obj = self.num_chunk(token.i, *doc)
                    obj_w = ret_obj[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_ + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 17
                #
                #   〇〇 + を + 〇〇 + の... 　
                #
                elif doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' or token.head.pos_ == 'PROPN') and doc[token.head.i + 1].lemma_ == 'の':
                    if(token.head.tag_ == '名詞-普通名詞-副詞可能'):     # 〇〇　＋　を　＋　ため　＋　の
                        verb = self.verb_chunk(token.head.i, *doc)
                        verb_w = verb["lemma"]
                        modality_w = verb["modality"]
                        rule_id = 18
                    else:
                        continue
                #
                #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
                #
                elif (doc_len > token.head.i + 1 and (token.head.pos_ == 'NOUN' and token.head.tag_ != '接尾辞-名詞的-副詞可能' and token.head.tag_ != '接尾辞-名詞的-助数詞' and token.head.tag_ != '名詞-普通名詞-助数詞可能') and
                      token.head.tag_ != '名詞-普通名詞-形状詞可能' and doc[token.head.i + 1].tag_ == '補助記号-読点'):
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ret_obj = self.num_chunk(token.i, *doc)
                    obj_w = ret_obj[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    verb_w = verb["lemma"] + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 19
                #
                #   〇〇　＋　を　＋　普通名詞。　　　体言止
                #
                elif (token.head.pos_ == 'NOUN' and ((token.head.dep_ == 'ROOT' and token.head.i == token.head.head.i) or (doc_len > token.head.i + 1 and doc[token.head.i + 1].pos_ == 'SYM'))):
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ret_obj = self.num_chunk(token.i, *doc)
                    obj_w = ret_obj[0]
                    verb = self.verb_chunk(token.head.i, *doc)
                    if (doc_len > token.head.i + 1 and doc[token.head.i + 1].lemma_ == 'です'):
                        verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_
                    elif verb["lemma"].endswith('中'):
                        verb_w = verb["lemma"] + '(です)'
                    else:
                        verb_w = verb["lemma"] + '(する)'
                    modality_w = verb["modality"]
                    rule_id = 20
                #                        obj_w = ''  # デバッグ用
                #
                #           ○○する　以外の一般の動詞
                #
                else:
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ###############################
                    #    形式動詞
                    ###############################
                    if(token.head.lemma_ == 'なる'):                                # 形式動詞
                        if(doc[token.head.i - 1].pos_ == 'ADP' or (doc[token.head.i - 1].pos_ == 'AUX' and doc[token.head.i - 1].orth_ == 'に')):     # 〜となる　〜になる
                            verb = self.verb_chunk(doc[token.head.i - 1].i - 1, *doc)
                            verb_w = verb["lemma"] + doc[token.head.i - 1].orth_ + token.head.lemma_
                            modality_w = verb["modality"]
                            rule_id = 21
                        else:
                            verb = self.verb_chunk(token.head.i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 22
                    elif doc_len > token.head.i + 1 and (doc[token.head.i + 1].tag_ == '動詞-非自立可能'):          # 動詞　＋　補助動詞
                        verb = self.verb_chunk(doc[token.head.i].i, *doc)
                        if (doc[token.head.i].tag_ != '動詞-一般' and
                                (doc[token.head.i + 1].lemma_ == 'する' or doc[token.head.i + 1].lemma_ == 'できる' or doc[token.head.i].tag_ == '名詞-普通名詞-サ変可能' or
                                doc[token.head.i].tag_ == '名詞-普通名詞-サ変形状詞可能' or doc[token.head.i].tag_ == '名詞-普通名詞-一般')):
#                           verb_w = verb["lemma"] + doc[token.head.i + 1].lemma_
                            verb_w = verb["lemma"] + 'する'
                        else:
                            verb_w = verb["lemma"]
                        modality_w = verb["modality"]
                        rule_id = 23
                    ###############################
                    #    形式名詞
                    ###############################
                    elif (token.head.lemma_ == 'ため'):  # 形式名詞
                        if(doc[token.head.i - 1].pos_ == 'AUX' and doc[token.head.i - 1].lemma_ == 'する'):
                            verb = self.verb_chunk(doc[token.head.i].i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 24
                        elif doc[token.head.i - 1].pos_ == 'VERB':
                            verb = self.verb_chunk(doc[token.head.i].i, *doc)
                            verb_w = verb["lemma"]
                            modality_w = verb["modality"]
                            rule_id = 25
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...） + する
                    ###############################
                    elif doc_len > token.head.i + 2 and token.head.tag_ == '名詞-普通名詞-一般' and doc[token.head.i + 1].pos_ == 'ADP' and doc[token.head.i + 2].lemma_ == 'する':
                        verb = self.verb_chunk(doc[token.head.i].i, *doc)
                        verb_w = verb["lemma"] + doc[token.head.i + 1].orth_ + doc[token.head.i + 2].lemma_
                        modality_w = verb["modality"]
                        rule_id = 26
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇 + 化　＋　する
                    ###############################
                    elif doc_len > token.head.i + 2 and token.head.tag_ == '名詞-普通名詞-一般' and doc[token.head.i + 1].head.i != doc[token.head.i + 1].i and doc[token.head.i + 1].tag_ == '接尾辞-名詞的-サ変可能' and doc[token.head.i + 2].lemma_ == 'する':
                        verb = self.verb_chunk(doc[token.head.i].i, *doc)
                        verb_w = verb["lemma"] + doc[token.head.i + 1].orth_ + doc[token.head.i + 2].lemma_
                        modality_w = verb["modality"]
                        rule_id = 27
                    ###############################
                    #    単独の動詞　普通名詞　〇〇　＋　を　＋　形容動詞
                    ###############################
                    elif doc_len > token.head.i + 1 and token.head.tag_ == '形状詞-一般' and doc[token.head.i + 1].orth_ == 'に':
                        verb = self.verb_chunk(doc[token.head.i].i, *doc)
                        verb_w = verb["lemma"] + 'にする'
                        modality_w = verb["modality"]
                        rule_id = 30
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇日　＋　から
                    ###############################
                    elif doc_len > token.head.i + 1 and token.head.tag_ == '名詞-普通名詞-副詞可能' and doc[token.head.i + 1].pos_ == 'ADP' and doc[token.head.i + 1].lemma_ == 'から':
                        next_head_use = True
                        verb = self.verb_chunk(doc[token.head.head.i].i, *doc)
                        verb_w = verb["lemma"] + doc[token.head.head.i + 1].orth_
                        modality_w = verb["modality"]
                        rule_id = 28
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇　に（で、と、から...）
                    ###############################
                    elif doc_len > token.head.i + 1 and token.head.tag_ == '名詞-普通名詞-一般' and (doc[token.head.i + 1].pos_ == 'ADP' or doc[token.head.i + 1].pos_ == 'SCONJ'):
                        obj_w = ''
                        verb_w = ''
                    elif doc_len > token.head.i + 2 and token.head.tag_ == '名詞-普通名詞-一般' and doc[token.head.i + 1].pos_ == 'PUNCT' and doc[token.head.i + 2].pos_ == 'ADP':
                        obj_w = ''
                        verb_w = ''
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　接尾
                    ###############################
                    elif token.head.tag_ == '接尾辞-名詞的-副詞可能' or token.head.tag_ == '名詞-普通名詞-形状詞可能':
                        obj_w = ''
                        verb_w = ''
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇日
                    ###############################
                    elif token.head.tag_ == '接尾辞-名詞的-助数詞' or token.head.tag_ == '名詞-普通名詞-助数詞可能' or token.head.tag_ == '名詞-普通名詞-副詞可能':
                        obj_w = ''
                        verb_w = ''
                    ###############################
                    #    普通名詞　〇〇　＋　を　＋　〇〇日
                    ###############################
                    elif doc_len > token.head.i + 1 and token.head.tag_ == '名詞-数詞' and doc[token.head.i + 1].pos_ == 'PUNCT':
                        obj_w = ''
                        verb_w = ''
                    ###############################
                    #    単独の動詞
                    ###############################
                    else:
                        verb_w = token.head.lemma_
                        verb = self.verb_chunk(token.head.i, *doc)
                        verb_w = verb["lemma"]
                        if doc_len > token.head.i + 1 and (doc[token.head.i + 1].tag_ == '接尾辞-名詞的-サ変可能' or
                            (doc[token.head.i + 1].pos_ == 'VERB' and doc[token.head.i + 2].lemma_ == 'する') or
                            (doc[token.head.i + 1].pos_ == 'VERB' and doc[token.head.i + 1].tag_ == '名詞-普通名詞-サ変可能' and doc[token.head.i + 1].head.i == doc[token.head.i].head.i)): # 〇〇化する   〇〇いたす
                            verb_w = verb_w + 'する'
                        modality_w = verb["modality"]
                        rule_id = 29
#                    obj_w = ''  # デバッグ用

                ###########################################################
                ##   TBD 慣用句処理  　（「日の目を見る」など）　#############
                ###########################################################
                #"""
                # デバッグ用
                if (obj_w ):
                    print(text)
                    modal = ', '.join([str(x) for x in modality_w])
                    if subject_w or not dummy_subject:
                        print('all = 【%s - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, verb_w, subject_w, modal, rule_id))
                        ret = ret + text + '\t\t' + subject_w + '\t' + obj_w + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        if para_subj[0][0]:
                            for para_s in para_subj:
                                print('all = 【%s - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, verb_w, para_s[0], modal, rule_id))
                                ret = ret + text + '\t\t' + para_s[0] + '\t' + obj_w + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        print('all = 【%s - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, verb_w, dummy_subject, modal, rule_id))
                        ret = ret + text + '\t\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        if para_subj[0][0]:
                            for para_s in para_subj:
                                print('all = 【%s - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, verb_w, para_s[0], modal, rule_id))
                                ret = ret + text + '\t\t' + para_s[0] + '(省略)\t' + obj_w + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                #"""
                # デバッグ用

                ##########################################################################################################################################
                #    メイン述部の判断
                #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
                #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
                ##########################################################################################################################################
                main_verb = False
#                """
                # 複合動詞の場合、複合動詞間のかかり受けがあるのでそれを排除して最終かかり先を求める
                predic_head = token.head.i
                comp_verb = self.verb_chunk(doc[token.head.i].i, *doc)
                for i in range(comp_verb['lemma_start'], comp_verb['lemma_end']):
                    if predic_head < doc[i].head.i:
                        predic_head = doc[i].head.i
                #
                # 述部が最終述部の場合
                #
                if (doc[predic_head].i == doc[predic_head].head.i and
                        (doc[predic_head].pos_ == "VERB" or doc[predic_head].pos_ == "ADV") or              # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
                        (doc_len > doc[predic_head].i + 1 and (doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[doc[predic_head].i + 1].lemma_ == 'する'))): # 普通名詞　＋　する が文末の場合
                    rule_id = 100
                    main_verb = True
                    #
                    #           〇〇したと〇〇した　（一時停止したと明らかにした）
                    #           誤解析により補助術部に対して目的語がかかっている場合の処理
                    #
                    if doc_len > doc[token.head.i].i + 3 and (doc[token.i + 2].head.i == doc[predic_head].i and doc[token.i + 2].pos_ == 'VERB' and doc[token.i + 3].lemma_ == "する"):
                        verb_w = doc[token.i + 2].lemma_ + doc[token.i + 3].lemma_
                        rule_id = 101
                #
                # 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
                #
                elif (doc[doc[predic_head].i].pos_ == "VERB" and doc[doc[predic_head].i].head.i == doc[doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB"):  # 最後の動詞を修飾する動詞？
                    #            print(doc[doc[predic_head].i].head.lemma_ , doc[doc[doc[predic_head].i].head.i - 1].lemma_)
                    if (doc[doc[predic_head].i].head.lemma_ == 'する' and doc[doc[doc[predic_head].i].head.i - 1].pos_ != 'ADP'):  # かかり先の動詞が　○○をする　ではなく　単独の動詞か○○する
#                        obj_w = self.num_chunk(token.i, *doc)[0]
                        ret_obj = self.num_chunk(token.i, *doc)
                        obj_w = ret_obj[0]
                        if(doc[doc[predic_head].i + 1].lemma_ == 'する'):
                            verb_w = doc[predic_head].lemma_ + doc[doc[predic_head].i + 1].lemma_
                        else:
                            verb_w = doc[predic_head].lemma_
                        rule_id = 102
                        main_verb = True
                    else:
                        rule_id = 103
                        main_verb = True
                #
                #  最終術部が名詞から形成される場合
                #
                elif (doc[predic_head].head.head.lemma_ == "する" and doc[doc[predic_head].i + 1].lemma_ == '決定'):        # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
                    verb_w = doc[predic_head].lemma_
#                    obj_w = self.num_chunk(token.i, *doc)[0]
                    ret_obj = self.num_chunk(token.i, *doc)
                    obj_w = ret_obj[0]
                    rule_id = 104
                    main_verb = True
                elif doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[predic_head].i == doc[predic_head].head.i:        # 文末が　体言止
                    rule_id = 105
                    main_verb = True
                elif next_head_use and doc[doc[predic_head].head.i + 1].lemma_ == "する":
                    rule_id = 106
                    main_verb = True
                #
                #   目的語がない場合は文脈（前の文）から目的語を持ってくる　　　TBD
                #
                #
                sub_verb = ''
                if self.sub_verb_chek(verb_w):
                    sub_verb = verb_w
                    verb_w = ''


                ##########################################################################################################################################
                #    複合術部のメインと補助への分割
                ##########################################################################################################################################
                if verb:
                    dev_verb = self.verb_devide(verb["lemma_start"], verb["lemma_end"], *doc)
                    if dev_verb[1]:
                        verb_w = dev_verb[0]
                        sub_verb = dev_verb[1]
                        verb["lemma_start"] = dev_verb[2]
                        verb["lemma_end"] = dev_verb[3]

                ##########################################################################################################################################
                #    目的語を述部と分割
                ##########################################################################################################################################

                if ret_obj and not verb_w:
                    dev_obj = self.object_devide(ret_obj[1], ret_obj[2], *doc)
                    if dev_obj[1]:
                        obj_w = dev_obj[0]
                        verb_w = dev_obj[1]
                        verb["lemma_start"] = dev_obj[2]
                        verb["lemma_end"] = dev_obj[3]
                    if not dev_obj[0]:
                        obj_w = ''
                if not verb_w and sub_verb:     # 目的語からの主述部がない場合は補助術部を主述部へもどす
                    verb_w = sub_verb
                    sub_verb = ''

                ##########################################################################################################################################
                #    主述部のフェイズチェック
                ##########################################################################################################################################
                if main_verb:
                    phase = self.phase_chek(verb["lemma_start"], verb["lemma_end"], *doc)


#"""
                # デバッグ用
                if (obj_w and main_verb):
                    print(text)
                    modal = ', '.join([str(x) for x in modality_w])
                    if subject_w or not dummy_subject:
                        print('【%s - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, verb_w, sub_verb, subject_w, phase, modal, rule_id))
                        ret = ret + text + '\tMain\t' + subject_w + '\t' + obj_w + '\t' + verb_w + '\t' + sub_verb + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        if para_subj[0][0]:
                            for para_s in para_subj:
                                print('【%s - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, verb_w, sub_verb, para_s[0], phase, modal, rule_id))
                                ret = ret + text + '\tMain\t' + para_s[0] + '\t' + obj_w + '\t' + verb_w + '\t' + sub_verb + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        print('【%s - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, verb_w, sub_verb, dummy_subject, phase, modal, rule_id))
                        ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + verb_w + '\t' + sub_verb + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        if para_subj[0][0]:
                            for para_s in para_subj:
                                print('【%s - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, verb_w, sub_verb, para_s[0], phase, modal, rule_id))
                                ret = ret + text + '\tMain\t' + para_s[0] + '(省略)\t' + obj_w + '\t' + verb_w + '\t' + sub_verb + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
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
