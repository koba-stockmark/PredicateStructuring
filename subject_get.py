from chunker import ChunkExtractor
from special_verb_dic import SpecialVerb
from case_information_get import CaseExtractor

class SubjectExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.head_connect_check = chunker.head_connect_check
        self.connect_word = chunker.connect_word
        self.rentai_check = chunker.rentai_check
        self.shuusi_check = chunker.shuusi_check
        c_g = CaseExtractor()
        self.case_get = c_g.case_get




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
                if doc[doc[chek].i + 1].tag_ == '形状詞-助動詞語幹' and doc[doc[chek].i + 1].head.i == doc[doc[chek].i].i:
                    break
                if doc[chek].lemma_ != '運営' and doc[chek].lemma_ != '提携' and doc[chek].head.lemma_ != 'ほか':
                    if ((doc[chek].morph.get("Inflection") and '連体形' in doc[chek].morph.get("Inflection")[0]) or
                            (doc[chek + 1].pos_ == 'AUX' and doc[chek + 1].morph.get("Inflection") and '連体形' in doc[chek + 1].morph.get("Inflection")[0]) or
                            (doc[chek + 1].pos_ == 'AUX' and doc[chek + 2].pos_ == 'AUX' and doc[chek + 2].morph.get("Inflection") and '連体形' in doc[chek + 2].morph.get("Inflection")[0])):
                        break
                    if self.rentai_check(chek, *doc):
                        if doc[doc[chek].head.i].lemma_ != 'こと':
                            break
                if doc[chek + 1].orth_ == 'さ' and doc[chek + 2].lemma_ == 'れる' and doc[chek + 3].lemma_ == 'た':
                    break
                if doc[chek].pos_ == 'NOUN' and doc[chek - 1].orth_ == 'が' and doc[chek + 1].orth_ == 'で':  # 〜が理由で…
                    break
                if doc[chek].norm_ == '成る' and doc[chek - 1].orth_ == 'に':  # 〜が〜になる〜する…
                    break
                if doc[chek].pos_ == 'ADJ':
                    break
                chek = doc[chek].head.i
        if doc[pt].i != ng_pt and (chek == verb_pt or chek == doc[verb_pt].head.i or
                                   (chek == doc[verb_pt].head.head.i and (doc[verb_pt].head.pos_ != 'NOUN' or (doc[verb_pt].head.dep_ == 'advcl' and doc[verb_pt].head.head.pos_ == 'VERB') or doc[verb_pt].head.lemma_ == 'こと'))):
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
    def subject_get(self, verb_pt, verb_end_pt, *doc):
        s_v = SpecialVerb()
        ng_pt = verb_pt
        ret = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # subjで直接接続をチェック
        for token in doc:
            if token.dep_ == "nsubj" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能'):
                if doc[token.head.i].norm_ == '出来る':
                    continue
                return self.direct_connect_chek(token.i, *doc)
        # subjで間接接続をチェック
        for i in range(0, verb_pt):
            if ((doc[i].dep_ == "nsubj" and doc[i].tag_ != '名詞-普通名詞-副詞可能') or
                 (len(doc) > i + 2 and doc[i].dep_ == "obl" and doc[i].tag_ != '名詞-普通名詞-副詞可能' and doc[i + 1].lemma_ == 'など' and (doc[i + 2].lemma_ == 'は' or doc[i + 2].lemma_ == 'が'))):
                if doc[doc[i].head.i].norm_ == '出来る':
                    continue
                ret = self.relational_connect_check(i, ng_pt, verb_pt, *doc)
                if ret['lemma']:
                    return ret
        # oblで直接接続をチェック
        for token in doc:
            case = self.case_get(token.i, *doc)
            if token.dep_ == "obl" and (case == 'では' or case == 'が') and token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能':
                return self.direct_connect_chek(token.i, *doc)
        # oblで間接接続をチェック
        for i in range(0, verb_pt):
            if doc[i].dep_ == "obl" and doc[i + 1].lemma_ == 'で' and doc[i + 2].lemma_ == 'は' and doc[i].tag_ != '名詞-普通名詞-副詞可能':
                ret = self.relational_connect_check(i, ng_pt, verb_pt, *doc)
                if ret['lemma']:
                    return ret
        # dislocatedで直接接続をチェック
        for token in doc:
            if token.dep_ == "dislocated" and ((token.head.i == verb_pt or token.head.i == verb_end_pt) and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能'):
                return self.direct_connect_chek(token.i, *doc)
        # dislocatedで間接接続をチェック
        for i in range(0, verb_pt):
            if doc[i].dep_ == "dislocated" and doc[i + 1].lemma_ == 'で' and doc[i + 2].lemma_ == 'は' and doc[i].tag_ != '名詞-普通名詞-副詞可能':
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
        if (doc[verb_end_pt].head.i != verb_end_pt) and ((doc[doc[verb_end_pt].head.i].dep_ == 'nsubj' or doc[doc[verb_end_pt].head.i].dep_ == 'obl' or doc[doc[verb_end_pt].head.i].dep_ == 'obj' or doc[doc[verb_end_pt].head.i].dep_ == 'acl' or doc[doc[verb_end_pt].head.i].dep_ == 'nmod' or (doc[doc[verb_end_pt].head.i].dep_ == 'ROOT' and doc[doc[verb_end_pt].head.i].i != doc[len(doc) - 1].head.i)) and doc[doc[verb_end_pt].head.i].lemma_ != 'こと' and
                                                 ((self.rentai_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '連体形' in doc[verb_end_pt].morph.get("Inflection")[0])) or
                                                 (self.shuusi_check(doc[verb_end_pt].i, *doc) or (doc[verb_end_pt].morph.get("Inflection") and '終止' in doc[verb_end_pt].morph.get("Inflection")[0])))):
            if (doc[doc[verb_end_pt].head.i].pos_ == 'NOUN' or doc[doc[verb_end_pt].head.i].pos_ == 'PROPN' or doc[doc[verb_end_pt].head.i].pos_ == 'NUM') and doc[doc[verb_end_pt].head.i].lemma_ != '予定':
 #               if doc[verb_end_pt].lemma_ in s_v.campany_special_verb:
                if doc[verb_end_pt + 1].lemma_ != 'さまざま':
                    if doc[verb_end_pt].head.i > verb_end_pt:
                        ret_subj = self.num_chunk(doc[verb_end_pt].head.i, *doc)
                    else:
                        ret_subj = self.num_chunk(verb_end_pt + 1, *doc)
                    ret['lemma_end'] = ret_subj['lemma_end']
                    if ret_subj['lemma_start'] == verb_end_pt and doc[verb_end_pt].pos_ == 'ADJ':    # 形容詞が前についているときは削る
                        ret_subj['lemma_start'] = verb_end_pt + 1
                    if '「' not in ret_subj["lemma"] and '”' not in ret_subj["lemma"]:
                        for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                            if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                                break
                            ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                            ret['rentai_subject'] = True
                            ret['lemma_start'] = i
                    else:
                        ret['lemma'] = ret_subj['lemma']
                        ret['rentai_subject'] = True
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
                ret['rentai_subject'] = True
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
                ret['rentai_subject'] = True
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # 〜〇〇とした（ている）〇〇
        if(len(doc) > verb_end_pt + 2 and doc[doc[verb_end_pt].head.i].dep_ == 'acl' and doc[verb_end_pt + 1].lemma_ == 'と'and doc[verb_end_pt + 2].lemma_ == 'する' and
                ((self.rentai_check(doc[verb_end_pt + 2].i, *doc) or (doc[verb_end_pt + 2].morph.get("Inflection") and '連体形' in doc[verb_end_pt + 2].morph.get("Inflection")[0])) or
                (self.shuusi_check(doc[verb_end_pt + 2].i, *doc) or (doc[verb_end_pt + 2].morph.get("Inflection") and '終止形' in doc[verb_end_pt + 2].morph.get("Inflection")[0])))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt].head.head.i, *doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 1, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['rentai_subject'] = True
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        # 〜〇〇して〇〇する〇〇
        if(len(doc) > verb_end_pt + 5 and doc[doc[verb_end_pt].head.i].dep_ == 'acl' and doc[verb_end_pt + 1].tag_ == '動詞-非自立可能' and doc[verb_end_pt + 2].tag_ == '助詞-接続助詞' and doc[verb_end_pt + 3].pos_ == 'VERB' and
                ((self.rentai_check(doc[verb_end_pt + 3].i, *doc)  or (doc[verb_end_pt + 3].morph.get("Inflection") and '連体形' in doc[verb_end_pt + 3].morph.get("Inflection")[0])) or
                (self.shuusi_check(doc[verb_end_pt + 3].i, *doc) or (doc[verb_end_pt + 3].morph.get("Inflection") and '終止形' in doc[verb_end_pt + 3].morph.get("Inflection")[0])))):
            if doc[verb_end_pt].head.i > verb_end_pt:
                ret_subj = self.num_chunk(doc[verb_end_pt + 3].head.i, *doc)
            else:
                ret_subj = self.num_chunk(verb_end_pt + 4, *doc)
            ret['lemma_end'] = ret_subj['lemma_end']
            for i in reversed(range(ret_subj['lemma_start'], ret_subj['lemma_end'] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret['lemma'] = self.connect_word(doc[i].orth_, ret['lemma'])
                ret['rentai_subject'] = True
                ret['lemma_start'] = i
                if len(doc) > i + 1 and doc[i + 1].pos_ == 'ADP' and doc[i + 1].lemma_ == 'を':
                    return {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
        return ret
