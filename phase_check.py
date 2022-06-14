from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from phase_rule_dic import PhaseRule

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

    def phase_chek(self, start, end, obj_start, obj_end, pre_phase, *doc):
        chunker = ChunkExtractor()
        p_rule = PhaseRule()
        s_v_dic = SubVerbDic()
        ret = ''
        verb_word = chunker.compaound(start, end, *doc)
        # 補助表現以外のメイン術部
        if verb_word not in s_v_dic.sub_verb_dic:
            # フルマッチ
            for rule in p_rule.phrase_rule:
                if self.rule_check(verb_word, rule["words"]):
#                if verb_word in rule["words"]:
                    if ret:
                        ret = ret + ',' + rule["label"]
                    else:
                        ret = ret + rule["label"]
            # フルマッチでない場合は後方マッチ
            if not ret:
                for rule in p_rule.phrase_rule:
                    if self.rule_check2(verb_word, rule["words"]):
                        #                if verb_word in rule["words"]:
                        if ret:
                            ret = ret + ',' + rule["label"]
                        else:
                            ret = ret + rule["label"]
        # 目的語からフェーズをチェック
        if verb_word in s_v_dic.sub_verb_dic and obj_start:
#        if(obj_start):
            ret2 = self.phase_chek(obj_start, obj_end, -1, -1, '', *doc)
            # 項全体として重複をチェック
            for ret3 in ret2.split(','):
                if ret3 not in ret:
                    ret = ret + ret3 + ','
            # 項の部分要素を重複をチェック
            for pt in range(obj_start, obj_end + 1):
                ret2 = self.phase_chek(pt, pt, -1, -1, '', *doc)
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

    def phase_get_and_set(self, predicate, argument, *doc):
        rule = PhaseRule()

        phase = ''
        single = ''
        for chek_predicate in predicate:
            if chek_predicate["main"]:
                pre_phase = ''
                for re_arg in argument:
                    phase = ''
                    if chek_predicate["id"] != re_arg["predicate_id"]:
                        continue
                    if not re_arg["case"]:
                        continue
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
                                            phase = self.phase_chek(check_p["lemma_start"], check_p["lemma_end"], check_a["lemma_start"], check_a["lemma_end"], '', *doc)
                                            pre_phase = phase
                                            if not phase and chek_predicate["sub_lemma"]:
                                                check_end = chek_predicate["sub_lemma_end"]
                                                if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                                                    check_end = check_end - 1
                                                add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, *doc)
                                                pre_phase = add_phase
                                                for append in add_phase.split(','):  # 重複は登録しない
                                                    if append != '<その他>' and append != '<告知>' and append not in phase:
                                                        if phase:
                                                            phase = phase + ',' + append
                                                        else:
                                                            phase = append
                            if not phase:
                                phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, *doc)
                        else:
                            phase = self.phase_chek(chek_predicate["lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, *doc)
                        pre_phase = phase
                        if not phase and chek_predicate["sub_lemma"]:
                            check_end = chek_predicate["sub_lemma_end"]
                            if doc[check_end].pos_ == 'AUX':  # 形容動詞の場合は助動詞部分を覗いてチェック
                                check_end = check_end - 1
                            add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], check_end, re_arg['lemma_start'], re_arg['lemma_end'], pre_phase, *doc)
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
                    if phase:   # phaseのある最終術部のphaesをシングルphaseにする
                        single = self.single_phase_get(phase)
        return single
