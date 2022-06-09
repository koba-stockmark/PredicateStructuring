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
        self.compaound = chunker.compaound
        c_g = CaseExtractor()
        self.case_get = c_g.case_get






    """
    補助動詞かどうかの判別
    """
    def sub_verb_chek(self, check_w):
        s_v_dic = SubVerbDic()
        for sub_verb_w in s_v_dic.sub_verb_dic:
            if sub_verb_w in check_w:
#            if check_w.startswith(sub_verb_w):
                return True
        return False


    """
    述部に対するobjを探索
    """
    def object_serch(self, start, *doc):
        for token in doc:
            if token.head.i == start and token.dep_ == 'obj':
                return self.num_chunk(token.i, *doc)['lemma']
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
            if doc[i].pos_ == 'PUNCT':
                break
            if doc[i].lemma_ == 'の' and doc[i].pos_ == 'ADP' and doc[i + 1].pos_ != 'ADJ':      # の　で分割。　への　は例外
                if doc[end].tag_ == '名詞-普通名詞-サ変可能' and i + 4 >= end:    # 述部の複合語を4語まで許す
                    return {'object': self.compaound(start, i - 1, *doc), 'verb': self.compaound(i + 1, end, *doc) + 'する', 'verb_start': i + 1, 'verb_end': end}
            elif doc[i].lemma_ == 'こと' and len(doc) > i + 1 and (doc[i + 1].lemma_ == 'の' or doc[i + 1].lemma_ == 'を'):         # 〇〇することの発表を＋行う
                if doc[i - 1].lemma_ == 'する':
                    return {'object': self.object_serch(start, * doc), 'verb': self.compaound(start, i - 2, *doc) + 'する', 'verb_start': start, 'verb_end': end - 2}
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
