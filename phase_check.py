from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from phase_rule_dic import PhaseRule
from government_action_dic import GovernmentActionRule

class PhaseCheker:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

    # 完全一致での辞書とのマッチング
    def rule_check(self, verb, rule):
        if verb in rule:
            return True
        return False

    # 後方一致での辞書とのマッチング
    def rule_check2(self, verb, rule):
        for check in rule:
            if check == verb[-len(check):]:
                return True
        return False

    def phase_chek(self, start, end, obj_start, obj_end, pre_phase, p_rule, *doc):
        chunker = ChunkExtractor()
#        p_rule = PhaseRule()
        s_v_dic = SubVerbDic()
        ret = ''
        new_end = end
        for c_pt in range(start, end):      # 述部の語幹だけを切り出す
            if doc[c_pt].pos_ == 'ADP' and (doc[c_pt].lemma_ != 'を' or (doc[c_pt].lemma_ == 'を' and len(doc) > c_pt + 1 and doc[c_pt + 1].norm_ == '為る')):
                new_end = c_pt - 1
                break
        verb_word = chunker.compaound(start, new_end, *doc)
        # 補助表現以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic or verb_word in s_v_dic.special_sub_verb_dic:
            # フルマッチ
            for rule in p_rule.phrase_rule:
                if self.rule_check(verb_word, rule["words"]):
                    if ret:
                        ret = ret + ',' + rule["label"]
                    else:
                        ret = ret + rule["label"]
            # フルマッチでない場合は後方マッチ
            if not ret:
                for rule in p_rule.phrase_rule:
                    if self.rule_check2(verb_word, rule["words"]):
                        if ret:
                            ret = ret + ',' + rule["label"]
                        else:
                            ret = ret + rule["label"]
        # 目的語からフェーズをチェック
        if verb_word in s_v_dic.sub_verb_dic and verb_word not in s_v_dic.special_sub_verb_dic and obj_start:
            ret2 = self.phase_chek(obj_start, obj_end, -1, -1, '', p_rule,  *doc)
            # 項全体として重複をチェック
            for ret3 in ret2.split(','):
                if ret3 not in ret:
                    ret = ret + ret3 + ','
            # 項の部分要素を重複をチェック
            for pt in range(obj_start, obj_end + 1):
                if (len(doc) > pt + 1 and (doc[pt + 1].lemma_ == '方' or doc[pt + 1].lemma_ == 'ため')) or (len(doc) > pt + 2 and doc[pt + 1].pos_ == 'AUX' and (doc[pt + 2].lemma_ == '方' or doc[pt + 2].lemma_ == 'ため')):      # 〇〇する方　はフェーズ判断に用いな
                    continue
                ret2 = self.phase_chek(pt, pt, -1, -1, '', p_rule, *doc)
                for ret3 in ret2.split(','):
                    if ret3 not in ret:
                        ret = ret + ret3 + ','
        # 補助表現がメイン術部のとき
        if not pre_phase and not ret and verb_word in s_v_dic.sub_verb_dic:
            for rule in p_rule.phrase_rule:
                if verb_word in rule["words"]:
                    if ret:
                        ret = ret + ',' + rule["label"]
                    else:
                        ret = ret + rule["label"]
        return ret.rstrip(',')

    #
    #  マルチラバルをシングルラベルへ
    #

    def single_phase_get(self, phase):
        rule = PhaseRule()

        if "<時制.未来>" in phase:
            return '研究・開発'
        if "<更新>" and "<実験>" in phase:
            return '研究・開発'
        for check in rule.single_rule:
            for check_label in check["labels"]:
                if check_label in phase:
                    return check["single"]
