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
    # 命令
    meirei_rule = [
        ["活用=命令形"],
        ["活用=終止形", "な"]
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
        ["活用=連用形", "た"],
        ["活用=連用形", "だ"]
    ]
    # 否定
    hitei_rule = [
        ["ず"],
        ["ぬ"],
        ["ない"],
        ["なかっ"],
        ["活用=終止形", "な"],
        ["Dいい", "じゃ", "ない"]    # いいじゃない　は外す
    ]
    # 意思
    ishi_rule = [
        ["たい"],
#        ["活用=終止形", "よう"],
#        ["活用=連体形", "よう"],
        ["期待", "する"],
        ["ほしい"]
    ]
    # 勧誘
    kanyuu_rule = [
        ["活用=意志推量形"],
        ["ば", "いい"],
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
        ["ば"],
        ["活用=連用形", "たら"]
    ]
    # 感情付与
    kanjyou_rule = [
        ["活用=終止形", "ね"],
        ["活用=終止形", "よ"]
    ]
    # 容易
    youi_rule = [
        ["やすい"]
    ]
    # 困難
    konnann_rule = [
        ["にくい"]
    ]
    # 限定
    gentei_rule = [
        ["だけ"],
        ["まで"]
    ]
    # 当然
    touzen_rule = [
        ["べから"],
        ["べく"],
        ["べし"],
        ["べき"]
    ]
    # 過剰
    kajyou_rule = [
        [".*すぎる"],
        ["すぎる"]
    ]
    # 使役
    shieki_rule = [
        ["させる"],
        ["活用=サ行変格;未然形-サ", "せ"],
        ["活用=サ行変格;未然形-サ", "せる"]
    ]
    # 受け身
    ukemi_rule = [
        [".*か", "れ"],
        [".*か", "れる"],
        [".*が", "れ"],
        [".*が", "れる"],
        [".*さ", "れ"],
        [".*さ", "れる"],
        [".*ざ", "れ"],
        [".*ざ", "れる"],
        [".*た", "れ"],
        [".*た", "れる"],
        [".*だ", "れ"],
        [".*だ", "れる"],
        [".*な", "れ"],
        [".*な", "れる"],
        [".*は", "れ"],
        [".*は", "れる"],
        [".*ば", "れ"],
        [".*ば", "れる"],
        [".*ま", "れ"],
        [".*ま", "れる"],
        [".*や", "れ"],
        [".*や", "れる"],
        [".*ら", "れ"],
        [".*ら", "れる"],
        [".*わ", "れ"],
        [".*わ", "れる"]
    ]
    # 試行
    sikou_rule = [
        [".*て", "みる"]
    ]
    # 継続
    keizoku_rule = [
        [".*て", "いる"]
    ]
    # 可能 [#] は [norm != orth] が条件でのorth
    kanou_rule = [
#        ["!する", "れる"],
        ["D.*さ", "#.*れる"],
        ["D.*あ", "ない"],
        ["D.*か", "ない"],
        ["D.*が", "ない"],
        ["D.*さ", "ない"],
        ["D.*ざ", "ない"],
        ["D.*た", "ない"],
        ["D.*だ", "ない"],
        ["D.*な", "ない"],
        ["D.*ば", "ない"],
        ["D.*ま", "ない"],
        ["D.*や", "ない"],
        ["D.*ら", "ない"],
        ["D.*わ", "ない"],
        ["できる"],
        ["でき", "た"],
        ["られる"],
        ["#.*える"],
        ["#.*ける"],
        ["#.*げる"],
        ["#.*せる"],
        ["#.*ぜる"],
        ["#.*てる"],
        ["#.*でる"],
        ["#.*ねる"],
        ["#.*べる"],
        ["#.*める"],
        ["#.*れる"],
        ["#.*え", "ず"],
        ["#.*け", "ず"],
        ["#.*げ", "ず"],
        ["#.*せ", "ず"],
        ["#.*ぜ", "ず"],
        ["#.*て", "ず"],
        ["#.*で", "ず"],
        ["#.*ね", "ず"],
        ["#.*べ", "ず"],
        ["#.*め", "ず"],
        ["#.*れ", "ず"],
        ["D活用=サ行変格;未然形-サ", "活用=未然形", "ない"],
        ["活用=未然形", "ない"]
    ]
    # 疑問
    gimon_rule = [
        ["の", "か", "。"],
        ["の", "か", "、"],
        ["の", "か", "\?"],
        ["の", "か", "\("],
        ["の", "か", "$"],
        ["いかに", "\?"],
        ["か", "。"],
        ["か", "$"],
        ["か", "\?"],
        ["か", "？"],
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
        ["だ", "か"],      # だろうか
        ["なぜ", "$"],
        ["なぜ", "/?"],
        ["なぜ", "？"],
        ["なぜ", "/!"],
        ["なぜ", "！"],
        ["なぜ", "。"]
    ]

    # 引用
    innyou_rule = [
        ["より"]
    ]
    # 目標
    mokuhyou_rule = [
        ["へ", "。"],
        ["へ", "$"]
    ]
    # こと
    koto_rule = [
        ["活用=連体形", "こと"]
    ]
    # とは
    towa_rule = [
        ["と", "は", "。"],
        ["と", "は", "\?"],
        ["と", "は", "？"],
        ["と", "は", "$"]
    ]

    # 文節区切り品詞
    stop_pos = [
        "VERB", "NOUN", "PUNCT", "PRON", "SYM", "NUM"
    ]

    # orth で比較必要する必要なあるルール
    orth_chek_rule = [suiron_rule, kako_rule, kanyuu_rule, kanou_rule, dantei_rule, shieki_rule, ukemi_rule, hitei_rule, katei_rule]

    ##########
    def rule_chek(self, rule, tag,  ret, delete, pt, *doc):
        del_f = False
        for chek in rule:
            baias = 0
            find = True
            for n_chek in chek:
                not_f = False
                if n_chek[0] == "D":                # 削除
                    del_f = True
                    n_chek = n_chek[1:]
                if n_chek[0] == "#":                # orth == norm
                    if doc[pt].orth_[-2:] == doc[pt].norm_[-2:]:
                        del_f = False
                        find = False
                        break
                    n_chek = n_chek[1:]
                if n_chek == "$":                  # 文末
                    if pt + baias == len(doc):
                        break
                elif n_chek[0] == "!":            # 否定
                    n_chek = n_chek[1:]
                    not_f = True
                if n_chek.startswith("活用"):      # 活用
                    if doc[pt].morph.get("Inflection") and n_chek[3:] in doc[pt].morph.get("Inflection")[0]:
                        if not_f:
                            find = False
                            del_f = False
                            break
                    else:
                        find = False
                        del_f = False
                        break
                elif (len(doc) > pt + baias and
                        ((rule in self.orth_chek_rule and re.fullmatch(n_chek, doc[pt + baias].orth_)) or
                        (rule not in self.orth_chek_rule and re.fullmatch(n_chek, doc[pt + baias].lemma_)))):
                    if not_f:
                        find = False
                        del_f = False
                        break
                else:
                    if not not_f:
                        find = False
                        del_f = False
                        break
                baias = baias + 1
            if find:
                if tag not in ret:
                    if del_f:
                        delete.append(tag)
                    else:
                        ret.append(tag)
            del_f = False
        return

    ##########
    def modality_get(self, sp, *doc):
        ret = []
        delete = []
        verb_in = False
        noun_ok_f = True

        for pt in range(sp, len(doc)):
            if len(doc) < pt:
                return ret
