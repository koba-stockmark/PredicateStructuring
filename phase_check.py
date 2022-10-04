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
            if doc[c_pt].pos_ == 'ADP' and ((doc[c_pt].lemma_ != 'を' and doc[c_pt].lemma_ != 'の' and doc[c_pt].lemma_ != 'が') or (doc[c_pt].lemma_ == 'を' and len(doc) > c_pt + 1 and doc[c_pt + 1].norm_ == '為る')):
                new_end = c_pt - 1
                break
        verb_word = chunker.compaound(start, new_end, *doc)
        obj_word = chunker.compaound(obj_start, obj_end, *doc)
        # O-V　ルール
        if obj_start >= 0:
            for rule in p_rule.phrase_rule:
                if "rule" in rule:
                    verb_ok = False
                    for check_verb in rule["rule"]["verb"]:
                        if check_verb and check_verb in verb_word:
                            verb_ok = True
                            break
                    if verb_ok:
                        for check_obj in rule["rule"]["obj"]:
                            if check_obj and check_obj in obj_word:
                                if ret:
                                    ret = ret + ',' + rule["label"]
                                else:
                                    ret = ret + rule["label"]
                                break

        # 補助表現以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic or verb_word in s_v_dic.special_sub_verb_dic:
        # フルマッチ
            for rule in p_rule.phrase_rule:
                if "words" in rule:
                    if self.rule_check(verb_word, rule["words"]):
                        if ret:
                            ret = ret + ',' + rule["label"]
                        else:
                            ret = ret + rule["label"]
            # フルマッチでない場合は後方マッチ
            if not ret:
                for rule in p_rule.phrase_rule:
                    if "words" in rule:
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
                    ret = ret + ',' + ret3 + ','
            # 項の部分要素を重複をチェック
            for pt in range(obj_start, obj_end + 1):
                if (len(doc) > pt + 1 and (doc[pt + 1].lemma_ == '方' or doc[pt + 1].lemma_ == 'ため')) or (len(doc) > pt + 2 and doc[pt + 1].pos_ == 'AUX' and (doc[pt + 2].lemma_ == '方' or doc[pt + 2].lemma_ == 'ため')):      # 〇〇する方　はフェーズ判断に用いな
                    continue
                ret2 = self.phase_chek(pt, pt, -1, -1, '', p_rule, *doc)
                for ret3 in ret2.split(','):
                    if ret3 not in ret:
                        ret = ret + ',' + ret3 + ','
        # 補助表現がメイン術部のとき
        if not pre_phase and not ret and verb_word in s_v_dic.sub_verb_dic:
            for rule in p_rule.phrase_rule:
                if "words" in rule:
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
    def sub_predicate_check(self, predicate, argument, p_rule, *doc):
        chunker = ChunkExtractor()
        s_v_dic = SubVerbDic()

        if p_rule == PhaseRule:
            return False
        start = predicate["lemma_start"]
        end = predicate["lemma_end"]
        new_end = end
        # かかり先がフェーズ判定語の場合はNG
#        for rule in p_rule.phrase_rule:
#            if "words" in rule:
#                if self.rule_check(doc[doc[end].head.i].lemma_, rule["words"]):
#                    if chunker.rentai_check(doc[end].i, *doc):
#                        return False

        for c_pt in range(start, end):      # 述部の語幹だけを切り出す
            if doc[c_pt].pos_ == 'ADP' and (doc[c_pt].lemma_ != 'を' or (doc[c_pt].lemma_ == 'を' and len(doc) > c_pt + 1 and doc[c_pt + 1].norm_ == '為る')):
                new_end = c_pt - 1
                break
        verb_word = chunker.compaound(start, new_end, *doc)
        # O-V　ルール
        for arg in argument:
            if arg["predicate_id"] == predicate["id"]:
                obj_start = arg["lemma_start"]
                obj_end = arg["lemma_end"]
                obj_word = chunker.compaound(obj_start, obj_end, *doc)
                if obj_start >= 0:
                    for rule in p_rule.phrase_rule:
                        if "rule" in rule:
                            verb_ok = False
                            for check_verb in rule["rule"]["verb"]:
                                if check_verb and check_verb in verb_word:
                                    verb_ok = True
                                    break
                            if verb_ok:
                                for check_obj in rule["rule"]["obj"]:
                                    if check_obj and check_obj in obj_word:
                                        return True

        # 補助表現以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic or verb_word in s_v_dic.special_sub_verb_dic:
            # フルマッチ
            for rule in p_rule.sub_phrase_rule:
                if "words" in rule:
                    if self.rule_check(verb_word, rule["words"]):
                        return True
            # フルマッチでない場合は後方マッチ
            for rule in p_rule.sub_phrase_rule:
                if "words" in rule:
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
            no_argument = True
            ok_f = False
            # 補助述部でもチェック対象にしてよいかチェック
            if not chek_predicate["main"] and p_rule != rule:
                ok_f = self.sub_predicate_check(chek_predicate, argument, p_rule, *doc)
            if chek_predicate["main"] or ok_f:
