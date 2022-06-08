import copy
from chunker import ChunkExtractor
from case_information_get import CaseExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from predicate_split import VerbSpliter
from phase_check import PhaseCheker
from kanyouku_check import KanyoukuExtractor
from predicate_phrase_analysis import PredicatePhraseExtractor
from main_verb_check import MainVerbChek
from predicate_get import PredicateGet
from data_dump import DataDumpSave

class PasAnalysis:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.compaound = chunker.compaound
        c_get = CaseExtractor()
        self.case_get = c_get.case_get
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get
        self.rentai_check = s_g.rentai_check
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.sub_verb_chek = v_s.sub_verb_chek
        self.object_devide = v_s.object_devide
        p_c = PhaseCheker()
        self.phase_chek = p_c.phase_chek
        self.single_phase_get = p_c.single_phase_get
        k = KanyoukuExtractor()
        self.kanyouku_chek = k.kanyouku_chek
        self.kanyouku_get = k.kanyouku_get
        v_x = PredicatePhraseExtractor()
        self.predicate_phrase_get = v_x.predicate_phrase_get
        m_v_c = MainVerbChek()
        self.main_verb_chek = m_v_c.main_verb_chek
        p_g = PredicateGet()
        self.predicate_get = p_g.predicate_get
        d_d_s = DataDumpSave()
        self.data_dump_and_save = d_d_s.data_dump_and_save
        self.data_dump_and_save2 = d_d_s.data_dump_and_save2

    """
    主述部と補助術部に別れた述語項構造の取得
    """

    def pas_analysis(self, debug, text, *doc):

        argument = []
        all_predict = []
        append_predict = []
        ret = {}
        verb_end = -1
        predicate_id = -1
        pre_predicate_id = -1
        d_ret = ''
        new_verb = False

        for token in doc:
            predicate = {}
            subject_w = ''
            dummy_subj = {}
            sub_verb_w = ''
            sub_verb = {}
            para_subj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
            pre_rentai_subj = False
            #
            #  述部の検索
            #
            if token.i <= verb_end:
                continue
            verb = self.predicate_get(token.i, *doc)
            if not verb:
                continue
            verb_w = verb["lemma"]
            verb_end = verb["lemma_end"]
            modality_w = verb["modality"]
            rule_id = verb["rule_id"]
            verb_rule_id = rule_id
            if len(doc) > verb_end + 1 and doc[verb_end + 1].norm_ == '為る': # 体言どめ用の補正
                verb_end = verb_end + 1
            if not verb_w:
                continue
            #
            #  補助用言を含む述部の範囲を判別
            #
            predicate_start = verb["lemma_start"]
            predicate_end = verb["lemma_end"]
            for check in doc[verb["lemma_end"] + 1:]:
