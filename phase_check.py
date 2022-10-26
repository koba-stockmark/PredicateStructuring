from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from phase_rule_dic import PhaseRule
from government_action_dic import GovernmentActionRule

class PhaseCheker:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        self.government_predicate = []
        self.subject_is_government = False
        self.is_government_press = False
        self.is_government_action = False
        self.action_is_haikei = False
        self.lase_predicate_subject_is_government = False

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
        ng_postfix = ["省", "庁", "局"]

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
        if doc[new_end + 1].lemma_ in ng_postfix:
            return ""
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

        # 補助用言以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic or verb_word in s_v_dic.special_sub_verb_dic or verb_word in s_v_dic.information_verb_dic:
            if verb_word in s_v_dic.information_verb_dic:
                return True
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
                    if len(check_case) == 1 or (check_case.startswith("に") and check_case != "について"):
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
    #  どこの国の政府かをチェック
    #########################################################

    country_dic = {"米": "米国", "英": "英国", "中": "中国", "韓": "韓国", "独": "ドイツ", "仏": "フランス", "伊": "イタリア",
                   "加": "カナダ", "印": "インド", "豪": "オーストラリア", "蘭": "オランダ", "朝": "北朝鮮", "西": "スペイン",
                   "台": "台湾", "比": "フィリピン", "露": "ロシア", "香港": "香港", "欧州": "欧州",
                   "州": "米国"}
    ng_country_dic = {"九州", "本州"}

    def country_check(self, argument, predicate, *doc):
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
                    if doc[i].tag_ == "名詞-固有名詞-地名-国" and doc[i + 1].lemma_ != "企業":
                        if predicate_is_main:
                            subject_ari = True
                            country = doc[i].lemma_
                        else:
                            other_country = doc[i].lemma_
                    else:
                        if i != arg["lemma_end"] and len(doc) > i + 1 and doc[i + 1].pos_ != "ADP":
                            if doc[i].lemma_ in self.country_dic and doc[i].lemma_ not in self.ng_country_dic:
                                if predicate_is_main:
                                    subject_ari = True
                                    country = self.country_dic[doc[i].lemma_]
                                else:
                                    other_country = self.country_dic[doc[i].lemma_]
                            else:
                                if doc[i].tag_ == "名詞-固有名詞-地名-一般" and doc[i + 1].lemma_ != "企業" and doc[i].lemma_ not in self.ng_country_dic:
                                    if "州" in doc[i].lemma_:
                                        if predicate_is_main:
                                            subject_ari = True
                                            country = "米国"
                                        else:
                                            other_country = "米国"

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
        return country


    #########################################################
    #  主語が「政府の〇〇」でも政府組織として判断してよいかのチェック
    #########################################################
    ok_no_word = ["研究所", "審議会", "委員会", "部会", "会議", "検討会", "分科会", "機関", "チーム", "機構", "公社", "連盟",
                  "省", "庁", "政府", "内閣", "党", "局", "東京都", "北海道", "大阪府", "京都府", "県",
                  "長官", "幹部", "参与", "長", "次官", "関係者", "司令塔", "職員", "ら", "首相", "大臣",
                  "報告", "調査", "実験", "戦略",
                  "延長", "金"]
    def is_ok_government_subject_chek(self, in_word, case):
        word = in_word
        if "の" in word:
            if case == 'に':     # 「政府の〇〇に」はNG
                return False
            if word.endswith("」") or word.endswith("）") or word.endswith("』") or word.endswith("”"):
                word = word[:-1]
            for check in self.ok_no_word:
                if word.endswith(check):
                    return True
            return False
        else:
            return True

    #########################################################
    #  政府活動か否かをチェック, "政府目標", "政府系"
    #########################################################
    government_rule = ["省", "庁", "政府", "内閣", "党", "東京都", "北海道", "大阪府", "京都府", "県", "委員会", "審議会", "分科会", "部会", "首相", "大臣", "相"]
    ng_word = ["帰省", "省エネ", "省エネルギー", "省力", "省略", "都市", "非政府", "官庁",
               "黒竜江省", "吉林省", "遼寧省", "河北省", "河南省", "山東省", "山西省", "湖南省", "湖北省", "江蘇省", "安徽省", "浙江省", "福建省", "江西省", "広東省",
               "海南省", "貴州省", "雲南省", "四川省", "陝西省", "青海省", "甘粛省", "台湾省",
               "沖", "沿岸", "山間", "東部", "南部", "北部", "西部", "東京電力", "都庁", "道庁", "府庁", "県庁",
               "ファンド", "政府系企業"
               ]
    ng_kakarisaki = ["必要", "重要性", "義務", "責務", "責任"]

    def government_subject_check(self, argument, predicate, *doc):
        self.government_predicate = []
        self.subject_is_government = False
        self.is_government_press = False
        self.is_government_action = False
        self.action_is_haikei = False
        self.lase_predicate_subject_is_government = False
        g_a_dic = GovernmentActionRule()
        c_h = ChunkExtractor()

        for arg in argument:
            is_ok_government_meishi = False
            if arg["subject"] or arg["case"] == "で" or arg["case"] == "と" or arg["case"] == "の" or arg["case"] == "から" or arg["case"] == "に" or arg["case"] == "は" or arg["case"] == "として-副詞的" or arg["case"] == "において-副詞的":
                if "連体" in arg["case"]:
                    continue
                if "から" in arg["lemma"]:
                    continue
                # 主語が政府関係か？
                for check in self.government_rule:
                    if check in arg["lemma"]:
                        ngw_f = False
                        for ng_w in self.ng_word:
                            if ng_w in arg["lemma"]:
                                ngw_f = True
                                break
                        # 並列で政府以外の主語がないか
                        if doc[arg["lemma_end"] + 1].lemma_ != "と" and doc[arg["lemma_end"] + 1].lemma_ != "、":
                            for c_arg in argument:
                                if not c_arg["lemma"].endswith("企業") and c_arg["lemma"] != arg["lemma"] and c_arg["predicate_id"] == arg["predicate_id"] and c_arg["subject"] and arg["subject"]:
                                    if doc[c_arg["lemma_end"] + 1].lemma_ != "と" and doc[c_arg["lemma_end"] + 1].lemma_ != "、":
                                        ngw_f = True
                                        for c_check in self.government_rule:
                                            if c_check in c_arg["lemma"]:
                                                ngw_f = False
                                                for ng_w in self.ng_word:
                                                    if ng_w in c_arg["lemma"]:
                                                        ngw_f = True
                                                        break
                        # 人名かチェック
                        for ac_pt in range(arg["lemma_start"], arg["lemma_end"]):
                            if "人名" in doc[ac_pt].tag_:
                                for check2 in self.government_rule:
                                    if check2 in doc[ac_pt].orth_:
                                        ngw_f = True
                                        break
                                if ngw_f:
                                    break
                        is_ok_government_meishi = False
                        if not ngw_f:
                            is_ok_government_meishi = self.is_ok_government_subject_chek(arg["lemma"], arg["case"])
                        # 「政府の〇〇に...」のチェック
                        if not is_ok_government_meishi and "の" in arg["lemma"]:
                            ok_seifu_no_f = False
                            for check_w in g_a_dic.o_v_houshin_dic["obj"]:
                                if arg["lemma"].endswith(check_w):
                                    ok_seifu_no_f = True
                                    break
                            if not ok_seifu_no_f:
                                continue
                        if not ngw_f:
                            self.subject_is_government = True
                            check_sub_w = predicate[arg["predicate_id"]]["sub_lemma"]
                            check_w = predicate[arg["predicate_id"]]["lemma"]
                            check_lemma = ""
                            if arg["predicate_id"] not in self.government_predicate:
                                # 最後の述部の主語が政府でカテゴリがあるときは背景ではない
