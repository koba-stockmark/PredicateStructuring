class DataDumpSave:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


    """
    解析結果のダンプとセーブ
    """

    def data_dump_and_save(self, text, argument, predicate, id):
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
            if not subj['subject'] and subj["predicate_id"] == id:
                subject_only = False
        for subj in argument:
            if subj['subject'] and subj["predicate_id"] == id:
                subj_f = True
                if subj['dummy'] and subj["predicate_id"] == id:
                    dummy_subject = subj["lemma"]
                    subject_case = subj["case"]
                else:
                    subject_w = subj["lemma"]
                    subject_case = subj["case"]
                # 見つけた主語ごとに他を展開
                for data in argument:
                    if data["predicate_id"] != id:
                        continue
                    if not subject_only and data['subject']:
                        continue
                    obj_w = data["lemma"]
                    if subject_only:
                        obj_w = ''
                        continue    # デバック用に主語だけのものは表示しない
                    case = data["case"]

                    if dummy_subject:
                        print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, dummy_subject, modal, rule_id))
                        ret = ret + text + '\tー\t' + dummy_subject + '(省略)\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, subject_w, modal, rule_id))
                        ret = ret + text + '\tー\t' + subject_w + '\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
            else:
                continue
        if not subj_f:
            for data in argument:
                if data["predicate_id"] != id:
                    continue
                obj_w = data["lemma"]
                case = data["case"]
                if dummy_subject and data["predicate_id"] == id:
                    print('all = 【%s(%s) - %s】 subj = 【%s (省略)】 modality = %s rule_id = %d' % (obj_w, case, verb_w, dummy_subject, modal, rule_id))
                    ret = ret + text + '\tー\t' + dummy_subject + '(省略)\t'  + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                else:
                    print('all = 【%s(%s) - %s】 subj = 【%s】 modality = %s rule_id = %d' % (obj_w, case, verb_w, subject_w, modal, rule_id))
                    ret = ret + text + '\tー\t' + subject_w + '\t' + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
        return ret

    def data_dump_and_save2(self, text, argument, predicate):

        ret = ''
        subject_w = ''
        subject_case = ''
        dummy_subject = ''

        for chek_predicate in predicate:
            if chek_predicate["main"]:
                subj_f = False
                all_subject = True
                verb_w = chek_predicate["lemma"]
                sub_verb_w = chek_predicate["sub_lemma"]
                rule_id = chek_predicate["rule_id"]
                if chek_predicate["main_rule_id"]:
                    rule_id = chek_predicate["main_rule_id"]
                modality_w = chek_predicate["modality"]
                modal = ', '.join([str(x) for x in modality_w])

                for subj in argument:
                    if not subj['subject'] and chek_predicate["id"] == subj["predicate_id"]:
                        all_subject = False
                for subj in argument:
                    if subj['subject'] and chek_predicate["id"] == subj["predicate_id"]:
                        phase = ""
                        subj_f = True
                        if subj['dummy'] and chek_predicate["id"] == subj["predicate_id"]:
                            dummy_subject = subj["lemma"]
                            subject_case = subj["case"]
                        else:
                            subject_w = subj["lemma"]
                            subject_case = subj["case"]
                        if "phase" in subj:
                            phase = subj["phase"]
                        if "category" in subj:
                            phase = subj["category"]
                        for data in argument:
                            if chek_predicate["id"] != data["predicate_id"]:
                                continue
                            if not all_subject and data['subject']:
                                continue
                            obj_w = data["lemma"]
                            if all_subject:
                                obj_w = ''
                                if subject_w != data["lemma"]:
                                    continue
                            case = data["case"]
                            if "phase" in data and data["phase"] not in phase:
                                phase = phase + data["phase"]
                            if "category" in data and data["category"] not in phase:
                                if "," in data["category"] and phase:
                                    for add in data["category"].split(","):
                                        if add not in phase:
                                            phase = phase + "," + add
                                else:
                                    if phase:
                                        phase = phase + "," + data["category"]
                                    else:
                                        phase = data["category"]
                            if dummy_subject:
                                print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, dummy_subject, phase, modal, rule_id))
                                ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                            else:
                                print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, subject_w, phase, modal, rule_id))
                                ret = ret + text + '\tMain\t' + subject_w + '\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                    else:
                        continue
                if not subj_f:
                    phase = ""
                    for data in argument:
                        if chek_predicate["id"] != data["predicate_id"]:
                            continue
                        obj_w = data["lemma"]
                        case = data["case"]
                        phase = ""
                        if "category" in chek_predicate:
                            phase = chek_predicate["category"]
                        if "phase" in data:
                            phase = data["phase"]
                        if "category" in data:
                            phase = data["category"]
                        if dummy_subject:
                            print('【%s(%s) - %s - (%s)】 subj = 【%s(省略)】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, dummy_subject, phase, modal, rule_id))
                            ret = ret + text + '\tMain\t' + dummy_subject + '(省略)\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
                        else:
                            print('【%s(%s) - %s - (%s)】 subj = 【%s】 フェーズ = 【%s】modality = %s rule_id = %d' % (obj_w, case, verb_w, sub_verb_w, subject_w, phase, modal, rule_id))
                            ret = ret + text + '\tMain\t' + subject_w + '\t' + subject_case + "\t" + obj_w + '\t' + case + '\t' + verb_w + '\t' + sub_verb_w + '\t' + phase + '\t' + modal + '\t' + str(rule_id) + '\n'
        return ret

    def data_dump_and_save3(self, text, argument, predicate):
        ret = ''
        print(text)

        for predic in predicate:
            modality_w = predic["modality"]
            modal = ', '.join([str(x) for x in modality_w])
            category_w = ""
            if "category" in predic:
                category_w = predic["category"]
            if predic["main"]:
                if "main_rule_id" in predic:
                    print("ID = %d 【%s - (%s) 】 modality = %s  category = %s ruleID = %d\t main_ruleID= %d" % (predic["id"], predic["lemma"], predic["sub_lemma"], modal, category_w, predic["rule_id"], predic["main_rule_id"]))
                    predic_ret = predic["lemma"] + '\t' + predic["sub_lemma"] + '\t' + modal + '\t' + str(predic["rule_id"]) + '\t' + str(predic["main_rule_id"]) + '\t'
                else:
                    print("ID = %d 【%s - (%s) 】 modality = %s  category = %s ruleID = %d\t main_ruleID= " % (predic["id"], predic["lemma"], predic["sub_lemma"], modal, category_w, predic["rule_id"]))
                    predic_ret = predic["lemma"] + '\t' + predic["sub_lemma"] + '\t' + modal + '\t' + str(predic["rule_id"]) + '\t' + '\t'
            else:
                if "main_rule_id" in predic:
                    print("ID = %d sub_【%s - (%s) 】 modality = %s  category = %s ruleID = %d\t main_ruleID= %d" % (predic["id"], predic["lemma"], predic["sub_lemma"], modal, category_w, predic["rule_id"],predic["main_rule_id"]))
                    predic_ret = predic["lemma"] + '\t' + predic["sub_lemma"] + '\t' + modal + '\t' + str(predic["rule_id"]) + '\t' + str(predic["main_rule_id"]) + '\t'
                else:
                    print("ID = %d sub_【%s - (%s) 】 modality = %s  category = %s ruleID = %d\t main_ruleID= " % (predic["id"], predic["lemma"], predic["sub_lemma"], modal, category_w, predic["rule_id"]))
                    predic_ret = predic["lemma"] + '\t' + predic["sub_lemma"] + '\t' + modal + '\t' + str(predic["rule_id"]) + '\t' + '\t'
            ret_subj = "\t"
            subject_only = 0
            subjects = []
            for a_id, arg in enumerate(argument):
                if predic["id"] == arg["predicate_id"]:
                    if arg["subject"]:
                        ret_subj = arg["lemma"] + "\t" + arg["case"]
                        subjects.append(ret_subj)
                        if subject_only != 2:
                            subject_only = 1
                    else:
                        subject_only = 2
            for a_id, arg in enumerate(argument):
                if predic["id"] == arg["predicate_id"]:
                    phase = ''
                    if "phase" in arg:
                        phase = arg["phase"]
                    if "category" in arg:
                        phase = arg["category"]
                    if arg["subject"]:
                        print("\tID = %d %s(%s)_主語 phase = %s" % (a_id, arg["lemma"], arg["case"], phase))
                        if subject_only == 1:
                            if predic["main"]:
                                ret = ret + text + "\t" + str(predic["id"]) + '\t' + 'Main' + '\t' + arg["lemma"] + "\t" + arg["case"] +  '\t\t\t' + predic_ret + phase + "\n"
                            else:
                                ret = ret + text + "\t" + str(predic["id"]) + '\t' + "ー" + '\t' + arg["lemma"] + "\t" + arg["case"] + '\t\t\t' + predic_ret + phase + "\n"
                    else:
                        print("\tID = %d %s(%s) phase = %s" % (a_id, arg["lemma"], arg["case"], phase))
                        if subjects:
                            for ret_subject in subjects:
                                if predic["main"]:
                                    ret = ret + text + "\t" + str(predic["id"]) + '\t' + 'Main' + '\t' + ret_subject + "\t" + arg["lemma"] + "\t" + arg["case"] + '\t' + predic_ret + phase + "\n"
                                else:
                                    ret = ret + text + "\t" + str(predic["id"]) + '\t' + "ー" + '\t' + ret_subject + "\t" + arg["lemma"] + "\t" + arg["case"] + '\t' + predic_ret + phase + "\n"
                        else:
                            if predic["main"]:
                                ret = ret + text + "\t" + str(predic["id"]) + '\t' + 'Main' + '\t' + "\t" + "\t" + arg["lemma"] + "\t" + arg["case"] + '\t' + predic_ret + phase + "\n"
                            else:
                                ret = ret + text + "\t" + str(predic["id"]) + '\t' + "ー" + "\t" + '\t' + "\t" + arg["lemma"] + "\t" + arg["case"] + '\t' + predic_ret + phase + "\n"
        return ret

    def data_dump_and_save4(self, text, argument, predicate):
        print(text)
        ret = text + "\n"
        for predic in predicate:
            if predic["main"]:
                if "main_rule_id" in predic:
                    print("ID = %d 【%s - (%s) 】 modality = %s ruleID = %d\t main_ruleID= %d" % (
                    predic["id"], predic["lemma"], predic["sub_lemma"], predic["modality"], predic["rule_id"],
                    predic["main_rule_id"]))
                    ret = ret + "\t" + str(predic["id"]) + '\t' + 'Main\t' + predic["lemma"] + '\t' + predic[
                        "sub_lemma"] + '\t\t\t\t\t' + predic["modality"] + '\t' + str(predic["rule_id"]) + '\t' + str(
                        predic["main_rule_id"]) + '\n'
                else:
                    print("ID = %d 【%s - (%s) 】 modality = %s ruleID = %d\t main_ruleID= " % (
                    predic["id"], predic["lemma"], predic["sub_lemma"], predic["modality"], predic["rule_id"]))
                    ret = ret + "\t" + str(predic["id"]) + '\t' + 'Main\t' + predic["lemma"] + '\t' + predic[
                        "sub_lemma"] + '\t\t\t\t\t' + predic["modality"] + '\t' + str(predic["rule_id"]) + '\t' + '\n'
            else:
                if "main_rule_id" in predic:
                    print("ID = %d sub_【%s - (%s) 】 modality = %s ruleID = %d\t main_ruleID= %d" % (
                    predic["id"], predic["lemma"], predic["sub_lemma"], predic["modality"], predic["rule_id"],
                    predic["main_rule_id"]))
                    ret = ret + "\t" + str(predic["id"]) + '\t' + '\t' + predic["lemma"] + '\t' + predic[
                        "sub_lemma"] + '\t\t\t\t\t' + predic["modality"] + '\t' + str(predic["rule_id"]) + '\t' + str(
                        predic["main_rule_id"]) + '\n'
                else:
                    print("ID = %d sub_【%s - (%s) 】 modality = %s ruleID = %d\t main_ruleID= " % (
                    predic["id"], predic["lemma"], predic["sub_lemma"], predic["modality"], predic["rule_id"]))
                    ret = ret + "\t" + str(predic["id"]) + '\t' + '\t' + predic["lemma"] + '\t' + predic[
                        "sub_lemma"] + '\t\t\t\t\t' + predic["modality"] + '\t' + str(predic["rule_id"]) + '\t' + '\n'
            for a_id, arg in enumerate(argument):
                if predic["id"] == arg["predicate_id"]:
                    phase = ''
                    if "phase" in arg:
                        phase = arg["phase"]
                    if "category" in arg:
                        phase = arg["category"]
                    if arg["subject"]:
                        print("\tID = %d %s(%s)_主語 phase = %s" % (a_id, arg["lemma"], arg["case"], phase))
                        ret = ret + "\t\t\t\t\t" + arg["case"] + "\t主語\t" + arg["lemma"] + phase + "\n"
                    else:
                        print("\tID = %d %s(%s) phase = %s" % (a_id, arg["lemma"], arg["case"], phase))
                        ret = ret + "\t\t\t\t\t" + arg["case"] + "\t\t" + arg["lemma"] + phase + "\n"
        return ret

    def text_treace(self, *doc):
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
