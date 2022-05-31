class DataDumpSave:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


    """
    解析結果のダンプとセーブ
    """

    def data_dump_and_save(self, text, argument, predicate):
        ret = ''
        subject_w = ''
        dummy_subject = ''
        verb_w = predicate["lemma"]
        rule_id = predicate["rule_id"]
        modality_w = predicate["modality"]
        modal = ', '.join([str(x) for x in modality_w])
        phase = ''
        subj_f = False
        print(text)
        subject_only = True
        for subj in argument:
            if not subj['subject']:
                subject_only = False
        for subj in argument:
            if subj['subject']:
                subj_f = True
                if subj['dummy']:
                    dummy_subject = subj["lemma"]
                else:
                    subject_w = subj["lemma"]
                # 見つけた主語ごとに他を展開
                for data in argument:
                    if not subject_only and data['subject']:
                        continue
                    obj_w = data["lemma"]
                    if subject_only:
                        obj_w = ''
                        continue    # デバック用に主語だけのものは表示しない
                    case = data["case"]

                    if dummy_subject:
                        print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, dummy_subject, modal, rule_id))
                        ret = ret + text + '\t\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, subject_w, modal, rule_id))
                        ret = ret + text + '\t\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
            else:
                continue
        if not subj_f:
            for data in argument:
                obj_w = data["lemma"]
                case = data["case"]
                if dummy_subject:
                    print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, dummy_subject, modal, rule_id))
                    ret = ret + text + '\t\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                else:
                    print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, subject_w, modal, rule_id))
                    ret = ret + text + '\t\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
        return ret

    def data_dump_and_save2(self, text, argument, predicate):

        ret = ''
        subject_w = ''
        dummy_subject = ''
        verb_w = predicate["lemma"]
        sub_verb_w = predicate["sub_lemma"]
        rule_id = predicate["rule_id"]
        modality_w = predicate["modality"]
        modal = ', '.join([str(x) for x in modality_w])
        subj_f = False
        all_subject = True

        for subj in argument:
            if not subj['subject']:
                all_subject = False
        for subj in argument:
            if subj['subject']:
                subj_f = True
                if subj['dummy']:
                    dummy_subject = subj["lemma"]
                else:
                    subject_w = subj["lemma"]
                for data in argument:
                    if not all_subject and data['subject']:
                        continue
                    obj_w = data["lemma"]
                    if all_subject:
                        obj_w = ''
                    case = data["case"]
                    phase = data["phase"]

                    if dummy_subject:
                        print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, dummy_subject, phase, modal, rule_id))
                        ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, subject_w, phase, modal, rule_id))
                        ret = ret + text + '\tMain\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
            else:
                continue
        if not subj_f:
            for data in argument:
                obj_w = data["lemma"]
                case = data["case"]
                phase = data["phase"]
                if dummy_subject:
                    print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, dummy_subject, phase, modal, rule_id))
                    ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                else:
                    print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, subject_w, phase, modal, rule_id))
                    ret = ret + text + '\tMain\t' + subject_w + '\t' + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
        return ret