#            if chek_predicate["main"] or p_rule != rule:
                pre_phase = ''
                koto_f = False
                for re_arg in argument:
                    phase = ''
                    if chek_predicate["id"] != re_arg["predicate_id"]:
                        continue
                    no_argument = False
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
#            if (chek_predicate["main"] or ok_f) and no_argument and not single:
            if (chek_predicate["main"] or ok_f) and no_argument:
                # 項のない述部のチェック
                phase = self.phase_chek(chek_predicate["lemma_start"], chek_predicate["lemma_end"], -1, -1, "", p_rule, *doc)
                if phase:
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
#        if "<募集>" in phase:
#            return head[0] + "," + head[1] + "," + "<その他>"
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
    government_rule = ["省", "庁", "政府", "内閣", "東京都", "北海道", "大阪府", "京都府", "県", "都庁", "道庁", "府庁", "県庁"]
    ng_word = ["帰省", "省エネ", "省エネルギー", "省力化", "政府系", "政府目標", "都市",
               "黒竜江省", "吉林省", "遼寧省", "河北省", "河南省", "山東省", "山西省", "湖南省", "湖北省", "江蘇省", "安徽省", "浙江省", "福建省", "江西省", "広東省",
               "海南省", "貴州省", "雲南省", "四川省", "陝西省", "青海省", "甘粛省", "台湾省"
               ]

    #########################################################
    #  政府活動を法令関係か否かでチェック
    #########################################################

    def government_action_get_and_set(self, predicate, argument, mode, *doc):
        ret_phase = self.government_rule_chek_and_set(predicate, argument, mode, *doc)
        print("%s\n" % ret_phase)
