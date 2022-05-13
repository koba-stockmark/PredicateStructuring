import spacy
from spacy.symbols import obj
from chunker import ChunkExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from verb_split import VerbSpliter
from phase_chek import PhaseCheker
from kanyouku_check import KanyoukuExtractor
from verb_phrase_get import VerbPhraseExtractor

class VerbExtractor:

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
        self.subject_get2 = s_g.subject_get_from_object2
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
        v_x = VerbPhraseExtractor()
        self.verb_phrase_get = v_x.verb_phrase_get


    """
    述部の探索
    """
    def predicate_search(self, *doc):
        for token in doc:
            if(token.pos_ == 'VERB'):
                self.verb_phrase_get(token.i, *doc)
        return ret

    """
    O-Vの取得
    """

    def v_o_get2(self, text):

        ret = ''
        modality_w = ''
        dummy_subject = ''
        dummy_subj = {}
        para_subj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析
        doc_len = len(doc)
        verb_end = -1

        for token in doc:
            subject_w = ''
            sub_verb_w = ''
            sub_verb = {}
            next_head_use = False
            #
            #  述部の検索
            #
            if token. i <= verb_end:
                continue
            if (token.pos_ == 'VERB' or token.pos_ == 'ADJ' or token.dep_ == 'ROOT' or token.dep_ == 'ROOT' or token.dep_ == 'obl' or token.dep_ == 'acl' or token.dep_ == 'advcl' or token.tag_ == '名詞-普通名詞-副詞可能' or
                    (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX') or
                    (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能') or
                    (len(doc) > token.i + 1 and token.tag_ == '名詞-普通名詞-サ変可能' and token.dep_ == 'nmod' and (doc[token.i + 1].lemma_ == '、' or doc[token.i + 1].lemma_ == '：'))):
                if token.pos_ == 'VERB' or token.pos_ == 'ADJ' or (token.dep_ == 'nmod' and token.i > 0 and doc[token.i - 1].pos_ == 'ADP') or (token.dep_ == 'ROOT' and token.tag_ == '名詞-普通名詞-サ変可能'):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif token.dep_ == 'obl' and (doc[token.i - 1].lemma_ == 'を' and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'に'):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif token.tag_ == '名詞-普通名詞-副詞可能' and (token.lemma_ == 'ため') and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'の':    # 〜ための
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif token.dep_ == 'acl' and token.lemma_ == 'する':  # 〜を〇〇する〇〇
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif token.dep_ == 'obl' and len(doc) > token.i + 1 and doc[token.i + 1].lemma_ == 'と':  # 〇〇とする
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].pos_ == 'AUX':
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif token.tag_ == '名詞-普通名詞-サ変可能' and (len(doc) <= token.i + 1 or doc[token.i + 1].pos_ != 'ADP') and (not doc[token.i - 1].morph.get("Inflection") or '連体形' not in doc[token.i - 1].morph.get("Inflection")[0]):
#                    verb = self.num_chunk(token.i, *doc)
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
#                    modality_w = ''
#                    rule_id = 50
                ###################
                #
                #   普通名詞 + する　のかたちの最終述部
                #
                elif len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'VERB') and token.dep_ == 'ROOT' and doc[token.i + 1].lemma_ == 'する':
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]                #
                #   〇〇 + を + 〇〇 + に、... 　
                #
                elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and len(doc) > token.i + 2 and token.pos_ == 'NOUN' and doc[token.i + 1].lemma_ == 'に' and doc[token.i + 2].tag_ == '補助記号-読点':
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]                #
                #   〇〇 + を + 〇〇 + の... 　
                #
                elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and len(doc) > token.i + 1 and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and doc[token.i + 1].lemma_ == 'の':
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]                #
                #   〇〇　＋　を　＋　〇〇(名詞) + 、+ ... 　
                #
                elif token.i > 0 and doc[token.i - 1].pos_ == 'ADP' and (len(doc) > token.i + 1 and (token.pos_ == 'NOUN' and token.tag_ != '接尾辞-名詞的-副詞可能' and token.tag_ != '接尾辞-名詞的-助数詞' and token.tag_ != '名詞-普通名詞-助数詞可能') and token.tag_ != '名詞-普通名詞-形状詞可能' and doc[token.i + 1].tag_ == '補助記号-読点'):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]               #
                #   〇〇　＋　を　＋　普通名詞。　　　体言止 連用中止
                #
                elif token.i > 0 and (doc[token.i - 1].pos_ == 'ADP' or doc[token.i - 1].pos_ == 'SCONJ') and (token.pos_ == 'NOUN' and ((token.dep_ == 'ROOT' and token.i == token.head.i) or (len(doc) > token.i + 1 and doc[token.i + 1].pos_ == 'SYM'))):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif (len(doc) > token.i + 1 and token.tag_ == '形状詞-一般' and doc[token.i + 1].tag_ == '助動詞'):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                elif (len(doc) > token.i + 1 and token.pos_ == 'NOUN' and doc[token.i + 1].tag_ == '動詞-非自立可能'):
                    verb = self.verb_phrase_get(token.i, *doc)
                    verb_w = verb["lemma"]
                    modality_w = verb["modality"]
                    rule_id = verb["rule_id"]
                else:
                    continue

            else:
                continue
            verb_rule_id = rule_id
            verb_end = verb["lemma_end"]
            #
            #  主語の検索
            #
            ret_subj = self.subject_get2(token.i, token.i, *doc)
            if not token.dep_ == "nsubj" or doc[ret_subj['lemma_end'] + 1].lemma_ != 'も':  # 〇〇も　の例外処理でsubjを目的語にしている場合は自分自身をsubjにしない（省略されていると考える）
                subject_w = ret_subj['lemma']

            #
            #  つながる項の検索
            #
            for i in range(0, verb["lemma_start"]):
                rule_id = verb_rule_id
                phase = ''
                if ret_subj["lemma"] and i >= ret_subj["lemma_start"] and i <= ret_subj["lemma_end"]:   # 主語は対象外
                    continue
                """
                if (doc[i].dep_ == "nsubj" or doc[i].dep_ == "dep" or doc[i].dep_ == "advcl" or doc[i].dep_ == "advmod" or doc[i].pos_ == "PUNCT" or doc[i].tag_ == '接頭辞'):
                    continue
                if doc[i].pos_ == 'VERB' or doc[i].dep_ == 'ROOT':
                    continue
                renyou_f = False
                if (doc[i].head.head.i != token.i and doc[i].head.pos_ == 'VERB' and (doc[i].head.morph.get("Inflection") and '連用形' in doc[i].head.morph.get("Inflection")[0])):  # 連用形の連続は前の格情報も継承する
                    renyou_f = True
                renyou_f = False
                if (doc[i].head.i == token.i or renyou_f) and doc[i].pos_ != 'CCONJ':
                    continue
                """
                if (doc[i].dep_ == "obj" and doc[i].head.dep_ != "obj") or ((doc[i].dep_ == "obl" and doc[i].head.dep_ != "obl") and doc[i].tag_ != '名詞-普通名詞-副詞可能'):
                    if doc[i].head.i < verb["lemma_start"] or doc[i].head.i > verb["lemma_end"]:    # 述部に直接かからない
