"""
  モダリティ解析
     過去、否定、意思・願望、推量、仮定、疑問
"""


class ModalityAnalysis:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

    # 過去
    kako_rule = [
        ["た"],
        ["だ"]
    ]
    # 否定
    hitei_rule = [
        ["ない"]
    ]
    # 意思
    ishi_rule = [
        ["たい"]
    ]
    # 推量
    suiron_rule = [
        ["か", "も", "しれ", "ない"],
        ["で", "あろう"],
        ["だろう"]
    ]
    # 仮定
    katei_rule = [
        ["ば"]
    ]
    # 疑問
    gimon_rule = [
        ["の", "か", "。"],
        ["の", "か", "、"],
        ["の", "か", "？"],
        ["か", "どう", "か"],
        ["だろう", "か"]
    ]

    # 文節区切り品詞
    stop_pos = [
        "VERB", "NOUN", "PUNCT", "PRON", "SYM", "NUM"
    ]

    def rule_chek(self, rule, tag, ret, pt, *doc):
        for chek in rule:
            if ((rule == self.suiron_rule or rule == self.kako_rule) and doc[pt].orth_ == chek[0]) or (
                    rule != self.suiron_rule and rule != self.kako_rule and doc[pt].lemma_ == chek[0]):
                baias = 0
                find = True
                for n_chek in chek:
                    if (len(doc) < pt + baias or
                            ((rule == self.suiron_rule or rule == self.kako_rule) and doc[pt + baias].orth_ != n_chek) or
                            (rule != self.suiron_rule and rule != self.kako_rule and doc[pt + baias].lemma_ != n_chek)):
                        find = False
                        break
                    baias = baias + 1
                if find:
                    if tag not in ret:
                        ret.append(tag)
        return

    def modality_get(self, sp, *doc):
        ret = []

        for pt in range(sp + 1, len(doc) - 1):
            if len(doc) < pt:
                return ret
            if doc[pt].pos_ in self.stop_pos:
                break

            # 過去
            self.rule_chek(self.kako_rule, "<過去>", ret, pt, *doc)

            # 否定
            self.rule_chek(self.hitei_rule, "<否定>", ret, pt, *doc)

            # 意思・願望
            self.rule_chek(self.ishi_rule, "<意思・願望>", ret, pt, *doc)

            # 推量
            self.rule_chek(self.suiron_rule, "<推量>", ret, pt, *doc)

            # 仮定
            self.rule_chek(self.katei_rule, "<仮定>", ret, pt, *doc)

            # 疑問
            self.rule_chek(self.gimon_rule, "<疑問>", ret, pt, *doc)
        return ret
