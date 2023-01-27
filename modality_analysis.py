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
        ["ず"],
        ["ぬ"],
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
        [".*よう"],
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
    # 引用
    innyou_rule = [
        ["より"]
    ]
    # 容易
    youi_rule = [
        ["やすい"]
    ]
    # 限定
    gentei_rule = [
        ["だけ"],
        ["まで"]
    ]
    # 目標
    mokuhyou_rule = [
        ["へ", "。"],
        ["へ", "$"]
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
        ["の", "か", "$"],
        ["いかに", "\?"],
        ["か", "。"],
        ["か", "$"],
        ["か", "\?"],
        ["は", "\?"],
        ["た", "\?"],
        ["だ", "\?"],
        [".*", "\?"],
        [".*", "\!", "\?"],
        ["と", "は", "$"],
        ["だ", "の", "か"],
        ["か", "どう", "か"],
        ["べし", "か"],   # べきか
        ["た", "か"],      # たろうか
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
            elif chek_w == "\!":
                chek_w = chek_w[1:]
            if ((rule in self.orth_chek_rule and re.match(chek_w, doc[pt].orth_))
                    or (rule not in self.orth_chek_rule and re.match(chek_w, doc[pt].lemma_))
                    or ng_word):
                if (ng_word and ((rule in self.orth_chek_rule and re.match(chek_w, doc[pt].orth_))
                                 or (rule not in self.orth_chek_rule and re.match(chek_w, doc[pt].lemma_)))):
                    continue
                if rule in self.orth_chek_rule and chek_w[0] == "." and doc[pt].orth_ == doc[pt].norm_:
                    continue
                baias = 0
                find = True
                for n_chek in chek:
                    if n_chek == "$":  # 文末
                        if pt + baias == len(doc):
                            break
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
        noun_ok_f = True

        for pt in range(sp, len(doc)):
            if len(doc) < pt:
                return ret
            if doc[sp].pos_ != "NOUN":
                noun_ok_f = False
            if doc[sp].pos_ == "NOUN" and noun_ok_f:
                if doc[pt].pos_ == "ADP":
                    noun_ok_f = False
            if doc[pt].pos_ in self.stop_pos and pt != sp:
                if not noun_ok_f or doc[pt].pos_ == "VERB":
                    if doc[pt].norm_ != "為る" and doc[pt].norm_ != "成る"  and doc[pt].norm_ != "有る" and doc[pt].norm_ != "こと" and doc[pt].pos_ != "PRON" and (doc[pt - 1].lemma_ != "を" or doc[pt].lemma_ != "する") and doc[pt - 1].pos_ != "NOUN":
                        break
                if doc[pt].tag_ == "補助記号-句点":
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

            # 引用
            self.rule_chek(self.innyou_rule, "<引用>", ret, pt, *doc)

            # 容易
            self.rule_chek(self.youi_rule, "<容易>", ret, pt, *doc)

            # 限定
            self.rule_chek(self.gentei_rule, "<限定>", ret, pt, *doc)

            # 目標
            self.rule_chek(self.mokuhyou_rule, "<目標>", ret, pt, *doc)

            # 可能
            self.rule_chek(self.kanou_rule, "<可能>", ret, pt, *doc)

            # 疑問
            self.rule_chek(self.gimon_rule, "<疑問>", ret, pt, *doc)
        return ret
