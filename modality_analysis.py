"""
  モダリティ解析
"""
import re
from modality_rule_dic import ModalityRule

class ModalityAnalysis:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        self.modality_dic = ModalityRule()

################################

    # 文節区切り品詞
    stop_pos = [
        "VERB", "NOUN", "PUNCT", "PRON", "SYM", "NUM"
    ]

    # orth で比較必要する必要なあるルール
    orth_chek_rule_tag = ["<推論>", "<過去>", "<勧誘>", "<可能>", "<断定>", "<使役>", "<受け身>", "<否定>", "<仮定>"]

    ##########
    def rule_chek(self, entry, delete, sp, pt, *doc):
        del_f = False
        for chek in self.modality_dic.modality_rule:
            tag = chek["tag"]
            if tag == "<断定>" and doc[sp].pos_ != "NOUN" and doc[sp].pos_ != "ADJ":
                continue
            verb_in = False
            if pt != sp and (doc[pt].pos_ == "VERB" or doc[pt].pos_ == "AUX"):
                verb_in = True
            if tag == "<過去>":
                if doc[sp].pos_ != "NOUN" or verb_in or (len(doc) > sp + 1 and doc[sp + 1].lemma_ == "を") or (len(doc) > sp + 1 and doc[sp + 1].orth_ == "だっ"):
                    pass
                else:
                    continue
            baias = 0
            find = True
            for m_rule in chek["rule"]:
                baias = 0
                find = True
                for n_chek in m_rule:
                    not_f = False
                    lemma_chek = False
                    if n_chek[0] == "D":                # 削除
                        del_f = True
                        n_chek = n_chek[1:]
                    if n_chek[0] == "#":                # orth != norm
                        if doc[pt].orth_[-2:] == doc[pt].norm_[-2:]:
                            del_f = False
                            find = False
                            break
                        n_chek = n_chek[1:]
                    if n_chek[0] == "%":                # lemma == norm
                        lemma_chek = True
                        if doc[pt].lemma_[-2:] != doc[pt].norm_[-2:]:
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
                          ("." not in n_chek and "*" not in n_chek) and
                          ((tag in self.orth_chek_rule_tag and not lemma_chek and n_chek == doc[pt + baias].orth_) or
                           ((tag not in self.orth_chek_rule_tag or lemma_chek) and n_chek == doc[pt + baias].lemma_))):
                            if not_f:
                                find = False
                                del_f = False
                                break
                    elif (len(doc) > pt + baias and
                          ("." in n_chek or "*" in n_chek) and
                          ((tag in self.orth_chek_rule_tag and not lemma_chek and re.fullmatch(n_chek, doc[pt + baias].orth_)) or
                           ((tag not in self.orth_chek_rule_tag or lemma_chek) and re.fullmatch(n_chek, doc[pt + baias].lemma_)))):
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
                    if tag not in entry:
                        if del_f:
                            delete.append(tag)
                        else:
                            entry.append(tag)
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
                    if doc[pt].norm_ != "為る" and doc[pt].norm_ != "成る" and doc[pt].norm_ != "来る" and doc[pt].norm_ != "居る" and doc[pt].norm_ != "見る"  and doc[pt].norm_ != "有る" and doc[pt].norm_ != "こと" and doc[pt].pos_ != "PRON" and (doc[pt - 1].lemma_ != "を" or doc[pt].lemma_ != "する") and doc[pt - 1].pos_ != "NOUN":
                        if len(doc) <= pt + 1 or (len(doc) > pt + 1 and doc[pt + 1].lemma_ != "\?" and doc[pt + 1].lemma_ != "?"):
                            break
                if doc[pt].tag_ == "補助記号-句点":
                    break
            self.rule_chek(ret, delete, sp, pt, *doc)
        for del_w in delete:
            if del_w in ret:
                ret.remove(del_w)
        return ret