#            if len(doc) > pt + 1 and doc[pt + 1].lemma_ == "こと":
#                return ret
            if doc[sp].pos_ != "NOUN":
                noun_ok_f = False
            if doc[sp].pos_ == "NOUN" and noun_ok_f:
                if doc[pt].pos_ == "ADP":
                    noun_ok_f = False
            if doc[pt].pos_ in self.stop_pos and pt != sp:
                if not noun_ok_f or doc[pt].pos_ == "VERB":
                    if doc[pt].norm_ != "為る" and doc[pt].norm_ != "成る" and doc[pt].norm_ != "居る" and doc[pt].norm_ != "見る"  and doc[pt].norm_ != "有る" and doc[pt].norm_ != "こと" and doc[pt].pos_ != "PRON" and (doc[pt - 1].lemma_ != "を" or doc[pt].lemma_ != "する") and doc[pt - 1].pos_ != "NOUN":
                        if len(doc) <= pt + 1 or (len(doc) > pt + 1 and doc[pt + 1].lemma_ != "\?" and doc[pt + 1].lemma_ != "?"):
                            break
                if doc[pt].tag_ == "補助記号-句点":
                    break
            if pt != sp and (doc[pt].pos_ == "VERB" or doc[pt].pos_ == "AUX"):
                verb_in = True

            # 断定
            if doc[sp].pos_ == "NOUN":
                self.rule_chek(self.dantei_rule, "<断定>",  ret, delete, pt, *doc)

            # 過去
            if doc[sp].pos_ != "NOUN" or verb_in or (len(doc) > sp + 1 and doc[sp + 1].lemma_ == "を") or (len(doc) > sp + 1 and doc[sp + 1].orth_ == "だっ"):
                self.rule_chek(self.kako_rule, "<過去>",  ret, delete, pt, *doc)

            # 命令
            self.rule_chek(self.meirei_rule, "<命令>",  ret, delete, pt, *doc)

            # 否定
            self.rule_chek(self.hitei_rule, "<否定>",  ret, delete, pt, *doc)

            # 意思・願望
            self.rule_chek(self.ishi_rule, "<意思・願望>",  ret, delete, pt, *doc)

            # 勧誘
            self.rule_chek(self.kanyuu_rule, "<勧誘>",  ret, delete, pt, *doc)

            # 推量
            self.rule_chek(self.suiron_rule, "<推量>",  ret, delete, pt, *doc)

            # 仮定
            self.rule_chek(self.katei_rule, "<仮定>",  ret, delete, pt, *doc)

            # 引用
            self.rule_chek(self.innyou_rule, "<引用>",  ret, delete, pt, *doc)

            # 容易
            self.rule_chek(self.youi_rule, "<容易>",  ret, delete, pt, *doc)

            # 困難
            self.rule_chek(self.konnann_rule, "<困難>",  ret, delete, pt, *doc)

            # 限定
            self.rule_chek(self.gentei_rule, "<限定>",  ret, delete, pt, *doc)

            # 当然
            self.rule_chek(self.touzen_rule, "<当然>",  ret, delete, pt, *doc)

            # 過剰
            self.rule_chek(self.kajyou_rule, "<過剰>",  ret, delete, pt, *doc)

            # 感情付与
            self.rule_chek(self.kanjyou_rule, "<感情付与>",  ret, delete, pt, *doc)

            # 目標
            self.rule_chek(self.mokuhyou_rule, "<目標>",  ret, delete, pt, *doc)

            # 使役
            self.rule_chek(self.shieki_rule, "<使役>",  ret, delete, pt, *doc)

            # 受け身
            self.rule_chek(self.ukemi_rule, "<受け身>",  ret, delete, pt, *doc)

            # 試行
            self.rule_chek(self.sikou_rule, "<試行>",  ret, delete, pt, *doc)

            # 継続
            self.rule_chek(self.keizoku_rule, "<継続>",  ret, delete, pt, *doc)

            # 可能
            self.rule_chek(self.kanou_rule, "<可能>",  ret, delete, pt, *doc)

            # 疑問
            self.rule_chek(self.gimon_rule, "<疑問>",  ret, delete, pt, *doc)

            # こと
            self.rule_chek(self.koto_rule, "<こと>", ret, delete, pt, *doc)

            # とは
            self.rule_chek(self.towa_rule, "<とは>", ret, delete, pt, *doc)

        for del_w in delete:
            if del_w in ret:
                ret.remove(del_w)
        return ret
