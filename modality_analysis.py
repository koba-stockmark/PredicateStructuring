"""
  モダリティ解析
     断定、過去、否定、意思・願望、勧誘、推量、仮定、可能、疑問
"""
import re

class ModalityAnalysis:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

    # 断定
    dantei_rule = [
        ["で", "ある"],
        ["です"],
        ["だ"]
    ]
    # 過去
    kako_rule = [
        ["て", "い", "た"],
        ["で", "い", "た"],
        ["て", "あっ", "た"],
        ["で", "あっ", "た"],
        ["て", "み", "た"],
        ["で", "み", "た"],
        ["て", "おい", "た"],
        ["で", "おい", "た"],
        ["だっ", "た"],
        ["た"],
        ["だ"]
    ]
    # 否定
    hitei_rule = [
        ["ない"]
    ]
    # 意思
    ishi_rule = [
        ["たい"],
        ["期待", "する"],
        ["ほしい"]
    ]
    # 勧誘
    kanyuu_rule = [
        ["ましょう"],
        ["ください"]
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
    # 可能
    kanou_rule = [
        ["!する", "れる"],
        ["できる"],
        ["られる"],
        [".*える"],
#        [".*ける"],
        [".*げる"],
        [".*せる"],
#        [".*ぜる"],
        [".*てる"],
#        [".*でる"],
        [".*ねる"],
        [".*べる"],
        [".*める"],
        [".*れる"]
    ]
    # 疑問
    gimon_rule = [
        ["の", "か", "。"],
        ["の", "か", "、"],
        ["の", "か", "\?"],
        ["いかに", "\?"],
        ["だ", "の", "か"],
        ["か", "どう", "か"],
        ["べし", "か"],   # べきか
        ["だ", "か"]      # だろうか
    ]

    # 文節区切り品詞
    stop_pos = [
        "VERB", "NOUN", "PUNCT", "PRON", "SYM", "NUM"
    ]

    # orth で比較必要する必要なあるルール
    orth_chek_rule = [suiron_rule, kako_rule, kanyuu_rule, kanou_rule, dantei_rule]

    def rule_chek(self, rule, tag, ret, pt, *doc):
        for chek in rule:
            chek_w = chek[0]
            ng_word = False
            if chek_w[0] == "!":
                chek_w = chek_w[1:]
                ng_word = True
            if (rule in self.orth_chek_rule and re.match(chek_w, doc[pt].orth_)) or (rule not in self.orth_chek_rule and re.match(chek_w, doc[pt].lemma_)) or ng_word:
                if ng_word and ((rule in self.orth_chek_rule and re.match(chek_w, doc[pt].orth_)) or (rule not in self.orth_chek_rule and re.match(chek_w, doc[pt].lemma_))):
                    continue
                if chek_w[0] == "." and doc[pt].orth_ == doc[pt].norm_:
                    continue
                baias = 0
                find = True
                for n_chek in chek:
                    if n_chek[0] == "!":
                        n_chek = n_chek[1:]
                        if (len(doc) < pt + baias or
                                (rule in self.orth_chek_rule and re.match(n_chek, doc[pt + baias].orth_)) or
                                (rule not in self.orth_chek_rule and re.match(n_chek, doc[pt + baias].lemma_))):
                            find = False
                            break
                        baias = baias + 1
                    else:
                        if (len(doc) <= pt + baias or
                                (rule in self.orth_chek_rule and not re.match(n_chek, doc[pt + baias].orth_)) or
                                (rule not in self.orth_chek_rule and not re.match(n_chek, doc[pt + baias].lemma_))):
                            find = False
                            break
                        baias = baias + 1
                if find:
                    if tag not in ret:
                        ret.append(tag)
        return

    def modality_get(self, sp, *doc):
        ret = []
        verb_in = False

        for pt in range(sp, len(doc)):
            if len(doc) < pt:
                return ret
            if doc[pt].pos_ in self.stop_pos and pt != sp:
                if doc[pt].norm_ != "為る" and doc[pt].norm_ != "こと" and (doc[pt - 1].lemma_ != "を" or doc[pt].lemma_ != "する") and doc[pt - 1].pos_ != "NOUN":
                    break
            if pt != sp and (doc[pt].pos_ == "VERB" or doc[pt].pos_ == "AUX"):
                verb_in = True

            # 断定
            if doc[sp].pos_ == "NOUN":
                self.rule_chek(self.dantei_rule, "<断定>", ret, pt, *doc)

            # 過去
            if doc[sp].pos_ != "NOUN" or verb_in or (len(doc) > sp + 1 and doc[sp + 1].lemma_ == "を") or (len(doc) > sp + 1 and doc[sp + 1].orth_ == "だっ"):
                self.rule_chek(self.kako_rule, "<過去>", ret, pt, *doc)

            # 否定
            self.rule_chek(self.hitei_rule, "<否定>", ret, pt, *doc)

            # 意思・願望
            self.rule_chek(self.ishi_rule, "<意思・願望>", ret, pt, *doc)

            # 勧誘
            self.rule_chek(self.kanyuu_rule, "<勧誘>", ret, pt, *doc)

            # 推量
            self.rule_chek(self.suiron_rule, "<推量>", ret, pt, *doc)

            # 仮定
            self.rule_chek(self.katei_rule, "<仮定>", ret, pt, *doc)

            # 可能
            self.rule_chek(self.kanou_rule, "<可能>", ret, pt, *doc)

            # 疑問
            self.rule_chek(self.gimon_rule, "<疑問>", ret, pt, *doc)
        return ret