#        return ret_phase
        return self.single_government_action_get(ret_phase, mode)


    #########################################################
    #  Main述部以外のタグも評価するか否かのチェック
    #########################################################
    check_all_predicate = ["<意思決定>", "<方針>", "<検討>", "<アクション>", "<支援>", "<情報公開>", "<所見>"]
    def all_predicate_need_check(self, tags):
        for check_phase in tags.split(","):
            if check_phase not in self.check_all_predicate:
                return False
        return True

    #########################################################
    #  政府活動をマルチラベルでチェック
    #########################################################

    def government_rule_chek_and_set(self, predicate, argument, mode, *doc):
        g_a_dic = GovernmentActionRule()
        c_h = ChunkExtractor()
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
        action_is_haikei = False
        for arg in argument:
            if arg["subject"] or arg["case"] == "で" or arg["case"] == "と" or arg["case"] == "の" or arg["case"] == "から" or arg["case"] == "に" or arg["case"] == "は" or arg["case"] == "として-副詞的":
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
                                ############################################
                                #  企業活動の背景か否かのチェック
                                ############################################
                                # 政府が発行した〇〇
                                if ((doc[predicate[arg["predicate_id"]]["lemma_end"]].morph.get("Inflection") and '連体形' in doc[predicate[arg["predicate_id"]]["lemma_end"]].morph.get("Inflection")[0]) or
                                    c_h.rentai_check(predicate[arg["predicate_id"]]["lemma_end"], *doc)):
                                    action_is_haikei = True
                                    # 〇〇が形容動詞
                                    if len(doc) > predicate[arg["predicate_id"]]["lemma_end"] + 2 and doc[predicate[arg["predicate_id"]]["lemma_end"] + 2].pos_ == "AUX":
                                        action_is_haikei = False
                                    # 〇〇のかかり先が副詞
                                    if doc[predicate[arg["predicate_id"]]["lemma_end"]].head.pos_ == "ADV":
                                        action_is_haikei = False
                                    # 〇〇のかかり先が政府活動述部
                                    if len(doc) > predicate[arg["predicate_id"]]["lemma_end"] + 2:
                                        for rule in g_a_dic.sub_phrase_rule:
                                            if "words" in rule:
                                                if self.rule_check(doc[predicate[arg["predicate_id"]]["lemma_end"] + 1].head.lemma_, rule["words"]):
                                                    action_is_haikei = False
                                                    break
                                                if self.rule_check(doc[predicate[arg["predicate_id"]]["lemma_end"] + 2].head.lemma_,rule["words"]):
                                                    action_is_haikei = False
                                                    break
                                # 政府が〇〇したこと
                                if len(doc) > predicate[arg["predicate_id"]]["lemma_end"] + 2 and (doc[predicate[arg["predicate_id"]]["lemma_end"] + 1].lemma_ == "こと" or (doc[predicate[arg["predicate_id"]]["lemma_end"] + 1].lemma_ == "た" and doc[predicate[arg["predicate_id"]]["lemma_end"] + 2].lemma_ == "こと")):
                                    action_is_haikei = True
                                # 政府が〇〇できず
                                if len(doc) > predicate[arg["predicate_id"]]["lemma_end"] + 2 and doc[predicate[arg["predicate_id"]]["lemma_end"] + 1].norm_ == "出来る" and doc[predicate[arg["predicate_id"]]["lemma_end"] + 2].norm_ == "ず":
                                    action_is_haikei = True
                                # 政府目標に向ける　（例外処理）
                                if doc[predicate[arg["predicate_id"]]["lemma_end"]].norm_ == "向ける" and "政府目標" in arg["lemma"]:
                                    action_is_haikei = True
                            break
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

        houshin_f = False
        is_main_shisuu = False
        ret = self.rule_chek_and_set(predicate, argument, GovernmentActionRule, *doc)
        if "方針" in ret:
            houshin_f = True
        if ret:
            gover_ret = ""
            sub_gover_ret = ""
            # まずはMain述部をチェック
            for arg in argument:
                if (arg["predicate_id"] in government_predicate or is_government_press) and predicate[arg["predicate_id"]]["main"]:
#                if arg["predicate_id"] in government_predicate and predicate[arg["predicate_id"]]["main"]:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase == "<指数>":
                                is_main_shisuu = True
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase
                elif arg["predicate_id"] in government_predicate and "phase" in arg:
                    sub_gover_ret = arg["phase"]
            # Main述部から意思決定など以外が見つからない場合は補助述部もチェック
            if self.all_predicate_need_check(gover_ret) or action_is_haikei:
                for arg in argument:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase

#            # 意思決定のみ場合は他の述部から意思決定の内容があるかを探す
#            if "<意思決定>" == gover_ret:
#                new_gover_ret = ""
#                for arg in argument:
#                    if "phase" in arg:
#                        for check_phase in arg["phase"].split(","):
#                            if check_phase not in new_gover_ret:
#                                if new_gover_ret:
#                                    new_gover_ret = new_gover_ret + "," + check_phase
#                                else:
#                                    new_gover_ret = check_phase
#                if new_gover_ret:
#                    gover_ret = new_gover_ret
            # 検討と方針の両方がある場合は方針を優先。「方針の検討」を行うと解釈
            if "検討" in gover_ret and "方針" in gover_ret:
                gover_ret = gover_ret.replace("<検討>", '')
            if houshin_f and "方針" not in gover_ret:     # 項の存在しない<方針>がある場合は補完する
                gover_ret = gover_ret + ",<方針>"

            if gover_ret and (not action_is_haikei or is_main_shisuu):
#            if gover_ret and not action_is_haikei:
                    return "<政府活動>,<" + country + ">," + gover_ret
            elif is_government_press and not action_is_haikei:
                if sub_gover_ret:
                    return "<政府活動>,<" + country + ">," + sub_gover_ret
                else:
                    return "<政府活動>,<" + country + ">," + ret
            elif is_government_action and sub_gover_ret:
                return "<企業活動背景>,<" + country + ">," + sub_gover_ret
            elif is_government_action or action_is_haikei:
                return "<企業活動背景>,<" + country + ">," + ret
            return ""
        elif is_government_action:
            if action_is_haikei:
                return "<企業活動背景>,<" + country + ">," + "<情報発信>"
            else:
                return "<政府活動>,<" + country + ">," + "<情報発信>"
        else:
            return ret