#        return 'その他'
        return ''

    ##########################################################################################################################################
    #    補助述部の時制チェック
    ##########################################################################################################################################

    def sub_phase_check(self, predicate, *doc):
        rule = PhaseRule()

        if predicate["sub_lemma"]:
            if predicate["sub_lemma"] in rule.mirai:
                return "<時制.未来>"
            if predicate["sub_lemma"] in rule.genzai:
                return "<時制.現在>"
            if predicate["sub_lemma"] in rule.kako:
                return "<時制.過去>"
        return ''

    ##########################################################################################################################################
    #    主述部のフェイズチェック
    ##########################################################################################################################################

    def rule_chek_and_set(self, predicate, argument, p_rule, *doc):
        rule = PhaseRule()
        s_v_dic = SubVerbDic()
        chunker = ChunkExtractor()

        single = ''
        phase = ""
        for chek_predicate in predicate:
            if chek_predicate["main"]:
                pre_phase = ''
                koto_f = False
                for re_arg in argument:
                    phase = ''
                    if chek_predicate["id"] != re_arg["predicate_id"]:
                        continue
                    if not re_arg["case"]:
                        continue
                    if re_arg["subject"] and doc[re_arg["lemma_end"]].lemma_ != 'こと' and re_arg["case"] != 'が' and re_arg["case"] != 'も':  # 他の項がある主語からフェーズ生成はない
                        new_end = chek_predicate["lemma_end"]
                        for c_pt in range(chek_predicate["lemma_start"], chek_predicate["lemma_end"]):  # 述部の語幹だけを切り出す
                            if doc[c_pt].pos_ == 'ADP' and doc[c_pt].lemma_ != 'を':
                                new_end = c_pt - 1
                                break
                        verb_word = chunker.compaound(chek_predicate["lemma_start"], new_end, *doc)
                        if p_rule == PhaseRule:
                            if verb_word in s_v_dic.sub_verb_dic:
                                continue
                    if re_arg["case"] == 'は' and not re_arg["subject"]:
                        no_subject = True
                        for check in argument:
                            if check["subject"] and check["predicate_id"] == re_arg["predicate_id"]:
                                no_subject = False
                                break
                        if no_subject:
                            continue
                    if koto_f:    # 〜こと　の項があった場合は優先して　「を格」以外は拡張しない
                        continue