#                if check.head.i <= verb["lemma_end"] or check.dep_ == 'ROOT':
                if check.head.i <= verb["lemma_end"]:
                    predicate_end = predicate_end + 1
                else:
                    break
            #
            #  主語の検索
            #
            ret_subj = self.subject_get(token.i, verb["lemma_end"], *doc)
            if not token.dep_ == "nsubj" or doc[ret_subj['lemma_end'] + 1].lemma_ != 'も':  # 〇〇も　の例外処理でsubjを目的語にしている場合は自分自身をsubjにしない（省略されていると考える）
                subject_w = ret_subj['lemma']

            if ((ret_subj["lemma_start"] <= verb["lemma_start"] and ret_subj["lemma_end"] >= verb["lemma_end"]) or
                (ret_subj["lemma_start"] <= verb["lemma_start"] and ret_subj["lemma_start"] >= verb["lemma_end"]) or
                (ret_subj["lemma_end"] <= verb["lemma_start"] and ret_subj["lemma_end"] >= verb["lemma_end"])):
                continue

            # 主語の表層格の取得
            subj_case = self.case_get(ret_subj['lemma_end'], *doc)

            # 省略主語のセット
            if subject_w:
                if (self.rentai_check(verb["lemma_end"], *doc) or (doc[verb["lemma_end"]].morph.get("Inflection") and '連体形' in doc[verb["lemma_end"]].morph.get("Inflection")[0])) and verb["lemma_start"] < ret_subj["lemma_start"]:
                    pre_rentai_subj = True
                else:
                    pre_rentai_subj = False
                    dummy_subj["lemma"] = ret_subj["lemma"]
                    dummy_subj["lemma_start"] = ret_subj["lemma_start"]
                    dummy_subj["lemma_end"] = ret_subj["lemma_end"]
                    dummy_subj["case"] = subj_case
            elif pre_rentai_subj:   # 前に出てきた主語が連体形から生成されている場合は省略の保存をクリア
                dummy_subj.clear()

            # 主語の並列化
            if subject_w:
                para_subj = self.para_get(ret_subj['lemma_start'], ret_subj['lemma_end'], *doc)
            #
            #  つながる項の検索
            #
            find_f = False
            argument_map = []
            for i in range(0, verb["lemma_start"]):
                if doc[i].dep_ != "nsubj" and ret_subj["lemma"] and i >= ret_subj["lemma_start"] and i <= ret_subj["lemma_end"]:  # 主語は対象外
                    continue
                if ((doc[i].dep_ == "obj" and doc[i].head.dep_ != "obj") or
                        (doc[i].dep_ == "obl" and
                         (doc[i].norm_ != 'そこ' and doc[i].norm_ != 'それ') and
                         (doc[i].tag_ != '名詞-普通名詞-副詞可能' or doc[i].norm_ == '為' or doc[i].norm_ == '下') and (doc[i].norm_ != '度' or doc[i - 1].pos_ == 'NUM'))):  # この度　はNG
#                    if doc[i].head.i < verb["lemma_start"] or doc[i].head.i > verb["lemma_end"]:  # 述部に直接かからない
                    if doc[i].head.i < predicate_start or doc[i].head.i > predicate_end:  # 述部に直接かからない
                        #                        continue
                        #####  要検討　条件をもっと追加しないと余計なものができる
                        if doc[i].head.head.i == token.i or (doc[i].head.morph.get("Inflection") and '連用形' not in doc[i].head.morph.get("Inflection")[0]):  # 連用形接続でもつながらない
                            if (doc[doc[i].head.i + 1].tag_ != '接尾辞-形容詞的' and (doc[doc[i].head.i].tag_ != '名詞-普通名詞-副詞可能' or doc[doc[i].head.i].lemma_ == 'ため' or doc[doc[i].head.i].lemma_ == '前')) or doc[i].head.head.pos_ == 'NOUN':
                                continue
                        elif doc[i].head.pos_ == 'VERB' and doc[i].head.head.i == verb["lemma_start"]:  # 特別処理　「ツールをより使いやすく、バージョンアップ」
                            if len(doc) > doc[i].head.i + 1 and doc[doc[i].head.i + 1].pos_ == 'AUX' and doc[i].head.head.pos_ == 'NOUN' and len(doc) > doc[i].head.head.i + 1 and doc[doc[i].head.head.i + 1].lemma_ == 'する':
                                pass
                            else:
                                continue
                        else:
                            continue
                        ####
                    find_f = True
                    argument_map += [i]

            #######################################
            #  PASの作成
            #######################################
            #
            #  主語のセット
            #
            predicate_id = predicate_id + 1
            if subject_w:
                ret_subj["case"] = subj_case
                ret_subj["dummy"] = False
                ret_subj["subject"] = True
                ret_subj["predicate_id"] = predicate_id
                argument.append(ret_subj)
                if para_subj and para_subj[0]['lemma']:
                    for p_subj in para_subj:
                        p_subj["case"] = subj_case
                        p_subj["dummy"] = False
                        p_subj["subject"] = True
                        p_subj["predicate_id"] = predicate_id
                        argument.append(p_subj)
            elif dummy_subj:
                dummy_subj["dummy"] = True
                dummy_subj["subject"] = True
                dummy_subj["predicate_id"] = predicate_id
                argument.append(dummy_subj)
            # 項のセット
            argument_id = 0
            for i in range(0, verb["lemma_start"]):
                ret_obj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
                rule_id = verb_rule_id
                para_obj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
                #
