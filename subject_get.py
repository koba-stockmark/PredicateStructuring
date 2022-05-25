from chunker import ChunkExtractor

class SubjectExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.head_connect_check = chunker.head_connect_check
        self.connect_word = chunker.connect_word


    """
    名詞＋動詞　の連体形の判別
    """
    def rentai_check(self, pt , *doc):
        find = False
        for cpt in range(pt + 1, doc[pt].head.i):
            if(doc[cpt].pos_ != 'AUX' and doc[cpt].pos_ != 'VERB' and doc[cpt].pos_ != 'SCONJ'):
                break
            if doc[cpt].morph.get("Inflection") and '連体形' in doc[cpt].morph.get("Inflection")[0]:
                find = True
        return find

    """
    名詞＋動詞　の終止形の判別
    """
    def shuusi_check(self, pt , *doc):
        find = False
        for cpt in range(pt + 1, doc[pt].head.i):
            if(doc[cpt].pos_ != 'AUX' and doc[cpt].pos_ != 'VERB' and doc[cpt].pos_ != 'SCONJ'):
                break
            if doc[cpt].morph.get("Inflection") and '終止形' in doc[cpt].morph.get("Inflection")[0]:
                find = True
        return find

    campany_special_vaerb = [
        'ある', 'おこなう', 'かかげる', 'かまえる', 'けん引', 'コンセプトと', 'コンセプトに', 'コントローラーに','コントロール',
        'サポート', 'する', 'する', 'セットに', 'テーマに', 'ミッションと', 'ライトアップ','リード',
        '運営', '営む', '遠隔管理', '応援', '解決', '開業', '開催', '開始','開発・運営', '開発・提供', '開発・販売', '成長',
        '開発', '活用', '管理', '企画・開発','企画販売', '協賛', '強みと', '強化', '掲げる', '掲載', '経営', '公開',
        '構える','構築', '行う', '行なう', '採用', '支援', '実現', '実行', '主力と', '取り扱う', '手がける','手掛ける',
        '手伝い', '集める', '承る', '称', '進める', '図る', '推進', '生産', '製造・販売','製造', '製造販売', '説明',
        '洗浄', '全国展開', '促進', '続ける', '担う', '置く','中心と', '提案', '提供', '展開', '得意と', '届ける','入れる',
        '発行', '発信', '発売','発売', '発表', '販売', '販売開始', '務める', '目指す', '利用', '理念と', '立ち上げる', '抱える'
    ]

    #
    #   直接つながる主語をサーチ
    #
    def direct_connect_chek(self, pt, *doc):
        ret = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        ret_subj = self.num_chunk(doc[pt].i, *doc)
        if doc[pt].i > 0 and '名詞-固有名詞-地名' in doc[pt].tag_ and doc[doc[pt].i - 1].pos_ == 'NOUN':  # NPO法人ラ・レーチェ・リーグ日本は　など地名がわかれる場合の処理
            append_subj = self.num_chunk(doc[pt].i - 1, *doc)
            ret_subj['lemma'] = append_subj['lemma'] + ret_subj['lemma']
            ret_subj['lemma_start'] = append_subj['lemma_start']
        ret['lemma_end'] = ret_subj['lemma_end']
        for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
            if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                break
            ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
            ret['lemma_start'] = i
        return ret

    #
    #   間接的につながる主語をサーチ
    #
    def relational_connect_check(self, pt, ng_pt, verb_pt, *doc):
        ret = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        chek = doc[pt].head.i
        while chek != doc[chek].head.i:  # 主語の候補がが見つかったら述部につながるかパスをたどる
            if chek == verb_pt:
                break
            else:
                if doc[chek].dep_ == 'nsubj':  # 他の主語が見つかったらそちらを優先
                    break
                if (doc[doc[chek].i + 1].tag_ == '形状詞-助動詞語幹' and doc[doc[chek].i + 1].head.i == doc[doc[chek].i].i):
                    break
                if doc[chek].lemma_ != '運営' and doc[chek].lemma_ != '提携' and doc[chek].head.lemma_ != 'ほか':
                    if ((doc[chek].morph.get("Inflection") and '連体形' in doc[chek].morph.get("Inflection")[0]) or
                            (doc[chek + 1].pos_ == 'AUX' and doc[chek + 1].morph.get("Inflection") and '連体形' in doc[chek + 1].morph.get("Inflection")[0]) or
                            (doc[chek + 1].pos_ == 'AUX' and doc[chek + 2].pos_ == 'AUX' and doc[chek + 2].morph.get("Inflection") and '連体形' in doc[chek + 2].morph.get("Inflection")[0])):
                        break
                    if self.rentai_check(chek, *doc):
                        if doc[doc[chek].head.i].lemma_ != 'こと':
                            break
                if (doc[chek + 1].orth_ == 'さ' and doc[chek + 2].lemma_ == 'れる' and doc[chek + 3].lemma_ == 'た'):
                    break
                if (doc[chek].pos_ == 'NOUN' and doc[chek - 1].orth_ == 'が' and doc[chek + 1].orth_ == 'で'):  # 〜が理由で…
                    break
                if (doc[chek].norm_ == '成る' and doc[chek - 1].orth_ == 'に'):  # 〜が〜になる〜する…
                    break
                if doc[chek].pos_ == 'ADJ':
                    break