#                        continue
                        #####  要検討　条件をもっと追加しないと余計なものができる
                        if doc[i].head.head.i == token.i or (doc[i].head.morph.get("Inflection") and '連用形' not in doc[i].head.morph.get("Inflection")[0]):  # 連用形接続でもつながらない
                            if (doc[doc[i].head.i + 1].tag_ != '接尾辞-形容詞的' and (doc[doc[i].head.i].tag_ != '名詞-普通名詞-副詞可能' or doc[doc[i].head.i].lemma_ == 'ため' or doc[doc[i].head.i].lemma_ == '前')) or doc[i].head.head.pos_ == 'NOUN':
                                continue
                        elif doc[i].head.pos_ == 'VERB' and doc[i].head.head.i == verb["lemma_start"] and rule_id == 31:    # rule_id 31 の特別処理　「ツールをより使いやすく、バージョンアップ」
                            pass
                        else:
                            continue
                        ####
                    case = self.case_get(i, *doc)
                    if not case and doc[i].tag_ == '名詞-普通名詞-サ変可能':
                        continue
#                    if(renyou_f and case == 'を'):
#                        continue
                    ret_obj = self.num_chunk(i, *doc)
                    obj_w = ret_obj['lemma']
#                    para_obj = self.para_get(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)

                    # 主語の並列化
                    """
                    if subject_w and case != 'と':
                        dummy_subject = subject_w
                        dummy_subj["lemma"] = ret_subj["lemma"]
                        dummy_subj["lemma_start"] = ret_subj["lemma_start"]
                        dummy_subj["lemma_end"] = ret_subj["lemma_end"]
                        para_subj = self.para_get(ret_subj['lemma_start'], ret_subj['lemma_end'], *doc)
                        """

                    if (obj_w):
                        print(text)
                        if dummy_subj and ret_obj["lemma_start"] <= dummy_subj["lemma_start"] and ret_obj["lemma_end"] >= dummy_subj["lemma_end"]:
                            dummy_subject = ''
                        modal = ', '.join([str(x) for x in modality_w])
                        if subject_w or not dummy_subject:
                            print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, subject_w, modal, rule_id))
                            ret = ret + text + '\t\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                            if para_subj and para_subj[0]['lemma']:
                                for para_s in para_subj:
                                    print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, para_s['lemma'], modal, rule_id))
                                    ret = ret + text + '\t\t' + para_s['lemma'] + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        else:
                            print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, dummy_subject, modal, rule_id))
                            ret = ret + text + '\t\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                            if para_subj and para_subj[0]['lemma']:
                                for para_s in para_subj:
                                    print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, para_s['lemma'], modal, rule_id))
                                    ret = ret + text + '\t\t' + para_s['lemma'] + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    # """
                    # デバッグ用

                    ##########################################################################################################################################
                    #    メイン述部の判断
                    #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
                    #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
                    ##########################################################################################################################################
                    main_verb = False
                    #                """
                    # 複合動詞の場合、複合動詞間のかかり受けがあるのでそれを排除して最終かかり先を求める
                    predic_head = token.i
                    if token.pos_ == 'VERB':
                        comp_verb = self.verb_chunk(doc[token.i].i, *doc)
                        for i in range(comp_verb['lemma_start'], comp_verb['lemma_end']):
                            if predic_head < doc[i].head.i:
                                predic_head = doc[i].head.i
                    #
                    # 述部が最終述部の場合
                    #
                    if (doc[predic_head].i == doc[predic_head].head.i and(doc[predic_head].pos_ == "VERB" or doc[predic_head].pos_ == "ADV") or  # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
                            (doc_len > doc[predic_head].i + 1 and (doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[doc[predic_head].i + 1].lemma_ == 'する'))):  # 普通名詞　＋　する が文末の場合
                        rule_id = 100
                        main_verb = True
                        #
                        #           〇〇したと〇〇した　（一時停止したと明らかにした）
                        #           誤解析により補助術部に対して目的語がかかっている場合の処理
                        #
                        if doc_len > i + 3 and (doc[i + 2].head.i == doc[predic_head].i and doc[i + 2].pos_ == 'VERB' and doc[i + 3].lemma_ == "する"):
                            verb_w = doc[i + 2].lemma_ + doc[i + 3].lemma_
                            rule_id = 101
                    #
                    # 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
                    #
                    elif (doc[doc[predic_head].i].pos_ == "VERB" and doc[doc[predic_head].i].head.i == doc[doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB"):  # 最後の動詞を修飾する動詞？
                        #            print(doc[doc[predic_head].i].head.lemma_ , doc[doc[doc[predic_head].i].head.i - 1].lemma_)
                        if (doc[doc[predic_head].i].head.lemma_ == 'する' and doc[doc[doc[predic_head].i].head.i - 1].pos_ != 'ADP' and verb["lemma_end"] != predic_head):  # かかり先の動詞が　○○をする　ではなく　単独の動詞か○○する
                            if (doc[doc[predic_head].i + 1].lemma_ == 'する'):
                                verb_w = doc[predic_head].lemma_ + doc[doc[predic_head].i + 1].lemma_
                            else:
                                verb_w = doc[predic_head].lemma_
                            verb["lemma"] = verb_w
                            verb["lemma_start"] = predic_head
                            verb["lemma_end"] = predic_head
                            rule_id = 102
                            main_verb = True
                        else:
                            rule_id = 103
                            main_verb = True
                    #
                    #  最終術部が名詞から形成される場合
                    #
                    elif (doc[predic_head].head.head.lemma_ == "する" and doc[
                        doc[predic_head].i + 1].lemma_ == '決定'):  # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
                        verb_w = doc[predic_head].lemma_
                        rule_id = 104
                        main_verb = True
                    elif doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[predic_head].i == \
                            doc[predic_head].head.i:  # 文末が　体言止
                        rule_id = 105
                        main_verb = True
                    elif doc[predic_head].head.pos_ == 'NOUN' and doc[predic_head].head.dep_ == 'ROOT' and doc[
                        predic_head].head.i == doc[doc[predic_head].head.i].head.i:  # 文末が　体言止
                        rule_id = 107
                        main_verb = True
                    elif next_head_use and doc[doc[predic_head].head.i + 1].lemma_ == "する":
                        rule_id = 106
                        main_verb = True

                    ##########################################################################################################################################
                    #   述部加工処理用に現在の述部を記憶する
                    ##########################################################################################################################################
                    memo_verb ={}
                    memo_verb_w = verb_w
                    memo_verb["lemma"] = verb["lemma"]
                    memo_verb["lemma_start"] = verb["lemma_start"]
                    memo_verb["lemma_end"] = verb["lemma_end"]

                    ##########################################################################################################################################
                    #   主述部と補助術部の判断
                    ##########################################################################################################################################
#                    sub_verb_w = ''
#                    sub_verb = {}
                    sub_verb_is_original = True
                    if self.sub_verb_chek(verb_w) and verb:
                        sub_verb_is_original = False
                        sub_verb_w = verb_w
                        sub_verb["lemma"] = verb["lemma"]
                        sub_verb["lemma_start"] = verb["lemma_start"]
                        sub_verb["lemma_end"] = verb["lemma_end"]
                        verb_w = ''
                        verb["lemma"] = ''
                        verb["lemma_start"] = -1
                        verb["lemma_end"] = -1

                    ##########################################################################################################################################
                    #    目的語を述部と分割
                    ##########################################################################################################################################

                    if ret_obj and not verb_w:
                        dev_obj = self.object_devide(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                        if dev_obj["verb"]:
                            obj_w = dev_obj["object"]
                            verb_w = dev_obj["verb"]
                            verb["lemma"] = verb_w
                            verb["lemma_start"] = dev_obj["verb_start"]
                            verb["lemma_end"] = dev_obj["verb_end"]
                        if not dev_obj["object"]:
                            obj_w = ''

                    ##########################################################################################################################################
                    #    複合術部のメインと補助への分割
                    ##########################################################################################################################################
                    """
                    dev_verb = {}
                    if verb and verb['lemma']:
                        dev_verb = self.verb_devide(verb["lemma_start"], verb["lemma_end"], *doc)
                    elif sub_verb and sub_verb['lemma']:
                        dev_verb = self.verb_devide(sub_verb["lemma_start"], sub_verb["lemma_end"], *doc)
                    if dev_verb and dev_verb["sub_verb"]:  # 補助述部がある
                        verb_w = dev_verb["verb"]
                        verb["lemma"] = verb_w
                        verb["lemma_start"] = dev_verb["verb_start"]
                        verb["lemma_end"] = dev_verb["verb_end"]
                        if verb_w and sub_verb_w and sub_verb_is_original:  # 主述部と補助術部の療法がる場合は取得した補助術部はもとの補助術部に追加する
                            sub_verb_w = dev_verb["sub_verb"] + sub_verb_w
                            sub_verb["lemma"] = sub_verb_w
                            sub_verb["lemma_start"] = dev_verb["sub_verb_start"]
                        else:
                            sub_verb_w = dev_verb["sub_verb"]
                            sub_verb["lemma"] = sub_verb_w
                            sub_verb["lemma_start"] = dev_verb["sub_verb_start"]
                            sub_verb["lemma_end"] = dev_verb["sub_verb_end"]
                    """

                    ##########################################################################################################################################
                    #    目的語からの主述部がない場合は補助術部を主述部へもどす
                    ##########################################################################################################################################
                    if not verb_w and sub_verb_w:  # 目的語からの主述部がない場合は補助術部を主述部へもどす
                        verb_w = sub_verb_w
                        sub_verb_w = ''
                        verb["lemma_start"] = sub_verb["lemma_start"]
                        verb["lemma_end"] = sub_verb['lemma_end']

                    ##########################################################################################################################################
                    #    主述部のフェイズチェック
                    ##########################################################################################################################################
                    if main_verb and verb:
                        phase = self.phase_chek(verb["lemma_start"], verb["lemma_end"], ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                        if sub_verb:
                            add_phase = self.phase_chek(sub_verb["lemma_start"], sub_verb["lemma_end"],
                                                        ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                            for append in add_phase.split(','):  # 重複は登録しない
                                if append != '<その他>' and append != '<告知>' and append not in phase:
                                    phase = phase + ',' + append

                    """
                    # デバッグ用
                    if (obj_w and main_verb):
                        print(text)
                        modal = ', '.join([str(x) for x in modality_w])
                        if subject_w or not dummy_subject:
                            print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, subject_w, phase, modal, rule_id))
                            ret = ret + text + '\tMain\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                            if para_subj and para_subj[0]['lemma']:
                                for para_s in para_subj:
                                    print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, para_s['lemma'], phase, modal, rule_id))
                                    ret = ret + text + '\tMain\t' + para_s['lemma'] + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        else:
                            print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, dummy_subject, phase, modal, rule_id))
                            ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                            if para_subj and para_subj[0]['lemma']:
                                for para_s in para_subj:
                                    print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, para_s['lemma'], phase, modal, rule_id))
                                    ret = ret + text + '\tMain\t' + para_s['lemma'] + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    # デバッグ用
                     """
                    ##########################################################################################################################################
                    #   述部加工処理用に現在の述部を記憶する
                    ##########################################################################################################################################
                    verb_w = memo_verb_w
                    verb["lemma"] = memo_verb["lemma"]
                    verb["lemma_start"] = memo_verb["lemma_start"]
                    verb["lemma_end"] = memo_verb["lemma_end"]

        return ret

    def text_treace(self, text):
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
