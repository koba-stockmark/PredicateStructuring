from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from case_information_get import CaseExtractor

class VerbSpliter:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.compaound = chunker.compaound
        c_g = CaseExtractor()
        self.case_get = c_g.case_get






    """
    補助動詞かどうかの判別
    """
    def sub_verb_chek(self, check_w):
        s_v_dic = SubVerbDic()
        check_word = check_w
        if check_word[-2:] == 'する' and check_word != 'する':
            check_word = check_word[:-2]
        if check_word[-4:] == '(する)' and check_word != '(する)':
            check_word = check_word[:-4]
        if check_word[-3:] == '(だ)' and check_word != '(だ)':
            check_word = check_word[:-3]
        if check_word[-4:] == '(です)' and check_word != '(です)':
            check_word = check_word[:-4]
        if check_word in s_v_dic.sub_verb_dic:
            return True
        return False


    """
    述部に対するobjを探索
    """
    def object_serch(self, start, *doc):
        for token in doc:
            if token.head.i == start and token.dep_ == 'obj':
                self.num_chunk(token.i, *doc)
        return ''


    """
    目的語の中の述部を分割

    ret : 目的語　＋　主述部　＋　主述始点　＋　主述部終点
    """
    def object_devide(self, start, end, *doc):
#        if start == end or doc[end].lemma_ == 'サービス':
#            return {'object': self.compaound(start, end, *doc), 'verb': '', 'verb_start': -1, 'verb_end': -1}
        if start == end:
            if (doc[start - 1].lemma_ == 'と' or doc[start - 1].lemma_ == 'や') and self.case_get(start, *doc) == 'を':
                return {'object': '', 'verb': self.compaound(start, end, *doc) + 'する', 'verb_start': start, 'verb_end': end}
            else:
                return {'object': self.compaound(start, end, *doc), 'verb': '', 'verb_start': -1, 'verb_end': -1}
        for i in reversed(range(start, end + 1)):
            if doc[i].pos_ == 'PUNCT' and i != end:
                break
            if doc[i].lemma_ == 'の' and doc[i].pos_ == 'ADP' and doc[i + 1].pos_ != 'ADJ' and doc[end + 1].lemma_ != 'で':      # の　で分割。　への　は例外
                if (doc[end].tag_ == '名詞-普通名詞-サ変可能' or doc[end].tag_ == '名詞-普通名詞-一般') and i + 4 >= end:    # 述部の複合語を4語まで許す
                    return {'object': self.compaound(start, i - 1, *doc), 'verb': self.compaound(i + 1, end, *doc) + 'する', 'verb_start': i + 1, 'verb_end': end}
                elif doc[end].tag_ == '補助記号-括弧閉' and i + 4 >= end:  # 述部の複合語を4語まで許す カッコ付きの目的語
                    return {'object': self.compaound(start, i - 1, *doc) + doc[end].orth_, 'verb': self.compaound(i + 1, end - 1, *doc) + 'する', 'verb_start': i + 1, 'verb_end': end - 1}
            elif doc[i].lemma_ == 'こと' and len(doc) > i + 1 and (doc[i + 1].lemma_ == 'の' or doc[i + 1].lemma_ == 'を' or doc[i + 1].lemma_ == 'が'):         # 〇〇することの発表を＋行う
                if doc[i - 1].lemma_ == 'する':
                    new_obj = self.num_chunk(start - 1, *doc)
                    if new_obj:
                        return {'object': new_obj["lemma"], 'verb': self.compaound(start, i - 2, *doc) + 'する', 'verb_start': start, 'verb_end': end - 2, 'new_object_start': new_obj["lemma_start"], 'new_object_end': new_obj["lemma_end"]}
                    else:
                        return {'object': '', 'verb': self.compaound(start, i - 2, *doc) + 'する','verb_start': start, 'verb_end': end - 2}
                if doc[i - 2].lemma_ == 'する' and doc[i - 1].lemma_ == 'た':
                    new_obj = self.num_chunk(start - 2, *doc)
                    if new_obj:
                        return {'object': new_obj["lemma"], 'verb': self.compaound(start, i - 3, *doc) + 'する','verb_start': start, 'verb_end': end - 3, 'new_object_start': new_obj["lemma_start"], 'new_object_end': new_obj["lemma_end"]}
                    else:
                        return {'object': '', 'verb': self.compaound(start, i - 3, *doc) + 'する','verb_start': start, 'verb_end': end - 3}
                if doc[i - 1].pos_ == 'VERB':   # 動詞　＋　こと　＋　（を、の、が）
                    new_verb = self.verb_chunk(start, *doc)
                    adp_pt = -1
                    for adp_pt in reversed(range(0, new_verb["lemma_start"] - 1)):  # 助詞を挟んだ自立語を探す
                        if doc[adp_pt].pos_ != 'ADP':
                            break
                    new_obj = self.num_chunk(adp_pt, *doc)
                    if new_obj:
                        return {'object': new_obj["lemma"], 'verb': new_verb["lemma"], 'verb_start': new_verb["lemma_start"], 'verb_end': new_verb["lemma_end"], 'new_object_start': new_obj["lemma_start"], 'new_object_end': new_obj["lemma_end"]}
                    else:
                        return {'object': '', 'verb': new_verb["lemma"], 'verb_start': new_verb["lemma_start"], 'verb_end': new_verb["lemma_end"]}

        return {'object': self.compaound(start, end, *doc), 'verb': '', 'verb_start': -1, 'verb_end': -1}


    """
    複合術部を主述部と補助術部に分割
    
    ret : 主述部　＋　補助術部　＋　主述始点　＋　主述部終点　＋　補助述部始点　＋　補助述部終点
    """
    def verb_devide(self, start, end, *doc):
        s_v_dic = SubVerbDic()
        if start == end:
            return {'verb': self.compaound(start, end, *doc), 'sub_verb': '', 'verb_start': start, 'verb_end': end, 'sub_verb_start': -1, 'sub_verb_end': -1}
        for i in reversed(range(start, end + 1)):
            if doc[i].norm_ in s_v_dic.sub_verb_dic:
                if doc[i - 1].tag_ != '名詞-普通名詞-サ変可能':  # 本格始動　など普通名詞との合成
                    if doc[end].lemma_ == 'ため' or doc[end].lemma_ == 'もの' or doc[end].lemma_ == 'とき' or doc[end].lemma_ == 'こと' or doc[end].lemma_ == '場合' or doc[end].lemma_ == '人' or doc[end].lemma_ == 'とき':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'だ', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    elif doc[end].tag_ == '名詞-普通名詞-サ変可能':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    elif doc[end].lemma_ == 'だ' or doc[end].lemma_ == 'です':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) , 'verb_start': -1,'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    else:
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                    return {'verb': self.compaound(start, i - 1, *doc) + 'する', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': start, 'verb_end': i - 1, 'sub_verb_start': i, 'sub_verb_end': end}
                else:
                    return {'verb': self.compaound(start, i - 1, *doc) + 'する', 'sub_verb': self.compaound(i, end, *doc), 'verb_start': start, 'verb_end': i - 1, 'sub_verb_start': i, 'sub_verb_end': end}
        return {'verb': self.compaound(start, end, *doc), 'sub_verb': '', 'verb_start': start, 'verb_end': end, 'sub_verb_start': -1, 'sub_verb_end': -1}