#                if chek == obj_point:    # obj は主語にならない
#                    break
                chek = doc[chek].head.i
#        if doc[pt].i != ng_pt and (chek == verb_pt or chek == doc[verb_pt].head.i or (chek == doc[verb_pt].head.head.i and doc[verb_pt].head.head.i < verb_pt + 4)):
        if doc[pt].i != ng_pt and (chek == verb_pt or chek == doc[verb_pt].head.i or chek == doc[verb_pt].head.head.i):
            ret_subj = self.num_chunk(doc[pt].i, *doc)
            if pt > 0 and '名詞-固有名詞-地名' in doc[pt].tag_ and doc[doc[pt].i - 1].pos_ == 'NOUN':  # NPO法人ラ・レーチェ・リーグ日本は　など地名がわかれる場合の処理
                append_subj = self.num_chunk(pt - 1, *doc)
                ret_subj['lemma'] = append_subj['lemma'] + ret_subj['lemma']
                ret_subj['lemma_start'] = append_subj['lemma_start']
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['lemma_start'] = i
            return ret
        return ret

    """
        目的語に対する主語の取得
        目的語のかかり先の動詞にかかる主語を探す
        〇〇と〇〇　のような並列は分割してひとつだけを返す。
        見つからないときは　連体修飾　「△△△をする〇〇(主語)は、」　のような形式からも探す　
        
        in: 目的語ID
        return : 主語文字列　始点ノードID　終点ノードID
    """
    def subject_get_from_object(self, obj_point, *doc):
        ret = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        ng_pt = obj_point
        verb_pt = doc[obj_point].head.i
        return self.subject_get_from_object2(verb_pt, ng_pt, *doc)

    def subject_get_from_object2(self, verb_pt, verb_end_pt, *doc):
        ng_pt = verb_pt
        ret = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # subjで直接接続をチェック
        for token in doc:
            if (token.dep_ == "nsubj" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能')):
                return self.direct_connect_chek(token.i, *doc)
        # subjで間接接続をチェック
        for i in range(0, verb_pt):
            if ((doc[i].dep_ == "nsubj" and doc[i].tag_ != '名詞-普通名詞-副詞可能') or
                 (len(doc) > i + 2 and doc[i].dep_ == "obl" and doc[i].tag_ != '名詞-普通名詞-副詞可能' and doc[i + 1].lemma_ == 'など' and (doc[i + 2].lemma_ == 'は' or doc[i + 2].lemma_ == 'が'))):
                ret = self.relational_connect_check(i, ng_pt, verb_pt, *doc)
                if ret['lemma']:
                    return ret
        # oblで直接接続をチェック
        for token in doc:
            if token.dep_ == "obl" and doc[token.i + 1].lemma_ == 'で' and doc[token.i + 2].lemma_ == 'は' and token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能':
                return self.direct_connect_chek(token.i, *doc)
        # oblで間接接続をチェック
        for i in range(0, verb_pt):
            if (doc[i].dep_ == "obl" and doc[i + 1].lemma_ == 'で' and doc[i + 2].lemma_ == 'は' and doc[i].tag_ != '名詞-普通名詞-副詞可能'):
                ret = self.relational_connect_check(i, ng_pt, verb_pt, *doc)
                if ret['lemma']:
                    return ret
        # dislocatedで直接接続をチェック
        for token in doc:
            if (token.dep_ == "dislocated" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能')):
                return self.direct_connect_chek(token.i, *doc)
        # dislocatedで間接接続をチェック
        for i in range(0, verb_pt):
            if (doc[i].dep_ == "dislocated" and doc[i + 1].lemma_ == 'で' and doc[i + 2].lemma_ == 'は' and doc[i].tag_ != '名詞-普通名詞-副詞可能'):
                ret = self.relational_connect_check(i, ng_pt, verb_pt, *doc)
                if ret['lemma']:
                    return ret
        # 〇〇は.....〇〇を△△すると〇〇した　本来なら主語も目的語も△△にかかってほしいものが主語が〇〇にかかってしまって関係が取れない場合の処理
        if doc[verb_pt].dep_ != 'ROOT' and doc[doc[verb_pt].head.i].dep_ == 'ROOT' and (doc[doc[verb_pt].head.head.i - 2].lemma_ == 'た' or doc[doc[verb_pt].head.head.i - 2].lemma_ == 'する') and doc[doc[verb_pt].head.head.i -1].lemma_ == 'と':
            ng_pt = doc[verb_pt].i
            verb_pt = doc[doc[verb_pt].i].head.i
            # 直接接続をチェック
            for token in doc:
                if (token.dep_ == "nsubj" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能') or
                        (doc[token.head.i].head.i == verb_pt and doc[token.head.i].dep_ == 'obl' and doc[token.head.i].tag_ == '名詞-普通名詞-副詞可能')):  # 〇〇は〇〇日　の場合は　日　からかかっているため
                    ret_subj = self.num_chunk(token.i, *doc)
                    ret['lemma_end'] = ret_subj['lemma_end']
                    for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                        if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                            break
                        ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                        ret['lemma_start'] = i
                    return ret
        # 連体修飾をチェック
#        if (doc[verb_end_pt].head.i != verb_end_pt) and ((doc[doc[verb_end_pt].head.i].dep_ == 'nsubj' or doc[doc[verb_end_pt].head.i].dep_ == 'obl' or doc[doc[verb_end_pt].head.i].dep_ == 'obj' or doc[doc[verb_end_pt].head.i].dep_ == 'nmod' or (doc[doc[verb_end_pt].head.i].dep_ == 'ROOT' and doc[doc[verb_end_pt].head.i].i != doc[len(doc) - 1].head.i)) and doc[doc[verb_end_pt].head.i].lemma_ != 'こと'):
        if (doc[verb_end_pt].head.i != verb_end_pt) and ((doc[doc[verb_end_pt].head.i].dep_ == 'nsubj' or doc[doc[verb_end_pt].head.i].dep_ == 'obl' or doc[doc[verb_end_pt].head.i].dep_ == 'obj' or doc[doc[verb_end_pt].head.i].dep_ == 'acl' or doc[doc[verb_end_pt].head.i].dep_ == 'nmod' or (doc[doc[verb_end_pt].head.i].dep_ == 'ROOT' and doc[doc[verb_end_pt].head.i].i != doc[len(doc) - 1].head.i)) and doc[doc[verb_end_pt].head.i].lemma_ != 'こと' and
                                                 ((self.rentai_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '連体形' in doc[verb_end_pt].morph.get("Inflection")[0])) or
                                                 (self.shuusi_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '終止' in doc[verb_end_pt].morph.get("Inflection")[0])))):
            if (doc[doc[verb_end_pt].head.i].pos_ == 'NOUN' or doc[doc[verb_end_pt].head.i].pos_ == 'PROPN' or doc[doc[verb_end_pt].head.i].pos_ == 'NUM'):