#                                if arg["predicate_id"] == predicate[len(predicate) - 1]["id"] and "の" not in arg["lemma"]:
                                if arg["predicate_id"] == predicate[len(predicate) - 1]["id"] and is_ok_government_meishi:
                                    self.lase_predicate_subject_is_government = True
                                bek_f = False
                                for beki_p in range (predicate[arg["predicate_id"]]["lemma_end"] + 1, doc[predicate[arg["predicate_id"]]["lemma_end"]].head.i):
                                    if doc[beki_p].lemma_ == "べし":
                                        bek_f = True
                                        break
                                if bek_f:
                                    continue
                                if "not_direct_subject" not in arg:
                                    self.action_is_haikei = False
                                self.government_predicate.append(arg["predicate_id"])
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
                                    self.is_government_action = True
                                if check_lemma in g_a_dic.press_dic:
                                    self.is_government_press = True
                                if check_sub_w and check_sub_w in g_a_dic.press_dic:
                                    self.is_government_press = True
                                ############################################
                                #  企業活動の背景か否かのチェック
                                ############################################
                                predicate_end = predicate[arg["predicate_id"]]["lemma_end"]
                                if predicate[arg["predicate_id"]]["sub_lemma_end"] != -1:
                                    predicate_end = predicate[arg["predicate_id"]]["sub_lemma_end"]
                                # 政府が発行した〇〇
                                if ((doc[predicate_end].morph.get("Inflection") and '連体形' in doc[predicate_end].morph.get("Inflection")[0]) or c_h.rentai_check(predicate_end, *doc)):
                                    self.action_is_haikei = True
                                    next_p = doc[predicate_end].head.i
                                    if doc[next_p].pos_ == "NOUN":
                                        next_p = c_h.num_chunk(doc[predicate_end].head.i, *doc)["lemma_end"]
                                        if doc[doc[predicate_end].head.i + 1].lemma_ == "の":
                                            next_p = c_h.num_chunk(doc[predicate_end].head.i + 2, *doc)["lemma_end"]
                                        if doc[doc[predicate_end].head.i + 1].lemma_ == "など" and doc[doc[predicate_end].head.i + 2].lemma_ == "の":
                                            next_p = c_h.num_chunk(doc[predicate_end].head.i + 3, *doc)["lemma_end"]

                                    ############# 禁止系　#################################

                                    # 政府が発行した〇〇へ...　は政府活動でも背景でもない
                                    if len(doc) > next_p + 1 and doc[next_p + 1].lemma_ == "へ":
                                        self.subject_is_government = False
                                    # 政府が発行する必要が...　は政府活動でも背景でもない
                                    if doc[next_p].lemma_ in self.ng_kakarisaki:
                                        self.subject_is_government = False

                                    ################　背景 #################################

                                    # 〇〇が形容動詞
                                    if len(doc) > doc[predicate_end].head.i + 1 and doc[doc[predicate_end].head.i].pos_ == "NOUN" and doc[doc[predicate_end].head.i + 1].pos_ == "AUX":
                                        self.action_is_haikei = False
                                    # 〇〇が形容動詞
                                    if len(doc) > predicate_end + 2 and doc[doc[predicate_end + 1].head.i].pos_ == "NOUN" and doc[predicate_end + 2].pos_ == "AUX":
                                        self.action_is_haikei = False
                                    # 〇〇が「ほか」
                                    if doc[predicate_end].head.lemma_ == "ほか":
                                        self.action_is_haikei = False
                                    # 〇〇が「こと」で「こと」のかかり先が情報発信動詞
                                    if doc[predicate_end].head.lemma_ == "こと":
                                        if doc[doc[predicate_end].head.i + 1].orth_ != "で":
                                            check_verb = c_h.verb_chunk(doc[predicate_end].head.head.i, *doc)
                                            if self.rule_check(check_verb["lemma"], g_a_dic.press_dic):
                                                self.action_is_haikei = False
                                    # 〇〇のかかり先が副詞
                                    if doc[predicate_end].head.pos_ == "ADV":
                                        self.action_is_haikei = False
                                    # 〇〇のかかり先が体言止
                                    if doc[next_p].dep_ == "ROOT":
                                        check_verb = c_h.verb_chunk(doc[next_p].i, *doc)
                                        if self.rule_check(check_verb["lemma"], g_a_dic.shoken_dic):
                                            self.action_is_haikei = False
                                        if self.rule_check(check_verb["lemma"], g_a_dic.action_dic):
                                            self.action_is_haikei = False
                                    # 〇〇のかかり先が政府活動述部
                                    if len(doc) > predicate_end + 2:
                                        if self.rule_check(doc[next_p].lemma_, g_a_dic.action_dic) or self.rule_check(doc[next_p].lemma_, g_a_dic.decision_dic):
                                            self.action_is_haikei = False
                                            for c_pt in range(next_p + 1, len(doc)):
                                                if doc[c_pt].pos_ == "ADP":
                                                    if doc[c_pt].lemma_ == "に" or doc[c_pt].lemma_ == "が" or doc[c_pt].lemma_ == "で":
                                                        self.action_is_haikei = True
                                                else:
                                                    break
                                        if doc[next_p].lemma_ != "こと":
                                            for rule in g_a_dic.sub_phrase_rule:
                                                if "words" in rule:
                                                    if doc[doc[next_p].head.i + 1].lemma_ != "の":
                                                        if self.rule_check(doc[next_p].head.lemma_, rule["words"]):
                                                            self.action_is_haikei = False
                                                            break
                                        if doc[next_p].head.lemma_ == "もと":  # 〜をもとに
                                            self.action_is_haikei = True
                                    # 〇〇のかかり先が政府活動オブジェクト
                                    if len(doc) > predicate_end + 2:
                                        if doc[next_p].lemma_ in g_a_dic.o_v_houshin_dic["obj"]:
                                            if self.rule_check(doc[next_p].head.lemma_, g_a_dic.action_dic):
                                                if not c_h.rentai_check(doc[next_p].head.i, *doc):
                                                    self.action_is_haikei = False
                                            for rule in g_a_dic.sub_phrase_rule:
                                                if "words" in rule:
                                                    if self.rule_check(doc[next_p].head.lemma_, rule["words"]):
                                                        if not c_h.rentai_check(doc[next_p].head.i, *doc):
                                                            self.action_is_haikei = False
                                                        break
                                # 政府が〇〇していること
                                elif doc[predicate_end].lemma_ == "こと":
                                    if doc[doc[predicate_end].i + 1].orth_ != "で":
                                        check_verb = c_h.verb_chunk(doc[predicate_end].head.i, *doc)
                                        if self.rule_check(check_verb["lemma"], g_a_dic.press_dic):
                                            self.action_is_haikei = False
                                # 政府が〇〇したこと
                                elif len(doc) > predicate_end + 2 and (doc[predicate_end + 1].lemma_ == "こと" or (doc[predicate_end + 1].lemma_ == "た" and doc[predicate_end + 2].lemma_ == "こと")):
                                    self.action_is_haikei = True
                                # 政府が〇〇できず
                                elif len(doc) > predicate_end + 2 and doc[predicate_end + 1].norm_ == "出来る" and doc[predicate_end + 2].norm_ == "ず":
                                    self.action_is_haikei = True
                                # 政府が〇〇のにあわせる
                                elif doc[predicate_end - 2].norm_ == "の" and doc[predicate_end - 1].norm_ == "に" and doc[predicate_end].norm_ == "合わせる":
                                    self.action_is_haikei = True
                                # 政府が〇〇しても（しており,してから）
                                elif (len(doc) > predicate_end + 2 and (doc[predicate_end + 1].norm_ == "て" or doc[predicate_end + 1].norm_ == "で") and
                                      (doc[predicate_end + 2].norm_ == "も" or doc[predicate_end + 2].norm_ == "おる" or doc[predicate_end + 2].norm_ == "から")):
                                    self.action_is_haikei = True
                                elif (len(doc) > predicate_end + 3 and doc[predicate_end + 1].orth_ == "し" and doc[predicate_end + 2].norm_ == "て" and
                                      (doc[predicate_end + 3].norm_ == "も" or doc[predicate_end + 3].norm_ == "おる" or doc[predicate_end + 3].norm_ == "から")):
                                    self.action_is_haikei = True
                                # 政府が〇〇したが（たなど）
                                elif len(doc) > predicate_end + 2 and (doc[predicate_end + 1].norm_ == "た" or doc[predicate_end + 1].norm_ == "だ") and (doc[predicate_end + 2].norm_ == "が" or doc[predicate_end + 2].norm_ == "など"):
                                    self.action_is_haikei = True
                                elif len(doc) > predicate_end + 3 and doc[predicate_end + 1].lemma_ == "する" and doc[predicate_end + 2].norm_ == "た" and (doc[predicate_end + 3].norm_ == "が" or doc[predicate_end + 3].norm_ == "など"):
                                    self.action_is_haikei = True
                                # 政府が〇〇しているが（しているなど）
                                elif len(doc) > predicate_end + 3 and (doc[predicate_end + 1].norm_ == "て" or doc[predicate_end + 1].norm_ == "で") and doc[predicate_end + 2].lemma_ == "いる" and (doc[predicate_end + 3].norm_ == "が" or doc[predicate_end + 3].norm_ == "など"):
                                    self.action_is_haikei = True
                                elif len(doc) > predicate_end + 4 and doc[predicate_end + 1].lemma_ == "する" and doc[predicate_end + 2].norm_ == "て" and doc[predicate_end + 3].lemma_ == "いる" and (doc[predicate_end + 4].norm_ == "が" or doc[predicate_end + 4].norm_ == "など"):
                                    self.action_is_haikei = True
                                # 政府が〇〇するなど
                                elif len(doc) > predicate_end + 1 and (doc[predicate_end + 1].norm_ == "が" or doc[predicate_end + 1].norm_ == "など"):
                                    self.action_is_haikei = True
                                elif len(doc) > predicate_end + 2 and doc[predicate_end + 1].lemma_ == "する" and (doc[predicate_end + 2].norm_ == "が" or doc[predicate_end + 2].norm_ == "など"):
                                    self.action_is_haikei = True
                                # 政府が〇〇、　連用中止
                                elif (((doc[predicate_end].morph.get("Inflection") and '連用形' in doc[predicate_end].morph.get("Inflection")[0]) or
                                       c_h.renyou_check(predicate_end, *doc)) and
                                      ((len(doc) > doc[predicate_end].head.i + 1 and (doc[doc[predicate_end].i + 1].lemma_ == "、" or doc[doc[predicate_end].i + 1].lemma_ == "「")) or
                                      (len(doc) > doc[predicate_end].head.i + 2 and doc[doc[predicate_end].i + 1].lemma_ == "する" and (doc[doc[predicate_end].i + 2].lemma_ == "、" or doc[doc[predicate_end].i + 2].lemma_ == "「")))):
                                    self.action_is_haikei = True
                                # 政府目標に向ける　（例外処理）
                                elif doc[predicate_end].norm_ == "向ける" and "政府目標" in arg["lemma"]:
                                    self.action_is_haikei = True
                            if not is_ok_government_meishi:
                                self.action_is_haikei = True