#                    if re_arg["case"] not in rule.phase_analyze_case and "副詞的" not in re_arg["case"]:
                    if re_arg["case"] not in rule.phase_analyze_case:
                        continue
                    if "rentai_subject" in re_arg:
                        continue
                    if not phase:
                        check_end = chek_predicate["lemma_end"]
                        if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                            check_end = check_end - 1
                        # 〜こと　は例外で項の先頭を見る
                        if doc[re_arg['lemma_end']].lemma_ == 'こと':
                            for check_p in predicate:
                                if check_p["lemma_start"] <= re_arg['lemma_start'] <= check_p["lemma_end"] or check_p["sub_lemma_start"] <= re_arg['lemma_start'] <= check_p["sub_lemma_end"]:
                                    for check_a in argument:
                                        if check_a["predicate_id"] == check_p["id"]:
                                            phase = self.phase_chek(check_p["lemma_start"], check_p["lemma_end"], check_a["lemma_start"], check_a["lemma_end"], '', p_rule, *doc)
                                            pre_phase = phase
                                            if re_arg["subject"]:
                                                koto_f = True
                                            if not phase and chek_predicate["sub_lemma"]:
                                                check_end = chek_predicate["sub_lemma_end"]
                                                if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                                                    check_end = check_end - 1
                                                add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                                                pre_phase = add_phase
                                                for append in add_phase.split(','):  # 重複は登録しない
                                                    if append != '<その他>' and append != '<告知>' and append not in phase:
                                                        if phase:
                                                            phase = phase + ',' + append
                                                        else:
                                                            phase = append
                            if not phase:
                                phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                        else:
                            phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                        pre_phase = phase
                        if not phase and chek_predicate["sub_lemma"]:
                            check_end = chek_predicate["sub_lemma_end"]
                            if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                                check_end = check_end - 1
                            add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                            pre_phase = add_phase
                            for append in add_phase.split(','):  # 重複は登録しない
                                if append != '<その他>' and append != '<告知>' and append not in phase:
                                    if phase:
                                        phase = phase + ',' + append
                                    else:
                                        phase = append
                    if phase:
                        ret_tence = self.sub_phase_check(chek_predicate, *doc)
                        if ret_tence not in phase:
                            phase = phase + ',' + ret_tence
                    else:
                        phase = self.sub_phase_check(chek_predicate, *doc)
                    if phase:
                        if "phase" not in re_arg:
                            re_arg["phase"] = phase
                        else:
                            re_arg["phase"] = re_arg["phase"] + ',' + phase
                    if phase:  # phaseのある最終術部のphaesをシングルphaseにする
                        if p_rule == PhaseRule:
                            single = self.single_phase_get(phase)
                        else:
                            for check_phase in phase.split(","):
                                if check_phase not in single:
                                    if single:
                                        single = single + "," + check_phase
                                    else:
                                        single = check_phase
        return single

    ##########################################################################################################################################
    #    主述部のフェイズチェック
    ##########################################################################################################################################

    def phase_get_and_set(self, predicate, argument, *doc):
        return self.rule_chek_and_set(predicate, argument, PhaseRule, *doc)

    ##########################################################################################################################################
    #    主述部のフェイズチェック
    ##########################################################################################################################################
    government_rule = ["省", "庁", "政府"]
    ng_word = ["帰省", "省エネ", "省エネルギー", "省力化", "官公庁"]

    def government_action_get_and_set(self, predicate, argument, *doc):
        g_a_dic = GovernmentActionRule()
        # 政府活動かの判断
        government_predicate = []
        is_government = False
        is_government_press = False
        for arg in argument:
            if arg["subject"] or arg["case"] == "で" or arg["case"] == "から" or arg["case"] == "に" or arg["case"] == "は" or is_government_press:
                for check in self.government_rule:
                    if check in arg["lemma"] or is_government_press:
                        ngw_f = False
                        for ng_w in self.ng_word:
                            if ng_w in arg["lemma"]:
                                ngw_f = True
                                break
                        if not ngw_f:
                            is_government = True
                            if arg["predicate_id"] not in government_predicate:
                                government_predicate.append(arg["predicate_id"])
                                check_lemma = predicate[arg["predicate_id"]]["lemma"]
                                if "する" in check_lemma:
                                    check_lemma = check_lemma.rstrip("する")
                                if (check_lemma in g_a_dic.sakusei_dic or check_lemma in g_a_dic.koudou_dic or
                                        check_lemma in g_a_dic.soshiki_dic or check_lemma in g_a_dic.baikyaku_dic or
                                        check_lemma in g_a_dic.yuushi_dic or check_lemma in g_a_dic.kannkoku_dic or
                                        check_lemma in g_a_dic.kounyuu_dic or check_lemma in g_a_dic.keiyaku_dic or
                                        check_lemma in g_a_dic.shingi_dic or check_lemma in g_a_dic.sosyou_dic or
                                        check_lemma in g_a_dic.yousei_dic or check_lemma in g_a_dic.date_dic):
                                    is_government_press = True
                            break
                        """
                            not_syuusyoku_f = True
                            for i in range(arg["lemma_start"], arg["lemma_end"] + 1):
                                if doc[i].lemma_ == "の" and check in doc[i - 1].lemma_:
                                    not_syuusyoku_f = False
                                    break
                            if not_syuusyoku_f:
                                is_government = True
                                break
                        """
        if not is_government:
            return ""

        # 発信国の判断
        country = "日本"
        other_country = ''
        sub_country = ''
        sub_country_ari = False
        subject_ari = False
        for arg in argument:
            if arg["subject"]:
                predicate_is_main = False
                if predicate[arg["predicate_id"]]["main"]:
                    predicate_is_main = True
                for i in range(arg["lemma_start"], arg["lemma_end"] + 1):
                    if doc[i].tag_ == "名詞-固有名詞-地名-国":
                        if predicate_is_main:
                            subject_ari = True
                            country = doc[i].lemma_
                        else:
                            other_country = doc[i].lemma_
                    elif doc[i].lemma_ == "米" and i != arg["lemma_end"] and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                        if predicate_is_main:
                            subject_ari = True
                            country = "米国"
                        else:
                            other_country = "米国"
                    elif doc[i].lemma_ == "英" and i != arg["lemma_end"] and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                        if predicate_is_main:
                            subject_ari = True
                            country = "英国"
                        else:
                            other_country = "英国"
                    elif doc[i].lemma_ == "韓" and i != arg["lemma_end"] and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                        if predicate_is_main:
                            subject_ari = True
                            country = "韓国"
                        else:
                            other_country = "韓国"
                    elif doc[i].lemma_ == "中" and i != arg["lemma_end"] and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                        if predicate_is_main:
                            subject_ari = True
                            country = "中国"
                        else:
                            other_country = "中国"
            if arg["case"] == "で" and predicate[arg["predicate_id"]]["main"]:
                for i in range(arg["lemma_start"], arg["lemma_end"] + 1):
                    if doc[i].tag_ == "名詞-固有名詞-地名-国":
                        sub_country_ari = True
                        sub_country = doc[i].lemma_
        # 国が全く見つからないときは他の述部か探す
        if not subject_ari and not sub_country_ari and other_country:
            country = other_country
        if not subject_ari and sub_country_ari:
            country = sub_country

        ret = self.rule_chek_and_set(predicate, argument, GovernmentActionRule, *doc)
        if ret:
            gover_ret = ""
            for arg in argument:
                if arg["predicate_id"] in government_predicate or is_government_press:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase
            if gover_ret:
                return "<政府活動>,<" + country + ">," + gover_ret
            return ""
        elif is_government_press:
            return "<政府活動>,<" + country + ">," + "<情報発信>"
        else:
            return ret
