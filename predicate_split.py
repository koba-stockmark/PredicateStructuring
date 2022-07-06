from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
from case_information_get import CaseExtractor
from special_verb_dic import SpecialVerb
import re

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
        s_v = SpecialVerb()
        self.campany_special_verb = s_v.campany_special_verb


    """
   項を分割しない格
    """
    not_devide_case_dic = ["により", "などに"]


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
    カタカナ動詞の複合語のチェック
    """
    def all_katakana(self, word1, word2):
        re_katakana = re.compile(r'[\u30A1-\u30F4ー]+')
        if re_katakana.fullmatch(word1) and re_katakana.fullmatch(word2):
            return True
        return False

    """
    目的語の中の述部を分割

    ret : 目的語　＋　主述部　＋　主述始点　＋　主述部終点
    """
    def object_devide(self, start, end, argument, predicate, *doc):
        compound_word = ['商品', '技術', '製品', '無料', '限定', '特別', '本格', '社会', '新', '国内', '顧客', '一般', '全国', '早期', '事前']    # 複合動を作っても良い普通名詞

        if start == end:
            if (doc[start - 1].lemma_ == 'と' or doc[start - 1].lemma_ == 'や') and self.case_get(start, *doc) == 'を':
                return {'object': '', 'verb': self.compaound(start, end, *doc) + 'する', 'verb_start': start, 'verb_end': end}
            else:
                return {'object': self.compaound(start, end, *doc), 'verb': '', 'verb_start': -1, 'verb_end': -1}
        for i in reversed(range(start, end + 1)):
            if doc[i].pos_ == 'PUNCT' and i != end:
                break
            if doc[i].lemma_ == 'の' and doc[i].pos_ == 'ADP' and doc[i - 1].tag_ != '形状詞-一般' and len(doc) > i + 1 and doc[i + 1].pos_ != 'ADJ' and len(doc) > end + 1 and doc[end + 1].lemma_ != 'で':      # の　で分割。　への　は例外
                if i == start:
                    break
                if doc[end].tag_ == '名詞-普通名詞-サ変可能' and i + 4 >= end:    # 述部の複合語を4語まで許す
                    if doc[end - 1].pos_ == 'NOUN' and doc[end - 1].tag_ != '名詞-普通名詞-サ変可能' and doc[end - 1].lemma_ not in compound_word and not self.all_katakana(doc[end - 1].lemma_, doc[end].lemma_):
                        break
                    return {'object': self.compaound(start, i - 1, *doc), 'verb': self.compaound(i + 1, end, *doc) + 'する', 'verb_start': i + 1, 'verb_end': end}
                elif doc[end].tag_ == '補助記号-括弧閉' and doc[end - 1].tag_ == '名詞-普通名詞-サ変可能' and i + 4 >= end:  # 述部の複合語を4語まで許す カッコ付きの目的語
                    if doc[end - 2].pos_ == 'NOUN' and doc[end - 2].tag_ != '名詞-普通名詞-サ変可能' and doc[end - 2].lemma_ not in compound_word and not self.all_katakana(doc[end - 2].lemma_, doc[end - 1].lemma_):
                        break
                    return {'object': self.compaound(start, i - 1, *doc) + doc[end].orth_, 'verb': self.compaound(i + 1, end - 1, *doc) + 'する', 'verb_start': i + 1, 'verb_end': end - 1}
            elif doc[i].lemma_ == 'こと' and len(doc) > i + 1 and (doc[i + 1].lemma_ == 'の' or doc[i + 1].lemma_ == 'を' or doc[i + 1].lemma_ == 'が'):         # 〇〇することの発表を＋行う
                not_special = False
                for c_pt in reversed(range(0, i - 1)):
                    if doc[c_pt].head.i == i:
                        if (doc[c_pt].lemma_ == '導入' or doc[c_pt].lemma_ == '発足') and doc[c_pt - 1].lemma_ == 'が':
                            not_special = True
                            break
                        if doc[c_pt].lemma_ not in self.campany_special_verb:
                            not_special = True
                            break
                if not_special: # 〜こと　は企業特別述部以外は分割しない
                    continue
                for predic in predicate:
                    if predic["lemma_start"] == start:
                        for arg in argument:
                            if arg["predicate_id"] == predic["id"] and arg["case"] == "を":
                                if doc[i - 1].lemma_ == 'する':
                                    return {'object': arg["lemma"], 'verb': self.compaound(start, i - 2, *doc) + 'する', 'verb_start': start, 'verb_end': end - 2, 'new_object_start': arg["lemma_start"], 'new_object_end': arg["lemma_end"]}
                                if doc[i - 2].lemma_ == 'する' and doc[i - 1].lemma_ == 'た':
                                    return {'object': arg["lemma"], 'verb': self.compaound(start, i - 3, *doc) + 'する', 'verb_start': start, 'verb_end': end - 3, 'new_object_start': arg["lemma_start"], 'new_object_end': arg["lemma_end"]}

                if doc[start - 1].pos_ != 'ADP':
                    return {'object': self.compaound(start, end, *doc), 'verb': '', 'verb_start': -1, 'verb_end': -1}
                if doc[i - 1].lemma_ == 'する':
                    if doc[start - 2].tag_ == '補助記号-括弧閉' or doc[start - 2].lemma_ == '＂':
                        new_obj = self.num_chunk(start - 3, *doc)
                    else:
                        new_obj = self.num_chunk(start - 2, *doc)
                    if new_obj and doc[new_obj["lemma_end"] + 1].lemma_ != 'に':
                        return {'object': new_obj["lemma"], 'verb': self.compaound(start, i - 2, *doc) + 'する', 'verb_start': start, 'verb_end': end - 2, 'new_object_start': new_obj["lemma_start"], 'new_object_end': new_obj["lemma_end"]}
                    else:
                        return {'object': '', 'verb': self.compaound(start, i - 2, *doc) + 'する','verb_start': start, 'verb_end': end - 2}
                if doc[i - 2].lemma_ == 'する' and doc[i - 1].lemma_ == 'た':
                    if doc[start - 2].tag_ == '補助記号-括弧閉':
                        new_obj = self.num_chunk(start - 3, *doc)
                    else:
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
            if i > start and doc[i - 1].tag_ == '動詞-一般':
                continue
            if doc[i].norm_ in s_v_dic.sub_verb_dic:
                if doc[i - 1].tag_ != '名詞-普通名詞-サ変可能':  # 本格始動　など普通名詞との合成
                    if doc[end].lemma_ == 'ため' or doc[end].lemma_ == 'もの' or doc[end].lemma_ == 'とき' or doc[end].lemma_ == 'こと' or doc[end].lemma_ == '場合' or doc[end].lemma_ == '人' or doc[end].lemma_ == 'とき':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'だ', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    elif doc[end].tag_ == '名詞-普通名詞-サ変可能':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    elif doc[end].lemma_ == 'だ' or doc[end].lemma_ == 'です':
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) , 'verb_start': -1,'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                    elif doc[end].norm_ == '出来る':
                        if doc[end - 1].pos_ == 'ADP':
                            return {'verb': self.compaound(start, i - 2, *doc) + 'する', 'sub_verb': 'できる', 'verb_start': start, 'verb_end': i - 2, 'sub_verb_start': end, 'sub_verb_end': end}
                        else:
                            return {'verb': self.compaound(start, i - 1, *doc) + 'する', 'sub_verb': 'できる', 'verb_start': start, 'verb_end': i - 1, 'sub_verb_start': end, 'sub_verb_end': end}
                    elif doc[end - 3].norm_ == '出来る' and doc[end - 2].orth_ == 'よう' and doc[end - 1].orth_ == 'に' and doc[end].norm_ == '成る':
                        if doc[end - 4].pos_ == 'ADP':
                            return {'verb': self.compaound(start, end - 5, *doc) + 'する', 'sub_verb': 'できるようになる', 'verb_start': start, 'verb_end': end - 5, 'sub_verb_start': end - 4, 'sub_verb_end': end}
                        else:
                            return {'verb': self.compaound(start, end - 4, *doc) + 'する', 'sub_verb': 'できるようになる', 'verb_start': start, 'verb_end': end - 4, 'sub_verb_start': end - 4, 'sub_verb_end': end}
                    else:
                        return {'verb': '', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': -1, 'verb_end': -1, 'sub_verb_start': i, 'sub_verb_end': end}
                if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                    return {'verb': self.compaound(start, i - 1, *doc) + 'する', 'sub_verb': self.compaound(i, end, *doc) + 'する', 'verb_start': start, 'verb_end': i - 1, 'sub_verb_start': i, 'sub_verb_end': end}
                else:
                    return {'verb': self.compaound(start, i - 1, *doc) + 'する', 'sub_verb': self.compaound(i, end, *doc), 'verb_start': start, 'verb_end': i - 1, 'sub_verb_start': i, 'sub_verb_end': end}
        return {'verb': self.compaound(start, end, *doc), 'sub_verb': '', 'verb_start': start, 'verb_end': end, 'sub_verb_start': -1, 'sub_verb_end': -1}
