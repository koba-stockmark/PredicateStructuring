#                """
# 複合動詞の場合、複合動詞間のかかり受けがあるのでそれを排除して最終かかり先を求める
predic_head = token.i
if token.pos_ == 'VERB':
    comp_verb = self.verb_chunk(doc[token.i].i, *doc)
    for i in range(comp_verb['lemma_start'], comp_verb['lemma_end']):
        if predic_head < doc[i].head.i:
            predic_head = doc[i].head.i
#
# 述部が最終述部の場合
#
if (doc[predic_head].i == doc[predic_head].head.i and (
        doc[predic_head].pos_ == "VERB" or doc[predic_head].pos_ == "ADV") or  # 最後の動詞？　注)普通名詞のサ変名詞利用の場合はADVになっている
        (doc_len > doc[predic_head].i + 1 and (
                doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[
            doc[predic_head].i + 1].lemma_ == 'する'))):  # 普通名詞　＋　する が文末の場合
    rule_id = 100
    main_verb = True
    #
    #           〇〇したと〇〇した　（一時停止したと明らかにした）
    #           誤解析により補助術部に対して目的語がかかっている場合の処理
    #
    if doc_len > i + 3 and (
            doc[i + 2].head.i == doc[predic_head].i and doc[i + 2].pos_ == 'VERB' and doc[i + 3].lemma_ == "する"):
        verb_w = doc[i + 2].lemma_ + doc[i + 3].lemma_
        rule_id = 101
#
# 最終述部でない場合 (最終術部が補助術部かを判断して補助術部の場合は最終術部でなくても主述部として扱う)
#
elif (doc[doc[predic_head].i].pos_ == "VERB" and doc[doc[predic_head].i].head.i == doc[
    doc[predic_head].i].head.head.i and doc[doc[predic_head].i].head.pos_ == "VERB"):  # 最後の動詞を修飾する動詞？
    if (doc[doc[predic_head].i].head.lemma_ == 'する' and doc[doc[doc[predic_head].i].head.i - 1].pos_ != 'ADP' and verb[
        "lemma_end"] != predic_head):  # かかり先の動詞が　○○をする　ではなく　単独の動詞か○○する
        if (doc[doc[predic_head].i + 1].lemma_ == 'する'):
            verb_w = doc[predic_head].lemma_ + doc[doc[predic_head].i + 1].lemma_
        else:
            verb_w = doc[predic_head].lemma_
        verb["lemma"] = verb_w
        verb["lemma_start"] = predic_head
        verb["lemma_end"] = predic_head
        rule_id = 102
        main_verb = True
    else:
        rule_id = 103
        main_verb = True
#
#  最終術部が名詞から形成される場合
#
elif (doc[predic_head].head.head.lemma_ == "する" and doc[
    doc[predic_head].i + 1].lemma_ == '決定'):  # 文末が　〇〇をする　の例外処理（サ変名詞による補助用言相当の処理）
    verb_w = doc[predic_head].lemma_
    rule_id = 104
    main_verb = True
elif doc[predic_head].pos_ == 'NOUN' and doc[predic_head].dep_ == 'ROOT' and doc[predic_head].i == \
        doc[predic_head].head.i:  # 文末が　体言止
    rule_id = 105
    main_verb = True
elif doc[predic_head].head.pos_ == 'NOUN' and doc[predic_head].head.dep_ == 'ROOT' and doc[
    predic_head].head.i == doc[doc[predic_head].head.i].head.i:  # 文末が　体言止
    rule_id = 107
    main_verb = True
elif next_head_use and doc[doc[predic_head].head.i + 1].lemma_ == "する":
    rule_id = 106
    main_verb = True