#                if doc[verbverb_end_pt_pt].lemma_ in self.campany_special_vaerb:
                    if doc[verb_end_pt].head.i > verb_end_pt:
                        ret_subj = self.num_chunk(doc[verb_end_pt].head.i, *doc)
                    else:
                        ret_subj = self.num_chunk(verb_end_pt + 1, *doc)
                    ret['lemma_end'] = ret_subj['lemma_end']
                    if('「' not in ret_subj["lemma"] and '”' not in ret_subj["lemma"]):
                        for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                            if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                                break
                            ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                            ret['lemma_start'] = i
    #                        if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
    #                            return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
                    else:
                        ret['lemma'] = ret_subj['lemma']
                        ret['lemma_start'] = ret_subj['lemma_start']
                    return ret
        # 〜して〜する〇〇　ただし　〜として〜する〇〇　は例外でだめ　
        if (doc[verb_end_pt - 1].lemma_ != 'と' and len(doc) > verb_end_pt + 2 and doc[verb_end_pt + 1].tag_ == '助詞-接続助詞' and doc[verb_end_pt + 2].pos_ == 'VERB' and doc[doc[verb_end_pt + 2].head.i].pos_ == 'NOUN' and
                ((self.rentai_check(doc[verb_end_pt + 2].i, *doc) or (doc[verb_end_pt + 2].morph.get("Inflection") and '連体形' in doc[verb_end_pt + 2].morph.get("Inflection")[0])) or
                 (self.shuusi_check(doc[verb_end_pt + 2].i, *doc) or (doc[verb_end_pt + 2].morph.get("Inflection") and '終止' in doc[verb_end_pt + 2].morph.get("Inflection")[0])))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt + 2].head.i, * doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 3, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # 〜をしている〇〇
        if(doc[verb_end_pt].lemma_ == 'する' and doc[verb_end_pt - 1].lemma_ == 'を' and
                ((self.rentai_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '連体形' in doc[verb_end_pt].morph.get("Inflection")[0])) or
                 (self.shuusi_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '終止' in doc[verb_end_pt].morph.get("Inflection")[0])))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt].head.i, * doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 1, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # 〜〇〇とした（ている）〇〇
        if(len(doc) > verb_end_pt + 2 and doc[doc[verb_end_pt].head.i].dep_ == 'acl' and doc[verb_end_pt + 1].lemma_ == 'と'and doc[verb_end_pt + 2].lemma_ == 'する' and
                ((self.rentai_check(doc[verb_end_pt + 2].i, *doc)  or (doc[verb_end_pt + 2].morph.get("Inflection") and '連体形' in doc[verb_end_pt + 2].morph.get("Inflection")[0])) or
                ((self.shuusi_check(doc[verb_end_pt + 2].i, *doc)  or (doc[verb_end_pt + 2].morph.get("Inflection") and '終止形' in doc[verb_end_pt + 2].morph.get("Inflection")[0]))))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt].head.head.i, *doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 1, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # 〜〇〇して〇〇する〇〇
        if(len(doc) > verb_end_pt + 5 and doc[doc[verb_end_pt].head.i].dep_ == 'acl' and doc[verb_end_pt + 1].tag_ == '動詞-非自立可能' and doc[verb_end_pt + 2].tag_ == '助詞-接続助詞' and doc[verb_end_pt + 3].pos_ == 'VERB' and
                ((self.rentai_check(doc[verb_end_pt + 3].i, *doc)  or (doc[verb_end_pt + 3].morph.get("Inflection") and '連体形' in doc[verb_end_pt + 3].morph.get("Inflection")[0])) or
                ((self.shuusi_check(doc[verb_end_pt + 3].i, *doc)  or (doc[verb_end_pt + 3].morph.get("Inflection") and '終止形' in doc[verb_end_pt + 3].morph.get("Inflection")[0]))))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt + 3].head.i, *doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 4, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        return ret
