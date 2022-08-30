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
        if start == -1 or end == -1:
            return ""
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
        if verb_word in s_v_dic.sub_verb_dic and verb_word not in s_v_dic.special_sub_verb_dic and obj_start >= 0:
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
    #    フェイズ可能性ありの補助述部の例外チェック
    ##########################################################################################################################################
    def sub_predicate_check(self, predicate, p_rule, *doc):
        chunker = ChunkExtractor()
        s_v_dic = SubVerbDic()

        start = predicate["lemma_start"]
        end = predicate["lemma_end"]
        new_end = end
        for c_pt in range(start, end):      # 述部の語幹だけを切り出す
            if doc[c_pt].pos_ == 'ADP' and (doc[c_pt].lemma_ != 'を' or (doc[c_pt].lemma_ == 'を' and len(doc) > c_pt + 1 and doc[c_pt + 1].norm_ == '為る')):
                new_end = c_pt - 1
                break
        verb_word = chunker.compaound(start, new_end, *doc)
        # 補助表現以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic or verb_word in s_v_dic.special_sub_verb_dic:
            # フルマッチ
            for rule in p_rule.sub_phrase_rule:
                if self.rule_check(verb_word, rule["words"]):
                    return True
            # フルマッチでない場合は後方マッチ
            for rule in p_rule.sub_phrase_rule:
                if self.rule_check2(verb_word, rule["words"]):
                    return True
        return False

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
            ok_f = False
            if not chek_predicate["main"] and p_rule != rule:
                ok_f = self.sub_predicate_check(chek_predicate, p_rule, *doc)
            if chek_predicate["main"] or ok_f:
#            if chek_predicate["main"] or p_rule != rule:
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
#                    if re_arg["case"] not in rule.phase_analyze_case and (("副詞的" not in re_arg["case"]) or ("-副詞的" == re_arg["case"])):
                    check_case = re_arg["case"].split("-")[0]
                    if len(check_case) == 1 or (check_case.startswith("に") and check_case != "について") or check_case.startswith("として"):
                        check_case = re_arg["case"]     # に-副詞的 などは対象外
                    if check_case not in rule.phase_analyze_case:
                        continue
                    if "rentai_subject" in re_arg:      # 連体修飾からの主語は対象外
                        continue
                    if not phase:
                        check_end = chek_predicate["lemma_end"]
                        if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を除いてチェック
                            check_end = check_end - 1
                        # 〜こと　は例外で項の先頭を見る
                        if doc[re_arg['lemma_end']].lemma_ == 'こと':
                            sub_phase = ""
                            for check_p in predicate:
                                # 〜こと　の成分の動詞（〜）にかかる句を調べる
                                if check_p["lemma_start"] <= re_arg['lemma_start'] <= check_p["lemma_end"] or check_p["sub_lemma_start"] <= re_arg['lemma_start'] <= check_p["sub_lemma_end"]:
                                    for check_a in argument:
                                        if check_a["predicate_id"] == check_p["id"]:
                                            sub_phase = self.phase_chek(check_p["lemma_start"], check_p["lemma_end"], check_a["lemma_start"], check_a["lemma_end"], '', p_rule, *doc)
                                            pre_phase = sub_phase
                                            if re_arg["subject"]:
                                                koto_f = True
                                            if not sub_phase and chek_predicate["sub_lemma"]:
                                                check_end = chek_predicate["sub_lemma_end"]
                                                if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                                                    check_end = check_end - 1
                                                add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                                                pre_phase = add_phase
                                                for append in add_phase.split(','):  # 重複は登録しない
                                                    if append != '<その他>' and append != '<告知>' and append not in sub_phase:
                                                        if sub_phase:
                                                            sub_phase = phase + ',' + append
                                                        else:
                                                            sub_phase = append