#                if(find_f and i in argument_map) or (not find_f and  doc[i].dep_ == "nsubj" and i >= ret_subj['lemma_start'] and i <= ret_subj['lemma_end']):
                if(find_f and i in argument_map):
#                    if(renyou_f and case == 'を'):doc[i].dep_ == "nsubj"
#                        continue
                    #
                    # 項の取得
                    #
                    if find_f:
                        ret_obj = self.num_chunk(i, *doc)
                        #
                        # 項の並列処理
                        #
                        para_obj = self.para_get(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                    elif verb["lemma"] == 'ため':     # ためだけの述部はNGとする
                        continue
                    #
                    # 格情報の取得
                    #
                    if ret_obj:
                        case = self.case_get(ret_obj['lemma_end'], *doc)
                    else:
                        case = self.case_get(i, *doc)
                    if not case and doc[i].tag_ == '名詞-普通名詞-サ変可能':
                        continue
                    #
                    # 項のセット
                    #
                    ret_obj["case"] = case
                    ret_obj["subject"] = False
                    ret_obj["id"] = argument_id
                    ret_obj["predicate_id"] = predicate_id
                    argument_id = argument_id + 1
                    argument.append(ret_obj)
                    if para_obj and para_obj[0]["lemma"]:
                        for p_obj in para_obj:
                            p_obj["case"] = case
                            p_obj["subject"] = False
                            p_obj["id"] = argument_id
                            p_obj["predicate_id"] = predicate_id
                            argument_id = argument_id + 1
                            argument.append(p_obj)
                    #
                    # 省略主語が項とかぶった場合は諸略主語を削除
                    #
                    if dummy_subj and ret_obj["lemma_start"] <= dummy_subj["lemma_start"] and ret_obj["lemma_end"] >= dummy_subj["lemma_end"]:
                        for subj in argument:
                            if subj["subject"] and subj["dummy"]:
                                argument.remove(subj)
                                break

            # データダンプ
            if find_f and debug:
                d_ret = d_ret + self.data_dump_and_save(text, argument, verb, predicate_id)
            ##########################################################################################
            #  メイン術部の分割処理   すべての項に対してチェックして最終的な述部を判断する
            ##########################################################################################
            verb_from_object = False
            for re_arg in argument:
                if predicate_id != re_arg["predicate_id"]:
                    continue
                ##########################################################################################################################################
                #   述部加工処理用に現在の述部を記憶する
                ##########################################################################################################################################
                memo_verb ={}
                memo_verb["lemma"] = verb["lemma"]
                memo_verb["lemma_start"] = verb["lemma_start"]
                memo_verb["lemma_end"] = verb["lemma_end"]

                ##########################################################################################################################################
                #   主述部と補助術部の判断
                ##########################################################################################################################################
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

                if verb_from_object or (re_arg and not verb_w):
                    dev_obj = self.object_devide(re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                    if dev_obj["verb"]:
                        re_arg["lemma"] = dev_obj["object"]
                        re_arg["lemma_end"] = dev_obj["verb_start"] - 1
                        verb_w = dev_obj["verb"]
                        verb["lemma"] = verb_w
                        verb["lemma_start"] = dev_obj["verb_start"]
                        verb["lemma_end"] = dev_obj["verb_end"]
                        verb_from_object = True
                        new_verb = True
                    if not dev_obj["object"]:
                        re_arg["lemma"] = ''
                        re_arg["lemma_start"] = -1
                        re_arg["lemma_end"] = -1

                ##########################################################################################################################################
                #    複合術部のメインと補助への分割
                ##########################################################################################################################################
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
                    new_verb = True

                ##########################################################################################################################################
                #    目的語からの主述部がない場合は補助術部を主述部へもどす
                ##########################################################################################################################################
                if not verb_w and sub_verb_w:  # 目的語からの主述部がない場合は補助術部を主述部へもどす
                    verb_w = sub_verb_w
                    sub_verb_w = ''
                    verb["lemma"] = sub_verb["lemma"]
                    verb["lemma_start"] = sub_verb["lemma_start"]
                    verb["lemma_end"] = sub_verb['lemma_end']
                    new_verb = False
                ##########################################################################################################################################
                #    述部が変更された場合は新しいものを保存
                ##########################################################################################################################################
#                if new_verb or predicate_id != pre_predicate_id:
                if new_verb:
                    same_word = False
                    for check in append_predict:
                       if verb["lemma"] == check["lemma"] and verb["lemma_start"] == check["lemma_start"]:
                           same_word = True
                           break
                    if same_word:
                        continue
                    predicate["id"] = predicate_id
                    predicate["lemma"] = verb["lemma"]
                    predicate["lemma_start"] = verb["lemma_start"]
                    predicate["lemma_end"] = verb["lemma_end"]
                    predicate["orth"] = verb_w
                    predicate["modality"] = ', '.join([str(x) for x in modality_w])
                    predicate["rule_id"] = rule_id
                    if sub_verb and sub_verb_w:
                        predicate["sub_lemma"] = sub_verb["lemma"]
                        predicate["sub_lemma_start"] = sub_verb["lemma_start"]
                        predicate["sub_lemma_end"] = sub_verb["lemma_end"]
                        predicate["sub_orth"] = sub_verb_w
                    else:
                        predicate["sub_lemma"] = ''
                        predicate["sub_lemma_start"] = ''
                        predicate["sub_lemma_end"] = ''
                        predicate["sub_orth"] = ''
                    pre_predicate_id = predicate_id
                    append_predict.append(copy.deepcopy(predicate))

            ##########################################################################################################################################
            #    最終的な述部の整理
            ##########################################################################################################################################
#            if not new_verb:
            if pre_predicate_id != predicate_id:
                predicate["id"] = predicate_id
                predicate["lemma"] = verb["lemma"]
                predicate["lemma_start"] = verb["lemma_start"]
                predicate["lemma_end"] = verb["lemma_end"]
                predicate["orth"] = verb_w
                predicate["modality"] = ', '.join([str(x) for x in modality_w])
                predicate["rule_id"] = rule_id
                if sub_verb and sub_verb_w:
                    predicate["sub_lemma"] = sub_verb["lemma"]
                    predicate["sub_lemma_start"] = sub_verb["lemma_start"]
                    predicate["sub_lemma_end"] = sub_verb["lemma_end"]
                    predicate["sub_orth"] = sub_verb_w
                else:
                    predicate["sub_lemma"] = ''
                    predicate["sub_lemma_start"] = ''
                    predicate["sub_lemma_end"] = ''
                    predicate["sub_orth"] = ''
                pre_predicate_id = predicate_id
                append_predict.append(copy.deepcopy(predicate))
        ##########################################################################################################################################
        #    メイン述部の判断
        #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
        #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
        ##########################################################################################################################################
        for predic in append_predict:
            predic["main"] = False
            if predic["sub_lemma_start"]:
                v_rule_id = self.main_verb_chek(predic["sub_lemma_end"], *doc)
                if v_rule_id < 0:   # 補助術部が２段で分割されている場合も考慮
                    v_rule_id = self.main_verb_chek(doc[predic["sub_lemma_end"]].head.i, *doc)
            else:
                v_rule_id = self.main_verb_chek(predic["lemma_end"], *doc)
            if v_rule_id > 0:
                predic["main_rule_id"] = v_rule_id
                predic["main"] = True
#        if new_verb:
        for arg in argument:
            if not arg["lemma"] and not arg["subject"]:
                argument.remove(arg)

        ret["argument"] = argument
        ret["predicate"] = append_predict

        return ret, d_ret