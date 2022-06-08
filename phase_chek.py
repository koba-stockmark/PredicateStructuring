from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from phase_rule_dic import PhaseRule

class PhaseCheker:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

    def phase_chek(self, start, end, obj_start, obj_end, *doc):
        chunker = ChunkExtractor()
        rule = PhaseRule()
        s_v_dic = SubVerbDic()
        ret = ''
        verb_word = chunker.compaound(start, end, *doc)
        # メイン術部
        if verb_word not in s_v_dic.sub_verb_dic:
            for rule in rule.phrase_rule:
                if verb_word in rule["words"]:
                    if ret:
                        ret = ret + ',' + rule["label"]
                    else:
                        ret = ret + rule["label"]
        # 目的語からフェーズをチェック
        if(verb_word in s_v_dic.sub_verb_dic and obj_start):
#        if(obj_start):
            ret2 = self.phase_chek(obj_start, obj_end, '', '', *doc)
            # 項全体としてチェック
            for ret3 in ret2.split(','):
                if ret3 not in ret:
                    ret = ret + ret3 + ','
            # 項の部分要素をチェック
            for pt in range(obj_start, obj_end + 1):
                ret2 = self.phase_chek(pt, pt, '', '', *doc)
                for ret3 in ret2.split(','):
                    if ret3 not in ret:
                        ret = ret + ret3 + ','
        # 補助表現がメイン術部のとき
        if not ret and verb_word in s_v_dic.sub_verb_dic:
            for rule in rule.phrase_rule:
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

        for chek in rule.single_rule:
            if phase in chek["labels"]:
                return chek["single"]
        return ''


    ##########################################################################################################################################
    #    主述部のフェイズチェック
    ##########################################################################################################################################

    def phase_get_and_set(self, predicate, argument, *doc):
        phase = ''
        single = ''
        for chek_predicate in predicate:
            if chek_predicate["main"]:
                phase = ''
                for re_arg in argument:
                    if chek_predicate["id"] != re_arg["predicate_id"]:
                        continue
                    if not re_arg["case"]:
                        continue
                    if "rentai_subject" in re_arg:
                        continue
                    if re_arg["subject"]:
                        continue
#                        all_subject = True
#                        for chek_arg in argument:
#                            if chek_arg["predicate_id"] == re_arg["predicate_id"] and not chek_arg["subject"]:
#                                all_subject = False
#                        if not all_subject:     # 主語以外の項がある場合は主語によるフェーズのチェックをしない
#                            continue
                    if not phase:
                        phase = self.phase_chek(chek_predicate["lemma_start"], chek_predicate["lemma_end"], re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                        if not phase and chek_predicate["sub_lemma"]:
                            add_phase = self.phase_chek(chek_predicate["sub_lemma_start"], chek_predicate["sub_lemma_end"],re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                            for append in add_phase.split(','):  # 重複は登録しない
                                if append != '<その他>' and append != '<告知>' and append not in phase:
                                    if phase:
                                        phase = phase + ',' + append
                                    else:
                                        phase = append
                    re_arg["phase"] = phase
                    if phase:   # phaseのある最終術部のphaesをシングルphaseにする
                        single = self.single_phase_get(phase)
        return single