#                            if not phase:
#                                phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                            phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, p_rule, *doc)
                            if not phase:
                                phase = sub_phase
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

        #
        #  マルチラバルをシングルラベルへ
        #

    def single_government_action_get(self, phase, mode):
        rule = GovernmentActionRule()

        ret = ""
        head = []
        if not phase:
            return ret
        if mode == 1:
            head = phase.split(",")
        else:
            head.append("<政府活動>")
            head.append("<日本>")
        if "<募集>" in phase:
            return head[0] + "," + head[1] + "," + "<その他>"
        for check in rule.single_rule:
            for check_label in check["labels"]:
                if check_label in phase:
                    ret = check["single"]
                    for stat in rule.stat_rule:
                        if stat in phase:
                            ret = ret + "," + stat
                    return head[0] + "," + head[1] + "," + ret
        return head[0] + "," + head[1] + "," + "<その他>"

    ##########################################################################################################################################
    #    主述部のフェイズチェック
    #    mode = 1 主語の政府判定あり
    #    mode = 2 主語の政府判定なし
    ##########################################################################################################################################
    government_rule = ["省", "庁", "政府", "内閣"]
    ng_word = ["帰省", "省エネ", "省エネルギー", "省力化", "官公庁", "政府系",
               "黒竜江省", "吉林省", "遼寧省", "河北省", "河南省", "山東省", "山西省", "湖南省", "湖北省", "江蘇省", "安徽省", "浙江省", "福建省", "江西省", "広東省",
               "海南省", "貴州省", "雲南省", "四川省", "陝西省", "青海省", "甘粛省", "台湾省"
               ]

    def government_action_get_and_set(self, predicate, argument, mode, *doc):
        ret_phase = self.government_rule_chek_and_set(predicate, argument, mode, *doc)
        print("%s\n" % ret_phase)
        return self.single_government_action_get(ret_phase, mode)
    def government_rule_chek_and_set(self, predicate, argument, mode, *doc):
        g_a_dic = GovernmentActionRule()
        # 政府発行刊行物？
        if mode == 2:
            ret = self.rule_chek_and_set(predicate, argument, GovernmentActionRule, *doc)
            if ret:
                return "<政府活動>,<日本>," + ret
            else:
                return ""

        # 政府活動かの判断
        government_predicate = []
        is_government = False
        is_government_press = False
        is_government_action = False
        for arg in argument:
            if arg["subject"] or arg["case"] == "で" or arg["case"] == "と" or arg["case"] == "の" or arg["case"] == "から" or arg["case"] == "に" or arg["case"] == "は":
                if "連体" in arg["case"]:
                    continue
                if "から" in arg["lemma"]:
                    continue
                # 主語が政府関係か？
                for check in self.government_rule:
#                    if check in arg["lemma"] or is_government_press:
                    if check in arg["lemma"]:
                        ngw_f = False
                        for ng_w in self.ng_word:
                            if ng_w in arg["lemma"]:
                                ngw_f = True
                                break
                        if not ngw_f:
                            is_government = True
                            if arg["predicate_id"] not in government_predicate:
                                government_predicate.append(arg["predicate_id"])
                                check_w = predicate[arg["predicate_id"]]["lemma"]
                                check_lemma = ""
                                for char in check_w:
                                    if char == '(':
                                        break
                                    check_lemma = check_lemma + char
                                if "こと" in check_lemma:
                                    check_lemma = check_lemma.rstrip("こと")
                                if "している" in check_lemma:
                                    check_lemma = check_lemma.rstrip("している")
                                if "していた" in check_lemma:
                                    check_lemma = check_lemma.rstrip("していた")
                                if "する" in check_lemma:
                                    check_lemma = check_lemma.rstrip("する")
                                if (check_lemma in g_a_dic.kentou_dic or check_lemma in g_a_dic.sekou_dic or
                                        check_lemma in g_a_dic.haishi_dic or
                                        check_lemma in g_a_dic.kaisei_dic or check_lemma in g_a_dic.kunji_dic or
                                        check_lemma in g_a_dic.yousei_dic or check_lemma in g_a_dic.ninka_dic or
                                        check_lemma in g_a_dic.keiyaku_dic or check_lemma in g_a_dic.sosyou_dic or
                                        check_lemma in g_a_dic.kannkoku_dic or check_lemma in g_a_dic.date_dic or
                                        check_lemma in g_a_dic.decision_dic or check_lemma in g_a_dic.action_dic or
                                        check_lemma in g_a_dic.sakusei_dic or check_lemma in g_a_dic.haikei_dic or
                                        check_lemma in g_a_dic.souritsu_dic or check_lemma in g_a_dic.renkei_dic or
                                        check_lemma in g_a_dic.shien_dic or check_lemma in g_a_dic.boshyu_dic or
                                        check_lemma in g_a_dic.yuushi_dic or check_lemma in g_a_dic.kounyuu_dic or
                                        check_lemma in g_a_dic.baikyaku_dic or check_lemma in g_a_dic.kaidan_dic or
                                        check_lemma in g_a_dic.haken_dic or check_lemma in g_a_dic.event_dic):
                                    is_government_action = True
                                if check_lemma in g_a_dic.press_dic:
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
                    if arg["lemma"] == "会議の様子":
                        is_government = True
                        is_government_press = True
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
            sub_gover_ret = ""
            for arg in argument:
#                if arg["predicate_id"] in government_predicate or is_government_press:
                if arg["predicate_id"] in government_predicate and predicate[arg["predicate_id"]]["main"]:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase
                elif arg["predicate_id"] in government_predicate and "phase" in arg:
                    sub_gover_ret = arg["phase"]

            if gover_ret:
                return "<政府活動>,<" + country + ">," + gover_ret
            elif is_government_press:
                if sub_gover_ret:
                    return "<政府活動>,<" + country + ">," + sub_gover_ret
                else:
                    return "<政府活動>,<" + country + ">," + ret
            elif is_government_action and sub_gover_ret:
                return "<企業活動背景>,<" + country + ">," + sub_gover_ret
            elif is_government_action:
                return "<企業活動背景>,<" + country + ">," + ret
            return ""
        elif is_government_action:
            return "<企業活動背景>,<" + country + ">," + "<情報発信>"
        else:
            return ret
