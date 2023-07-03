class DeepCaseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


    case_change_rule = [
        {"deep_case": "AND格", "case": "と", "post_pos": "NOUN"},
        {"deep_case": "OR格", "case": "または", "post_pos": "NOUN"},

        {"deep_case": "動作主格", "case": "が"},
        {"deep_case": "経験者格", "case": "が"},
        {"deep_case": "経験者格", "case": "について*"},
        {"deep_case": "場所格", "case": "で", "pre_tag": "地名"},
        {"deep_case": "道具格", "case": "で"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "年"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "月"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "日"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "時"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "分"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "秒"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "頭"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "末"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "後"},
        {"deep_case": "時間格", "case": "に*", "pre_word": "度内"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "年"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "月"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "日"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "時"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "分"},
        {"deep_case": "時間格", "case": "副詞的", "pre_word": "秒"},
        {"deep_case": "原因格", "case": "に", "pre_word": "ため"},
        {"deep_case": "原因格", "case": "ために-副詞的"},
        {"deep_case": "対象格", "case": "を"},
        {"deep_case": "対象格", "case": "と"},
        {"deep_case": "対象格", "case": "のを-副詞的"},

        {"deep_case": "源泉格", "case": "から"},
        {"deep_case": "目標格", "case": "に"},
        {"deep_case": "目標格", "case": "へ"},
        {"deep_case": "目標格", "case": "への"},

        {"deep_case": "期間格", "case": "に"},
        {"deep_case": "協業格", "case": "と"},
        {"deep_case": "費用格", "case": "で"},
        {"deep_case": "物量格", "case": "の", "pre_tag": "数詞"},
        {"deep_case": "物量格", "case": "の", "pre_tag": "助数詞可能"},

        {"deep_case": "比較格", "case": "より"},    # モダリティとの関係は？
        {"deep_case": "所有・部分格", "case": "の"},
        {"deep_case": "内容格", "case": "とも"},
        {"deep_case": "材料格", "case": "から"},

        {"deep_case": "連用修飾-動詞", "case": "ながら"},
        {"deep_case": "連体修飾-様態", "case": "の"},
        {"deep_case": "連体修飾-様態", "case": "な", "pre_word": "な"},

        {"deep_case": "連用修飾", "case": "*副詞的"},
        {"deep_case": "連体修飾", "case": "連体修飾"}
    ]


    """
    深層格の獲得    
    """
    def deep_case_get(self, case, pt, *doc):
        for chek in self.case_change_rule:
            aa = chek["case"][:-1]
            aa = chek["case"][:1]
            aa = chek["case"][1:]
            if (chek["case"] == case or
                    (chek["case"].endswith("*") and case.startswith(chek["case"][:-1])) or
                    (chek["case"].startswith("*") and case.endswith(chek["case"][1:]))):
                if "pre_tag" in chek:
                    if chek["pre_tag"] in doc[pt].tag_:
                        if "pre_word" in chek:
                            if doc[pt].lemma_.endswith(chek["pre_word"]):
                               return chek["deep_case"]
                        else:
                            return chek["deep_case"]
                elif "post_pos" in chek:
                    if len(doc) > pt + 1 and chek["post_pos"] in doc[pt + 1].pos_:
                        if "pre_word" in chek:
                            if doc[pt].lemma_.endswith(chek["pre_word"]):
                                return chek["deep_case"]
                        else:
                            return chek["deep_case"]
                elif "pre_word" in chek:
                    if doc[pt].lemma_.endswith(chek["pre_word"]):
                        return chek["deep_case"]
                else:
                    return chek["deep_case"]
        return ""