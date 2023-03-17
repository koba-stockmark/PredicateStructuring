import copy
from chunker import ChunkExtractor
from case_information_get import CaseExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from predicate_split import VerbSpliter
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
        self.head_connect_check = chunker.head_connect_check
        self.predicate_connect_check = chunker.predicate_connect_check
        self.rentai_check = chunker.rentai_check
        self.shuusi_check = chunker.shuusi_check
        c_get = CaseExtractor()
        self.case_get = c_get.case_get
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        self.para_ng_word = p_g.para_ng_word
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.sub_verb_chek = v_s.sub_verb_chek
        self.object_devide = v_s.object_devide
        self.not_devide_case_dic = v_s.not_devide_case_dic
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
    述語のマージ
    """
    def predicate_merge(self, append_predict, predicate, argument):
        for chek in append_predict:
            if chek["lemma"] == predicate["lemma"] and chek["lemma_start"] == predicate["lemma_start"] and chek["lemma_end"] == predicate["lemma_end"] and not chek["sub_lemma"] and predicate["sub_lemma"]:
                for arg in argument:
                    if arg["predicate_id"] == chek["id"] and arg["subject"]:    # 主語がある場合はマージしない
                        append_predict.append(copy.deepcopy(predicate))
                        return
                chek["sub_lemma"] = predicate["sub_lemma"]
                chek["sub_lemma_start"] = predicate["sub_lemma_start"]
                chek["sub_lemma_end"] = predicate["sub_lemma_end"]
                chek["sub_orth"] = predicate["sub_orth"]
                for arg in argument:
                    if arg["predicate_id"] == chek["id"]:
                        arg["predicate_id"] = -1
                    if arg["predicate_id"] == chek["id"] + 1:    # 主語がある場合はマージしない
                        arg["predicate_id"] = arg["predicate_id"] - 1
                for a_pt, arg in enumerate(argument):
                    if arg["predicate_id"] == -1:
                        del argument[a_pt]
                return
        append_predict.append(copy.deepcopy(predicate))
        return

    """
    短い述部の併合
    """
    def short_predicate_delete(self, append_predict, predicate, argument):
        ret = 0
        del_id = 0
        for chek in reversed(append_predict):
            if chek["lemma_start"] >= predicate["lemma_start"] and chek["lemma_end"] <= predicate["lemma_end"]:
                for arg in reversed(argument):
                    if arg["predicate_id"] == chek["id"]:
                        arg["predicate_id"] = predicate["id"] - ret
                        if "not_direct_subject" in arg:
                            for check2 in argument:
                                if check2["predicate_id"] == predicate["id"]:
                                    if check2["subject"] and not "not_direct_subject" in check2:
                                        del argument[argument.index(arg)]
                                        break
                for arg in argument:
                    if arg["predicate_id"] >= chek["id"]:
                        arg["predicate_id"] = arg["predicate_id"] - 1
                for arg in reversed(argument):
                    if arg["predicate_id"] == chek["id"]:
                        for c_arg in reversed(range(argument.index(arg) + 1, len(argument))):
                            if argument[c_arg]["lemma"] == arg["lemma"]:
                                del argument[c_arg]
                del_id = chek["id"]
                ret = ret + 1
                for chek_p in append_predict:
                    if chek_p["id"] > del_id:
                        append_predict[chek_p["id"]]["id"] = append_predict[chek_p["id"]]["id"] - 1
#                del append_predict[chek["id"]]
                del append_predict[append_predict.index(chek)]
        return ret


    """
    主述部と補助術部に別れた述語項構造の取得
    """

    def pas_analysis(self, debug, text, *doc):

        argument = []
        append_predict = []
        predicate_relations = []
        attributs = []
        ret = {}
        verb_end = -1
        predicate_id = -1
        pre_predicate_id = -1
        d_ret = ''
        new_verb = False
        pre_rentai_subj = False
        argument_id = 0

        for token in doc:
            predicate = {}
            predicate_relation = {}
            subject_w = ''
            dummy_subj = {}
            sub_verb_w = ''
            save_verb_w = ''
            sub_verb = {}
            save_verb = {}
            para_subj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
            #
            #  述部の検索
            #
            if token.i <= verb_end:
                continue
            if token.tag_ == "空白":
                continue
            verb = self.predicate_get(token.i, *doc)
            if not verb or not verb["lemma"]:
                continue
            verb_w = verb["lemma"]
            verb_end = verb["lemma_end"]
            modality_w = verb["modality"]
            rule_id = verb["rule_id"]
            verb_rule_id = rule_id
            if len(doc) > verb_end + 1 and doc[verb_end + 1].norm_ == '為る': # 体言どめ用の補正
                verb_end = verb_end + 1
            #
            #  補助用言を含む述部の範囲を判別
            #
            predicate_start = verb["lemma_start"]
            predicate_end = verb["lemma_end"]
            for check in doc[verb["lemma_end"] + 1:]:
                if check.head.i <= verb["lemma_end"]:
                    predicate_end = predicate_end + 1
                else:
                    break
            #
            #  主語の検索
            #
#            ret_subj = self.subject_get(token.i, verb["lemma_end"], *doc)
            ret_subj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
            ret_subj_all = self.subject_get(verb["lemma_start"], verb["lemma_end"], *doc)
            case_wa = False
            case_ga = False
            ret_subj_wa = {}
            for check_subj in reversed(ret_subj_all):
                if "special_connection" in check_subj:
                    ret_subj = check_subj
                    subject_w = ret_subj['lemma']
                    break
                if doc[check_subj['lemma_end']].pos_ == 'PRON':
                    ret_subj = check_subj
                    subject_w = ret_subj['lemma']
                    break
                if doc[check_subj['lemma_end']].tag_ == '接尾辞-名詞的-助数詞' and len(ret_subj_all) > 1:
                    continue
                if doc[verb["lemma_end"]].lemma_ != 'こと' and doc[doc[verb["lemma_end"]].head.i].lemma_ != 'こと' and doc[verb["lemma_end"]].pos_ != 'NOUN':
                    if len(doc) > check_subj['lemma_end'] + 1 and doc[check_subj['lemma_end'] + 1].lemma_ == 'は':
                        if case_ga:
                            ret_subj = check_subj
                            subject_w = ret_subj['lemma']
                            break
                        ret_subj_wa = check_subj
                        case_wa = True
                    if len(doc) > check_subj['lemma_end'] + 1 and (doc[check_subj['lemma_end'] + 1].lemma_ == 'が' or doc[check_subj['lemma_end'] + 1].lemma_ == 'も'):
                        if case_wa:
                            ret_subj = ret_subj_wa
                            subject_w = ret_subj['lemma']
                            break
                        case_ga = True
                else:
                    if len(doc) > check_subj['lemma_end'] + 1 and doc[check_subj['lemma_end'] + 1].lemma_ == 'が':
                        ret_subj = check_subj
                        subject_w = ret_subj['lemma']
                        break
                if ((check_subj["lemma_start"] <= verb["lemma_start"] and check_subj["lemma_end"] >= verb["lemma_end"]) or
                    (verb["lemma_start"] <= check_subj["lemma_start"] <= verb["lemma_end"]) or
                    (verb["lemma_start"] <= check_subj["lemma_end"] <= verb["lemma_end"])):
                    continue
                if append_predict:
                    ng_f = False
                    for check_p in append_predict:
                        if (check_p["lemma_start"] <= check_subj["lemma_start"] <= check_p["lemma_end"]) or (check_p["lemma_start"] <= check_subj["lemma_end"] <= check_p["lemma_end"]):
                            if ((len(doc) > check_p["lemma_end"] + 2 and doc[check_p["lemma_end"] + 1].pos_ == "AUX" and doc[check_p["lemma_end"] + 2].pos_ == "SCONJ" and doc[check_p["lemma_end"] + 2].tag_ == "助詞-準体助詞") or
                                (len(doc) > check_p["lemma_end"] + 2 and doc[check_p["lemma_end"] + 2].pos_ == "SCONJ" and doc[check_p["lemma_end"] + 2].tag_ == "助詞-準体助詞")):
                                continue
                            ng_f = True
                            break
                    if ng_f:
                        continue
                if not token.dep_ == "nsubj" or (len(doc) > check_subj['lemma_end'] + 1 and doc[check_subj['lemma_end'] + 1].lemma_ != 'も'):  # 〇〇も　の例外処理でsubjを目的語にしている場合は自分自身をsubjにしない（省略されていると考える）
                    ret_subj = check_subj
                    subject_w = ret_subj['lemma']

            # 主語の表層格の取得
            subj_case = self.case_get(ret_subj['lemma_end'], *doc)
            if "rentai_subject" in ret_subj and ret_subj["rentai_subject"]:
                subj_case = "が(連体)"
            if subj_case == "を":    # を　格の主語は誤解析
                subject_w = ''
                ret_subj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}

            # 省略主語のセット
            if subject_w:
                if (self.rentai_check(verb["lemma_end"], *doc) or (doc[verb["lemma_end"]].morph.get("Inflection") and '連体形' in doc[verb["lemma_end"]].morph.get("Inflection")[0])) and verb["lemma_start"] < ret_subj["lemma_start"]:
                    pre_rentai_subj = True
                    subj_case = 'が(連体)'
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
                if "not_direct_subject" in ret_subj:
                    for para in para_subj:
                        para["not_direct_subject"] = True
            #
            #  つながる項の検索 (連用修飾、連体修飾もチェック)
            #
            find_f = False
            argument_map = []
            for i in range(0, verb["lemma_start"]):
                if doc[i].pos_ == 'ADP' or doc[i].pos_ == 'PART' or doc[i].pos_ == 'PUNCT':
                    continue
                if para_subj:
                    subject_is_same = False
                    for para in para_subj:
                        if para["lemma_start"] <= i <= para["lemma_end"]:  # 主語は対象外
                            subject_is_same = True
                    if subject_is_same:
                        continue
                if ret_subj["lemma"] and ret_subj["lemma_start"] <= i <= ret_subj["lemma_end"]:  # 主語は対象外
                    if doc[doc[i].head.i].norm_ == '出来る': # 〇〇が出来る　は例外
                        pass
                    else:
                        continue
                if ((doc[i].dep_ == "obj" and doc[i].head.dep_ != "obj") or (doc[i].dep_ == 'advcl' and doc[i].tag_ == '名詞-普通名詞-形状詞可能') or
                        (doc[i].dep_ == 'advcl' and len(doc) > i + 1 and doc[i + 1].tag_ == '助詞-格助詞') or
                        (doc[i].dep_ == 'advcl' and len(doc) > i + 1 and doc[i + 1].tag_ == '助詞-接続助詞') or
                        (doc[i].dep_ == 'advcl' and len(doc) > i + 1 and doc[i + 1].tag_ == '助動詞') or
                        (doc[i].dep_ == 'advcl' and len(doc) > i + 1 and doc[i + 1].tag_ == '動詞-非自立可能') or
                        (doc[i].dep_ == 'advmod' and doc[i].pos_ == 'ADV') or
                        ((doc[i].dep_ == 'amod' or doc[i].dep_ == 'acl') and doc[i].pos_ == 'ADJ') or
                        ((doc[i].dep_ == 'acl' or doc[i].dep_ == 'advcl' or doc[i].dep_ == 'ccomp') and doc[i].pos_ == 'VERB') or
                        (len(doc) > i + 1 and doc[i + 1].dep_ == 'case' and doc[i].orth_ != ret_subj["lemma"]) or
                        (len(doc) > i + 2 and doc[i + 1].tag_ == '補助記号-読点' and doc[i + 2].dep_ == 'case' and doc[i].orth_ != ret_subj["lemma"]) or
                        (len(doc) > i + 2 and doc[i + 1].tag_ == '接尾辞-形容詞的' and doc[i + 2].tag_ == '接尾辞-名詞的-一般' and doc[i].pos_ == "VERB") or
                        (doc[i].dep_ == 'nsubj' and doc[i].orth_ != ret_subj["lemma"]) or
                        (doc[i].dep_ == 'compound' and verb["lemma_start"] <= doc[i].head.i <= verb["lemma_end"]) or
                        (doc[i].lemma_ == '際' and predicate_start <= doc[i].head.i <= predicate_end) or
                        (doc[i].lemma_ == '場合' and predicate_start <= doc[i].head.i <= predicate_end) or
                        ((doc[i].dep_ == "obl" or doc[i].dep_ == "nmod")and doc[i - 1].lemma_ != 'が' and
                         (len(doc) > i + 1 and (doc[i + 1].pos_ != 'AUX' or doc[i + 1].lemma_ == 'で' or doc[i + 1].tag_ == '助詞-格助詞' or doc[i + 1].tag_ == '補助記号-読点')) and
                         (doc[i].norm_ != 'そこ' and doc[i].norm_ != 'それ') and
                         (doc[i].tag_ != '名詞-普通名詞-副詞可能' or doc[i].norm_ == '為' or doc[i].norm_ == '下' or doc[i].norm_ == '中' or doc[i].norm_ == 'うち' or doc[i].norm_ == 'もと' or doc[i].norm_ == '間') and (doc[i].norm_ != '度' or doc[i - 1].pos_ == 'NUM'))):  # この度　はNG
                    if doc[doc[i].head.i].lemma_ == '際' and doc[i + 1].lemma_ == 'の':   # 〇〇の際　は際から作る
                        continue
                    if len(doc) > i + 1 and doc[i].tag_ == "名詞-普通名詞-助数詞可能" and doc[i + 1].tag_ == "補助記号-読点" and doc[doc[i].head.i].tag_ == "名詞-普通名詞-助数詞可能":   # 〇〇円、…は〇〇円
                        continue
                    if len(doc) > i + 1 and doc[i + 1].lemma_ == '「':   #  〇〇「〇〇　カッコの外から中にかかる場合は　NG
                        kakko_f = True
                        for cpt in range(i + 2, len(doc)):
                            if doc[cpt].lemma_ == '」':
                                kakko_f = False
                            if doc[i].head.i == cpt:
                                break
                        if kakko_f:
                            continue
                    if doc[i].head.i < predicate_start or doc[i].head.i > predicate_end:  # 述部に直接かからない
                        if doc[i].head.head.i == token.i and (doc[i].head.morph.get("Inflection") and '連用形' not in doc[i].head.morph.get("Inflection")[0]):  # 連用形接続でもつながらない
                            if (doc[doc[i].head.i + 1].tag_ != '接尾辞-形容詞的' and (doc[doc[i].head.i].tag_ != '名詞-普通名詞-副詞可能' or doc[doc[i].head.i].lemma_ == 'ため' or doc[doc[i].head.i].lemma_ == 'もと' or doc[doc[i].head.i].lemma_ == '前')) or doc[i].head.head.pos_ == 'NOUN':
                                if doc[i].lemma_ == '際' and doc[i].head.head.i == predicate_start:
                                    pass
                                else:
                                    continue
                            elif doc[doc[i].head.i].dep_ == 'obj':
                                continue
                        elif doc[i].head.pos_ == 'VERB' and doc[i].head.head.i == verb["lemma_start"]:  # 特別処理　「ツールをより使いやすく、バージョンアップ」
                            continue
                        elif doc[i].head.lemma_ == '共同' and doc[doc[i].head.i -1].lemma_ == 'と' and predicate_start <= doc[i].head.head.i <= predicate_end: # 〇〇と共同で　はかかり関係が特殊なので襟外処理
                            pass
                        elif len(doc) > i + 1 and doc[i + 1].dep_ == 'case' and doc[i + 1].lemma_ == 'から' and doc[i].dep_ != 'nsubj' and self.predicate_connect_check(verb["lemma_start"] ,i ,  *doc):
                            pass
                        else:
                            continue
                    if (len(doc) > i + 2 and doc[i + 1].lemma_ == 'た' and doc[i + 2].lemma_ == '際' and doc[i + 2].head.i == i) or (len(doc) > i + 1 and doc[i + 1].lemma_ == '際' and doc[i + 1].head.i == i):
                        continue
                    ng_f = False
                    kakko = 0
                    for chp in range(i, verb["lemma_start"]):
                        if doc[chp].lemma_ == '「':
                            kakko = kakko + 1
                        if doc[chp].lemma_ == '」':
                            kakko = kakko - 1
                        if doc[chp].lemma_ == '。' and kakko == 0:
                            ng_f = True
                            break
                    if ng_f:
                        continue
                    find_f = True
                    argument_map += [i]
            #######################################
            #  PASの作成
            #######################################
            #
            #  主語のセット
            #
            predicate_id = predicate_id + 1
            predicate_relation_id = -1
            if subject_w:
                ret_subj["case"] = subj_case
                ret_subj["dummy"] = False
                ret_subj["subject"] = True
                ret_subj["id"] = argument_id
                argument_id = argument_id + 1
                ret_subj["predicate_id"] = predicate_id
                argument.append(ret_subj)
                if para_subj and para_subj[0]['lemma']:
                    for p_subj in para_subj:
                        p_subj["case"] = subj_case
                        p_subj["dummy"] = False
                        p_subj["subject"] = True
                        p_subj["id"] = argument_id
                        argument_id = argument_id + 1
                        p_subj["predicate_id"] = predicate_id
                        argument.append(p_subj)
            elif dummy_subj:
                dummy_subj["dummy"] = True
                dummy_subj["subject"] = True
                dummy_subj["id"] = argument_id
                argument_id = argument_id + 1
                dummy_subj["predicate_id"] = predicate_id

                argument.append(dummy_subj)
            # 項のセット
            relation_case = ""
            for i in range(0, verb["lemma_start"]):
                case = ''
                ret_obj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
                rule_id = verb_rule_id
                para_obj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1, "subject": False}]
                para_subject_case = ""
                if find_f and i in argument_map:
                    #
                    # 項の取得
                    #
                    if find_f:
                        #
                        #  他の項に包含されるかチェック
                        #
                        hougan_f = False
                        for check in argument:
                            if check["lemma_start"] <= i <= check["lemma_end"] and predicate_id == check["predicate_id"]:
                                hougan_f = True
                                break
                        if hougan_f:
                            continue
                        #
                        # 項の獲得
                        #
                        if ((doc[i].dep_ == 'advcl' or doc[i].dep_ == 'acl' or doc[i].dep_ == 'ccomp') and (doc[i].pos_ == 'ADJ' or doc[i].pos_ == 'AUX' or doc[i].pos_ == 'VERB')) or (len(doc) > i + 1 and doc[i].pos_ == 'VERB' and doc[i + 1].pos_ == 'AUX' and (len(doc) <= i + 2 or (len(doc) > i + 2 and doc[i + 2].pos_ != 'PART'))):
                            """
                            ret_obj = self.verb_chunk(i, *doc)
                            """
                            #
                            #   PAS リレーション
                            #
                            predicate_find = False
                            for check_predict in append_predict:
                                if check_predict["lemma_start"] <= i <= check_predict["lemma_end"]:
                                    ret_obj["lemma"] = check_predict["lemma"]
                                    ret_obj["lemma_start"] = check_predict["lemma_start"]
                                    ret_obj["lemma_end"] = check_predict["lemma_end"]
                                    predicate_relation_id = check_predict["id"]
                                    check_predict["predicate_relation_to"] = predicate_id
                                    predicate_find = True
                                    break
                            if not predicate_find:
                                if doc[i].lemma_ == "する" and doc[i - 1].pos_ == "ADP" and doc[i - 1].lemma_ == "と" and doc[i - 2].pos_ == "NOUN":
                                    for j in reversed(range(0, i)):
                                        if j == 0 or ((doc[j].pos_ != "ADP" or doc[j].lemma_ != "と") and doc[j].pos_ != "AUX"):
                                            ret_obj = self.verb_chunk(j, *doc)
                                            for jj in range(j + 1, i):
                                                ret_obj['lemma'] = ret_obj['lemma'] + doc[jj].orth_
                                            ret_obj['lemma'] = ret_obj['lemma'] + doc[i].lemma_
                                            ret_obj['lemma_end'] = i
                                            break
                                else:
                                    ret_obj = self.verb_chunk(i, *doc)
                        else:
                            ret_obj = self.num_chunk(i, *doc)
                            if doc[i].tag_ == "連体詞" and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                                ret_obj["lemma"] = doc[i].lemma_
                                ret_obj["lemma_end"] = ret_obj["lemma_start"]
                            #
                            # 項の並列処理
                            #
                            if len(doc) > ret_obj["lemma_end"] + 2 and doc[ret_obj["lemma_end"] + 1].lemma_ == "と" and doc[ret_obj["lemma_end"] + 2].lemma_ in self.para_ng_word:   # NGワードは並列処理しない
                                continue
                            if doc[ret_obj["lemma_start"]].dep_ != 'advcl':
                                para_obj = self.para_get(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                                if para_obj and (ret_obj["lemma"] == 'とも' or ret_obj["lemma"] == '共') and doc[ret_obj['lemma_start'] - 1].lemma_ == 'と' and doc[ret_obj['lemma_start'] + 1].lemma_ == 'に':    # 〇〇とともに　は例外
                                    ret_obj = para_obj[0]
                                    del para_obj[0]
                                    case = "とともに"
                                para_subject_case = ""
                                if para_obj and para_obj[0]["subject"]:
                                    for check_arg in argument:
                                        if check_arg["subject"]:
                                            para_subject_case = check_arg["case"]
                    elif verb["lemma"] == 'ため':     # ためだけの述部はNGとする
                        continue
                    else:
                        pass  # 通るか確認
                    #
                    # 格情報の取得
                    #
                    if ret_obj:
                        if not case:
                            if doc[ret_obj["lemma_start"]].dep_ == 'advcl' and doc[ret_obj["lemma_end"]].dep_ != 'advcl' and doc[ret_obj["lemma_end"]].pos_ != 'NOUN'  and doc[ret_obj["lemma_end"]].pos_ != 'PROPN' and doc[ret_obj["lemma_end"]].pos_ != 'AUX' and doc[ret_obj["lemma_end"]].tag_ != '動詞-非自立可能':
                                case = self.case_get(ret_obj['lemma_start'], *doc)
                            else:
                                case = self.case_get(ret_obj['lemma_end'], *doc)
                        if predicate_relation_id >= 0 and not relation_case:
                            relation_case = case
                    else:
                        if not case:
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
                    #
                    # 並列項のセット
                    #
                    if para_obj and para_obj[0]["lemma"]:
                        for p_obj in para_obj:
                            if para_subject_case:
                                p_obj["case"] = para_subject_case
                            else:
                                p_obj["case"] = case
#                            p_obj["subject"] = False
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
            #################################
            #  主語が前にある連体修飾で項がない場合は連体修飾先を項とする
            #################################
            if (subject_w and ret_subj["case"] == 'が' and
                    ("rentai_subject" not in ret_subj or not ret_subj["rentai_subject"]) and
                    not argument_map and
#                    (self.shuusi_check(verb["lemma_end"], *doc) or self.rentai_check(verb["lemma_end"], *doc)) and
                    (self.rentai_check(verb["lemma_end"], *doc)) and
                    doc[verb["lemma_end"] + 1].lemma_ != 'こと' and
                    (doc[verb["lemma_end"] + 1].pos_ != 'AUX' or (doc[verb["lemma_end"] + 2].lemma_ != 'こと' and doc[verb["lemma_end"] + 2].norm_ != '中')) and
                    doc[doc[verb["lemma_end"]].head.i].lemma_ != 'こと' and doc[verb["lemma_end"]].pos_ != "ADJ"):
#                    doc[doc[verb["lemma_end"]].head.i].pos_ == 'NOUN' and doc[doc[verb["lemma_end"]].head.i].lemma_ != 'こと' and doc[verb["lemma_end"]].pos_ != "ADJ":
                ret_obj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
                if doc[doc[verb["lemma_end"]].head.i].pos_ == 'NOUN':
                    ret_obj = self.num_chunk(doc[verb["lemma_end"]].head.i, *doc)
                else:
                    for cpt in range(verb["lemma_end"] + 1, len(doc)):
                        if doc[cpt].head.i == doc[verb["lemma_end"]].head.i and doc[cpt].head.dep_ != 'ROOT':
                            ret_obj = self.num_chunk(cpt, *doc)
                            break

    #
                # 項の並列処理
                #
                para_obj = self.para_get(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                case = 'を'
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
#                        p_obj["subject"] = False
                        p_obj["id"] = argument_id
                        p_obj["predicate_id"] = predicate_id
                        argument_id = argument_id + 1
                        argument.append(p_obj)
            # データダンプ
            if find_f and debug:
                d_ret = d_ret + self.data_dump_and_save(text, argument, verb, predicate_id)
            ##########################################################################################
            #  メイン術部の分割処理   すべての項に対してチェックして最終的な述部を判断する
            ##########################################################################################
            verb_from_object = False
            split_f = False
            add_arg = {}
            for re_arg in argument:
                if predicate_id != re_arg["predicate_id"]:
                    continue
                if re_arg["subject"]:   # 主語から動詞生成はない
                    not_all_subject = False
                    for check in argument:
                        if not check["subject"] and check["predicate_id"] == re_arg["predicate_id"]:
                            not_all_subject = True
                            break
                    if not_all_subject:
                        continue
                ##########################################################################################################################################
                #   主述部と補助術部の判断 (どの項によって主述部が生成されるか最後までわからないので遅くなるが重複処理を行う)
                ##########################################################################################################################################
                sub_verb_is_original = True
                if self.sub_verb_chek(verb_w, verb, *doc) and verb:
                    sub_verb_is_original = False
                    sub_verb_w = verb_w
                    sub_verb["lemma"] = verb["lemma"]
                    sub_verb["lemma_start"] = verb["lemma_start"]
                    sub_verb["lemma_end"] = verb["lemma_end"]
                    save_verb["lemma"] = verb["lemma"]
                    save_verb["lemma_start"] = verb["lemma_start"]
                    save_verb["lemma_end"] = verb["lemma_end"]
                    save_verb_w = verb_w
                    verb_w = ''
                    verb["lemma"] = ''
                    verb["lemma_start"] = -1
                    verb["lemma_end"] = -1

                ##########################################################################################################################################
                #    目的語を述部と分割
                ##########################################################################################################################################

                if verb_from_object or (re_arg and not verb_w):
                    if doc[re_arg["lemma_end"]].dep_ == 'advcl':        # 助動詞以外の　で格　は分離しない
                        continue
                    if re_arg['case'] in self.not_devide_case_dic:
                        continue
                    if 'subject' in re_arg and re_arg['subject'] and re_arg['case'] != 'も':
                        continue
                    dev_obj = self.object_devide(re_arg['lemma_start'], re_arg['lemma_end'], re_arg['case'], argument, append_predict, *doc)
                    if dev_obj["verb"]:
                        re_arg["lemma"] = dev_obj["object"]
                        re_arg["lemma_end"] = dev_obj["verb_start"] - 2
                        re_arg["case"] = "を"
                        if "new_object_start" in dev_obj:
                            re_arg["lemma_start"] = dev_obj["new_object_start"]
                            re_arg["lemma_end"] = dev_obj["new_object_end"]
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
                    elif (dev_obj["object"] != re_arg['lemma'].split("(")[0] and dev_obj["object"] != re_arg['lemma'].split("の")[0] and not re_arg['lemma'].endswith("」")) and len(dev_obj["object"]) < len(re_arg['lemma']):
                        re_arg['lemma'] = dev_obj["object"]

                ##########################################################################################################################################
                #    複合術部のメインと補助への分割
                ##########################################################################################################################################
                dev_verb = {}
                if verb and verb['lemma']:
                    dev_verb = self.verb_devide(verb["lemma_start"], verb["lemma_end"], *doc)
                elif sub_verb and sub_verb['lemma']:
                    dev_verb = self.verb_devide(sub_verb["lemma_start"], sub_verb["lemma_end"], *doc)
                if dev_verb and dev_verb["sub_verb"] and dev_verb["verb"]:  # 補助述部がある
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
                    if "object" in dev_verb:
                        add_arg["lemma"] = dev_verb["object"]
                        add_arg["lemma_start"] = dev_verb["obj_start"]
                        add_arg["lemma_end"] = dev_verb["obj_end"]
                        add_arg["case"] = "を"
                        add_arg["subject"] = False
                        add_arg["id"] = re_arg["id"] + 1
                        add_arg["predicate_id"] = re_arg["predicate_id"]

                ##########################################################################################################################################
                #    目的語からの主述部がない場合は補助術部を主述部へもどす
                ##########################################################################################################################################
                if not verb_w and sub_verb_w:  # 目的語からの主述部がない場合は補助術部を主述部へもどす
                    if "lemma" in save_verb:
                        verb_w = save_verb_w
                        verb["lemma"] = save_verb["lemma"]
                        verb["lemma_start"] = save_verb["lemma_start"]
                        verb["lemma_end"] = save_verb['lemma_end']
                    else:
                        verb_w = sub_verb_w
                        verb["lemma"] = sub_verb["lemma"]
                        verb["lemma_start"] = sub_verb["lemma_start"]
                        verb["lemma_end"] = sub_verb['lemma_end']
                    sub_verb_w = ''
                    sub_verb["lemma"] = ''
                    sub_verb["lemma_start"] = -1
                    sub_verb['lemma_end'] = -1
                    new_verb = False
                ##########################################################################################################################################
                #    述部が変更された場合は新しいものを保存
                ##########################################################################################################################################
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
#                    predicate["modality"] = ', '.join([str(x) for x in modality_w])
                    predicate["modality"] = modality_w
                    predicate["rule_id"] = rule_id
                    if sub_verb and sub_verb_w:
                        predicate["sub_lemma"] = sub_verb["lemma"]
                        predicate["sub_lemma_start"] = sub_verb["lemma_start"]
                        predicate["sub_lemma_end"] = sub_verb["lemma_end"]
                        predicate["sub_orth"] = sub_verb_w
                    else:
                        predicate["sub_lemma"] = ''
                        predicate["sub_lemma_start"] = -1
                        predicate["sub_lemma_end"] = -1
                        predicate["sub_orth"] = ''
                    pre_predicate_id = predicate_id
                    del_ct = self.short_predicate_delete(append_predict, predicate, argument)
                    if del_ct > 0:  # 新しい述部より短い過去の述部を削除
                        predicate_id = predicate_id - del_ct
                        pre_predicate_id = pre_predicate_id - del_ct
                        predicate["id"] = predicate["id"] - del_ct
                    if split_f:
                        predicate["id"] = predicate["id"] + 1
                        for change_arg in argument:
                            if change_arg["predicate_id"] == predicate_id:
                                argument.append(copy.deepcopy(change_arg))
                                argument[-1]["predicate_id"] = argument[-1]["predicate_id"] + 1
                        re_arg["predicate_id"] = re_arg["predicate_id"]
                        self.predicate_merge(append_predict, predicate, argument)
                        predicate_id = predicate_id + 1
                        pre_predicate_id = pre_predicate_id + 1
                    else:
                        self.predicate_merge(append_predict, predicate, argument)
                        split_f = True
                    if predicate_relation_id >= 0 and len(append_predict) > predicate_relation_id:
                        predicate["predicate_relation_from"] = predicate_relation_id
                        predicate_relation["from_id"] = predicate_relation_id
                        predicate_relation["to_id"] = predicate_id
                        predicate_relation["relation"] = relation_case
                        predicate_relation["from_predicate"] = append_predict[predicate_relation_id]
                        predicate_relation["to_predicate"] = append_predict[predicate_id]
                        predicate_relations.append(copy.deepcopy(predicate_relation))
                    # 述部に含まれた項の削除
                    for del_arg in reversed(argument):
                        if del_arg["predicate_id"] == predicate["id"] and del_arg["lemma_start"] >= predicate["lemma_start"] and del_arg["lemma_end"] <= predicate["lemma_end"]:
                            del argument[argument.index(del_arg)]

            #
            if add_arg:
                argument.append(add_arg)

            ##########################################################################################################################################
            #    目的語からの主述部がない場合は補助術部を主述部へもどす
            ##########################################################################################################################################
            if not verb_w and sub_verb_w:  # 目的語からの主述部がない場合は補助術部を主述部へもどす
                verb_w = sub_verb_w
                sub_verb_w = ''
                verb["lemma"] = sub_verb["lemma"]
                verb["lemma_start"] = sub_verb["lemma_start"]
                verb["lemma_end"] = sub_verb['lemma_end']
                sub_verb["lemma"] = ''
                sub_verb["lemma_start"] = -1
                sub_verb['lemma_end'] = -1
                new_verb = False
            ##########################################################################################################################################
            #    最終的な述部の整理
            ##########################################################################################################################################
            if pre_predicate_id != predicate_id:
                predicate["id"] = predicate_id
                predicate["lemma"] = verb["lemma"]
                predicate["lemma_start"] = verb["lemma_start"]
                predicate["lemma_end"] = verb["lemma_end"]
                predicate["orth"] = verb_w
#                predicate["modality"] = ', '.join([str(x) for x in modality_w])
                predicate["modality"] = modality_w
                predicate["rule_id"] = rule_id
                if sub_verb and sub_verb_w:
                    predicate["sub_lemma"] = sub_verb["lemma"]
                    predicate["sub_lemma_start"] = sub_verb["lemma_start"]
                    predicate["sub_lemma_end"] = sub_verb["lemma_end"]
                    predicate["sub_orth"] = sub_verb_w
                else:
                    predicate["sub_lemma"] = ''
                    predicate["sub_lemma_start"] = -1
                    predicate["sub_lemma_end"] = -1
                    predicate["sub_orth"] = ''
                pre_predicate_id = predicate_id
                del_ct = self.short_predicate_delete(append_predict, predicate, argument)
                if del_ct > 0:  # 新しい述部より短い過去の述部を削除
                    predicate_id = predicate_id - del_ct
                    predicate["id"] = predicate["id"] - del_ct
                    pre_predicate_id = pre_predicate_id - del_ct
                self.predicate_merge(append_predict, predicate, argument)
                if predicate_relation_id >= 0 and len(append_predict) > predicate_relation_id:
                    predicate["predicate_relation_from"] = predicate_relation_id
                    predicate_relation["from_id"] = predicate_relation_id
                    predicate_relation["to_id"] = predicate_id
                    predicate_relation["relation"] = relation_case
                    predicate_relation["from_predicate"] = append_predict[predicate_relation_id]
                    predicate_relation["to_predicate"] = append_predict[predicate_id]
                    predicate_relations.append(copy.deepcopy(predicate_relation))
                # 述部に含まれた項の削除
                for del_arg in reversed(argument):
                    if del_arg["predicate_id"] == predicate["id"] and del_arg["lemma_start"] >= predicate["lemma_start"] and del_arg["lemma_end"] <= predicate["lemma_end"]:
                        del argument[argument.index(del_arg)]

        ##########################################################################################################################################
        #    メイン述部の判断
        #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
        #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
        ##########################################################################################################################################
        for predic in append_predict:
            predic["main"] = False
            if predic["sub_lemma_start"] > 0:
                v_rule_id = self.main_verb_chek(predic["sub_lemma_end"], *doc)
                if v_rule_id < 0:   # 補助術部が２段で分割されている場合も考慮
                    v_rule_id = self.main_verb_chek(doc[predic["sub_lemma_end"]].head.i, *doc)
            else:
                v_rule_id = self.main_verb_chek(predic["lemma_end"], *doc)
            if v_rule_id > 0:
                predic["main_rule_id"] = v_rule_id
                predic["main"] = True
        for arg in argument:
            if not arg["lemma"] and not arg["subject"]:
                argument.remove(arg)

        #
        # 項のアトリビュート（連体修飾）のセット
        #
        attribute = {}
        for ch_predic in append_predict:
            if self.rentai_check(ch_predic["lemma_start"], *doc):
                for ch_arg in argument:
                    if ch_arg["lemma_start"] <= doc[ch_predic["lemma_start"]].head.i <= ch_arg["lemma_end"]:
                        attribute["predicate_id"] = ch_predic["id"]
                        attribute["argument_id"] = ch_arg["id"]
                        attributs.append(copy.deepcopy(attribute))

        ret["argument"] = argument
        ret["predicate"] = append_predict
        ret["argument_attribute"] = attributs
        ret["predicate_relation"] = predicate_relations

        return ret, d_ret