#                            elif self.action_is_haikei and len(predicate) - 1 == arg["predicate_id"]:     # 最終述部が政府主語の場合は背景ではない
                            elif self.action_is_haikei and len(predicate) - 1 == arg["predicate_id"] and check_lemma in g_a_dic.press_dic:  # 最終述部が政府主語の場合は背景ではない
                                self.action_is_haikei = False
                            # 政府が〇〇に乗り出す　補助述部で判断するケース
                            elif check_sub_w and check_sub_w in g_a_dic.press_dic:
                                self.action_is_haikei = False
                            break
                if not self.subject_is_government:
                    if arg["lemma"] == "会議の様子":
                        self.subject_is_government = True
                        self.is_government_press = True
        return

    #########################################################
    #  政府活動をマルチラベルでチェック
    #########################################################
    # 政府の背景を表す述部
    haikei_dic = ["後押しする"]

    def government_rule_chek_and_set(self, predicate, argument, mode, *doc):

        # 政府発行刊行物？
        if mode == 2:
            gover_ret = self.rule_chek_and_set(predicate, argument, GovernmentActionRule, *doc)
            # 政府が主語の文は補助述部を使わない
            self.government_subject_check(argument, predicate, *doc)
            if self.subject_is_government:
                gover_ret = ""
                for arg in argument:
                    if predicate[arg["predicate_id"]]["main"]:
                        if "phase" in arg:
                            for check_phase in arg["phase"].split(","):
                                if check_phase not in gover_ret:
                                    if gover_ret:
                                        gover_ret = gover_ret + "," + check_phase
                                    else:
                                        gover_ret = check_phase
            if gover_ret and gover_ret != "<意思決定>":
                return "<政府活動>,<日本>," + gover_ret
            else:
                return ""

        # ニュースが政府活動かの判断
        self.government_subject_check(argument, predicate, *doc)
        if not self.subject_is_government:
            return ""

        # 発信国の判断
        country = self.country_check(argument, predicate, *doc)

        # カテゴリとフェイズをチェック
        ret = self.rule_chek_and_set(predicate, argument, GovernmentActionRule, *doc)

        # 背景判断の例外処理
        last_ok = False
        for ch_arg in argument:
            if ch_arg["predicate_id"] == predicate[len(predicate) - 1]["id"] and "phase" in ch_arg:
                last_ok = True
        if last_ok and self.lase_predicate_subject_is_government:
            self.action_is_haikei = False
        if predicate[len(predicate) - 1]["lemma"] in self.haikei_dic and self.lase_predicate_subject_is_government:
            self.action_is_haikei = True

        houshin_f = False   # 方針が含まれる
        is_main_shisuu = False  # 主述部で指数が述べられている
        if "方針" in ret:
            houshin_f = True
        if ret:
            gover_ret = ""
            # まずはMain述部をチェック
            for arg in argument:
                if (arg["predicate_id"] in self.government_predicate or self.is_government_press) and predicate[arg["predicate_id"]]["main"]:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase == "<指数>":
                                is_main_shisuu = True
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase
            # Main述部から意思決定など以外が見つからない場合は補助述部もチェック
            if self.all_predicate_need_check(gover_ret) or self.action_is_haikei:
                for arg in argument:
                    if "phase" in arg:
                        for check_phase in arg["phase"].split(","):
                            if check_phase not in gover_ret:
                                if gover_ret:
                                    gover_ret = gover_ret + "," + check_phase
                                else:
                                    gover_ret = check_phase

            # 検討と方針の両方がある場合は方針を優先。「方針の検討」を行うと解釈
            if "認可" not in gover_ret and "方針" in gover_ret:
                if "検討" in gover_ret:
                    gover_ret = gover_ret.replace("<検討>", '')
                if "改正" in gover_ret:
                    gover_ret = gover_ret.replace("<改正>", '')
                if "方策内容" in gover_ret:
                    gover_ret = gover_ret.replace("<方策内容>", '')
            if houshin_f and "方針" not in gover_ret:     # 項の存在しない<方針>がある場合は補完する
                gover_ret = gover_ret + ",<方針>"

            if gover_ret and (not self.action_is_haikei or is_main_shisuu):
                return "<政府活動>,<" + country + ">," + gover_ret
            elif self.is_government_press and not self.action_is_haikei:
                return "<政府活動>,<" + country + ">," + ret
#            elif self.is_government_action or self.action_is_haikei:
            elif self.is_government_action or (self.is_government_press and self.action_is_haikei):
                return "<企業活動背景>,<" + country + ">," + ret
            return ""
        elif self.is_government_action:
            if self.action_is_haikei:
                return "<企業活動背景>,<" + country + ">," + "<情報発信>"
            else:
                return "<政府活動>,<" + country + ">," + "<情報発信>"
        else:
            return ret
