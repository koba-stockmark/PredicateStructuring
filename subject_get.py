from chunker import ChunkExtractor

class SubjectExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk

    """
        目的語に対する主語の取得
        目的語のかかり先の動詞にかかる主語を探す
        〇〇と〇〇　のような並列は分割してひとつだけを返す。
        見つからないときは　連体修飾　「△△△をする〇〇(主語)は、」　のような形式からも探す　
        
        in: 目的語ID
        return : 主語文字列　始点ノードID　終点ノードID
    """
    def subject_get_from_object(self, obj_point, *doc):
        ret = ['', 0, 0]
        ng_pt = obj_point
        verb_pt = doc[obj_point].head.i
        # 直接接続をチェック
        for token in doc:
            if (token.dep_ == "nsubj" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能')):
#                    (doc[token.head.i].head.i == verb_pt and doc[token.head.i].dep_ == 'obl' and doc[token.head.i].tag_ == '名詞-普通名詞-副詞可能')):  # 〇〇は〇〇日　の場合は　日　からかかっているため
                ret_subj = self.num_chunk(token.i, *doc)
                ret[2] = ret_subj[2]
                for i in reversed(range(ret_subj[1], ret_subj[2] + 1)):  # 〇〇と〇〇　は切り離す
                    if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                        break
                    ret[0] = doc[i].orth_ + ret[0]
                    ret[1] = i
                return ret
        # 〇〇を〇〇すると〇〇した　のチェック
        """
        text = 'NECは1月4日、警視庁向けに、75歳以上の高齢者が運転免許更新時に受ける認知機能検査時、電話予約に加えスマートフォンやパソコンからインターネットで24時間予約を受付するシステムを構築し、都内の運転免許試験場で運用を開始したと発表した。'
        ng_pt = doc[obj_point].head.i
        verb_pt = doc[doc[obj_point].head.i].head.i
        # 直接接続をチェック
        for token in doc:
            if (token.dep_ == "nsubj" and (token.head.i == verb_pt and token.i != ng_pt and token.tag_ != '名詞-普通名詞-副詞可能') or
                    (doc[token.head.i].head.i == verb_pt and doc[token.head.i].dep_ == 'obl' and doc[token.head.i].tag_ == '名詞-普通名詞-副詞可能')):  # 〇〇は〇〇日　の場合は　日　からかかっているため
                ret_subj = self.num_chunk(token.i, *doc)
                ret[2] = ret_subj[2]
                for i in reversed(range(ret_subj[1], ret_subj[2] + 1)):  # 〇〇と〇〇　は切り離す
                    if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                        break
                    ret[0] = doc[i].orth_ + ret[0]
                    ret[1] = i
                return ret
        """
        # 間接接続をチェック
        ng_pt = obj_point
        verb_pt = doc[obj_point].head.i
        for i in reversed(range(0, verb_pt)):
            if ((doc[i].dep_ == "nsubj" and doc[i].tag_ != '名詞-普通名詞-副詞可能') or
                    (len(doc) > i + 2 and doc[i].dep_ == "obl" and doc[i].tag_ != '名詞-普通名詞-副詞可能' and doc[i + 1].lemma_ == 'など' and (doc[i + 2].lemma_ == 'は' or doc[i + 2].lemma_ == 'が'))):
                chek = doc[i].head.i
                while chek != doc[chek].head.i:
                    if chek == verb_pt:
                        break
                    else:
                        if (doc[doc[chek].i + 1].tag_ == '形状詞-助動詞語幹' and doc[doc[chek].i + 1].head.i == doc[doc[chek].i].i):
                            break
#                        if doc[doc[chek].i].tag_ == '名詞-普通名詞-助数詞可能':
#                            break
                        if doc[chek].pos_ == 'ADJ':
                            break
                        chek = doc[chek].head.i
                if doc[i].i != ng_pt and (chek == verb_pt or chek == doc[verb_pt].head.i or chek == doc[verb_pt].head.head.i):
                    ret_subj = self.num_chunk(doc[i].i, *doc)
                    ret[2] = ret_subj[2]
                    for i in reversed(range(ret_subj[1], ret_subj[2] + 1)):  # 〇〇と〇〇　は切り離す
                        if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                            break
                        ret[0] = doc[i].orth_ + ret[0]
                        ret[1] = i
                    return ret
        # 連体修飾をチェック
        if doc[doc[obj_point].head.head.i].dep_ == 'nsubj':
            ret_subj = self.num_chunk(doc[obj_point].head.head.i, *doc)
            ret[2] = ret_subj[2]
            for i in reversed(range(ret_subj[1], ret_subj[2] + 1)):  # 〇〇と〇〇　は切り離す
                if doc[i].pos_ == 'ADP' and doc[i].lemma_ == 'と':
                    break
                ret[0] = doc[i].orth_ + ret[0]
                ret[1] = i
        return ret
