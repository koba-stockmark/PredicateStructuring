import spacy
from spacy.symbols import obj
from chunker import ChunkExtractor
from subject_get import SubjectExtractor
from parallel_get import ParallelExtractor
from verb_split import VerbSpliter
from phase_chek import PhaseCheker
from kanyouku_check import KanyoukuExtractor
from verb_phrase_get import VerbPhraseExtractor
from main_verb_chek import MainVerbChek
from predicate_get import PredicateGet
from data_dump import DataDumpSave

class PasExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """


        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.verb_chunk = chunker.verb_chunk
        self.case_get = chunker.case_get
        self.compaound = chunker.compaound
        s_g = SubjectExtractor()
        self.subject_get = s_g.subject_get_from_object
        self.rentai_check = s_g.rentai_check
        p_g = ParallelExtractor()
        self.para_get = p_g.para_get
        v_s = VerbSpliter()
        self.verb_devide = v_s.verb_devide
        self.sub_verb_chek = v_s.sub_verb_chek
        self.object_devide = v_s.object_devide
        p_c = PhaseCheker()
        self.phase_chek = p_c.phase_chek
        self.single_phase_get = p_c.single_phase_get
        k = KanyoukuExtractor()
        self.kanyouku_chek = k.kanyouku_chek
        self.kanyouku_get = k.kanyouku_get
        v_x = VerbPhraseExtractor()
        self.predicate_phrase_get = v_x.predicate_phrase_get
        m_v_c = MainVerbChek()
        self.main_verb_chek = m_v_c.main_verb_chek
        p_g = PredicateGet()
        self.predicate_get = p_g.predicate_get
        d_d_s = DataDumpSave()
        self.data_dump_and_save = d_d_s.data_dump_and_save
        self.data_dump_and_save2 = d_d_s.data_dump_and_save2

    """
    フェーズの取得
    """

    def phase_get(self, text):
        return self.pas_get(text)

    """
    述部の探索
    """
    def predicate_search(self, *doc):
        for token in doc:
            if(token.pos_ == 'VERB'):
                self.predicate_phrase_get(token.i, *doc)
        return ret

    """
    主述部と補助術部に別れた述語項構造の取得
    """

    def pas_get(self, text):

        ret = ''
        dummy_subj = {}
        para_subj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析
        verb_end = -1
        pre_rentai_subj = False
        predicate_id = 0
        single_phase = ''

        for token in doc:
            subject_w = ''
            sub_verb_w = ''
            sub_verb = {}
            #
            #  述部の検索
            #
            if token. i <= verb_end:
                continue
            verb = self.predicate_get(token.i, *doc)
            if not verb:
                continue
            verb_w = verb["lemma"]
            verb_end = verb["lemma_end"]
            modality_w = verb["modality"]
            rule_id = verb["rule_id"]
            verb_rule_id = rule_id
            if len(doc) > verb_end + 1 and doc[verb_end + 1].norm_ == '為る':
                verb_end = verb_end + 1
            #
            #  主語の検索
            #
            ret_subj = self.subject_get(token.i, verb["lemma_end"], *doc)
            if not token.dep_ == "nsubj" or doc[ret_subj['lemma_end'] + 1].lemma_ != 'も':  # 〇〇も　の例外処理でsubjを目的語にしている場合は自分自身をsubjにしない（省略されていると考える）
                subject_w = ret_subj['lemma']

            if ((ret_subj["lemma_start"] <= verb["lemma_start"] and ret_subj["lemma_end"] >= verb["lemma_end"]) or
                (ret_subj["lemma_start"] <= verb["lemma_start"] and ret_subj["lemma_start"] >= verb["lemma_end"]) or
                (ret_subj["lemma_end"] <= verb["lemma_start"] and ret_subj["lemma_end"] >= verb["lemma_end"])):
                continue

            # 主語の表層格の取得
            subj_case = self.case_get(ret_subj['lemma_end'], *doc)

            # 省略主語のセット
            if subject_w:
                if (self.rentai_check(verb["lemma_end"], *doc) or (doc[verb["lemma_end"]].morph.get("Inflection") and '連体形' in doc[verb["lemma_end"]].morph.get("Inflection")[0])) and verb["lemma_start"] < ret_subj["lemma_start"]:
                    pre_rentai_subj = True
                else:
                    pre_rentai_subj = False
                    dummy_subj["lemma"] = ret_subj["lemma"]
                    dummy_subj["lemma_start"] = ret_subj["lemma_start"]
                    dummy_subj["lemma_end"] = ret_subj["lemma_end"]
                    dummy_subj["case"] = subj_case
            elif pre_rentai_subj:   # 前に出てきた主語が連体形から生成されている場合は省略の保存をクリア
                dummy_subj.clear()

            # 主語の並列化
            if subject_w:
                para_subj = self.para_get(ret_subj['lemma_start'], ret_subj['lemma_end'], *doc)
            #
            #  つながる項の検索
            #
            find_f = False
            argument_map = []
            for i in range(0, verb["lemma_start"]):
                if doc[i].dep_ != "nsubj" and ret_subj["lemma"] and i >= ret_subj["lemma_start"] and i <= ret_subj["lemma_end"]:  # 主語は対象外
                    continue
                if ((doc[i].dep_ == "obj" and doc[i].head.dep_ != "obj") or
                        (doc[i].dep_ == "obl" and
                         (doc[i].norm_ != 'そこ' and doc[i].norm_ != 'それ') and
                         doc[i].tag_ != '名詞-普通名詞-副詞可能' and (doc[i].norm_ != '度' or doc[i - 1].pos_ == 'NUM'))):  # この度　はNG
                    if doc[i].head.i < verb["lemma_start"] or doc[i].head.i > verb["lemma_end"]:  # 述部に直接かからない
                        #                        continue
                        #####  要検討　条件をもっと追加しないと余計なものができる
                        if doc[i].head.head.i == token.i or (doc[i].head.morph.get("Inflection") and '連用形' not in doc[i].head.morph.get("Inflection")[0]):  # 連用形接続でもつながらない
                            if (doc[doc[i].head.i + 1].tag_ != '接尾辞-形容詞的' and (doc[doc[i].head.i].tag_ != '名詞-普通名詞-副詞可能' or doc[doc[i].head.i].lemma_ == 'ため' or doc[doc[i].head.i].lemma_ == '前')) or doc[i].head.head.pos_ == 'NOUN':
                                continue
                        elif doc[i].head.pos_ == 'VERB' and doc[i].head.head.i == verb["lemma_start"] and rule_id == 28:  # rule_id 28 の特別処理　「ツールをより使いやすく、バージョンアップ」
                            pass
                        else:
                            continue
                        ####
                    find_f = True
                    argument_map += [i]

            #
            #  PASの作成
            #
            argument = []
            #
            #  主語のセット
            #
            if subject_w:
                ret_subj["case"] = subj_case
                ret_subj["dummy"] = False
                ret_subj["subject"] = True
                argument.append(ret_subj)
                if para_subj and para_subj[0]['lemma']:
                    for p_subj in para_subj:
                        p_subj["case"] = subj_case
                        p_subj["dummy"] = False
                        p_subj["subject"] = True
                        argument.append(p_subj)
            elif dummy_subj:
                dummy_subj["dummy"] = True
                dummy_subj["subject"] = True
                argument.append(dummy_subj)
            # 項のセット
            argument_id = 0
            for i in range(0, verb["lemma_start"]):
                ret_obj = {'lemma': '', 'lemma_start': -1, 'lemma_end': -1}
                rule_id = verb_rule_id
                para_obj = [{'lemma': '', 'lemma_start': -1, 'lemma_end': -1}]
                #
#                if(find_f and i in argument_map) or (not find_f and  doc[i].dep_ == "nsubj" and i >= ret_subj['lemma_start'] and i <= ret_subj['lemma_end']):
                if(find_f and i in argument_map):
#                    if(renyou_f and case == 'を'):doc[i].dep_ == "nsubj"
#                        continue
                    #
                    # 項の取得
                    #
                    if find_f:
                        ret_obj = self.num_chunk(i, *doc)
                        #
                        # 項の並列処理
                        #
                        para_obj = self.para_get(ret_obj['lemma_start'], ret_obj['lemma_end'], *doc)
                    elif verb["lemma"] == 'ため':     # ためだけの述部はNGとする
                        continue
                    #
                    # 格情報の取得
                    #
                    if ret_obj:
                        case = self.case_get(ret_obj['lemma_end'], *doc)
                    else:
                        case = self.case_get(i, *doc)
                    if not case and doc[i].tag_ == '名詞-普通名詞-サ変可能':
                        continue
                    #
                    # 項のセット
                    #
                    ret_obj["case"] = case
                    ret_obj["subject"] = False
                    ret_obj["id"] = argument_id
                    argument_id = argument_id + 1
                    argument.append(ret_obj)
                    if para_obj and para_obj[0]["lemma"]:
                        for p_obj in para_obj:
                            p_obj["case"] = case
                            p_obj["subject"] = False
                            p_obj["id"] = argument_id
                            argument_id = argument_id + 1
                            argument.append(p_obj)
                    #
                    # 省略主語が項とかぶった場合は諸略主語を削除
                    #
                    if dummy_subj and ret_obj["lemma_start"] <= dummy_subj["lemma_start"] and ret_obj["lemma_end"] >= dummy_subj["lemma_end"]:
                        for subj in argument:
                            if subj["subject"] and subj["dummy"]:
                                argument.remove(subj)
                                break

            # データダンプ
            if find_f:
                ret = ret + self.data_dump_and_save(text, argument, verb)
            ##########################################################################################
            #  メイン術部の分割処理
            ##########################################################################################
            main_verb = False
            phase = ''
            predicate = {}
            for re_arg in argument:
                re_arg["phase"] = ''
                case = re_arg["case"]
                if case == 'は' or case == 'が':
                    if len(argument) != 1:
                        continue
                ##########################################################################################################################################
                #    メイン述部の判断
                #              目的語のかかる先が　メイン述部　か　メイン述部＋補助述部　かの判断
                #              出力は　目的語　＋　メイン述部　＋　補助述部　にする
                ##########################################################################################################################################
                v_rule_id = self.main_verb_chek(token.i, *doc)
                if v_rule_id > 0:
                    rule_id = v_rule_id
                    main_verb = True

                ##########################################################################################################################################
                #   述部加工処理用に現在の述部を記憶する
                ##########################################################################################################################################
                memo_verb ={}
                memo_verb["lemma"] = verb["lemma"]
                memo_verb["lemma_start"] = verb["lemma_start"]
                memo_verb["lemma_end"] = verb["lemma_end"]

                ##########################################################################################################################################
                #   主述部と補助術部の判断
                ##########################################################################################################################################
                sub_verb_is_original = True
                if self.sub_verb_chek(verb_w) and verb:
                    sub_verb_is_original = False
                    sub_verb_w = verb_w
                    sub_verb["lemma"] = verb["lemma"]
                    sub_verb["lemma_start"] = verb["lemma_start"]
                    sub_verb["lemma_end"] = verb["lemma_end"]
                    verb_w = ''
                    verb["lemma"] = ''
                    verb["lemma_start"] = -1
                    verb["lemma_end"] = -1

                ##########################################################################################################################################
                #    目的語を述部と分割
                ##########################################################################################################################################

                if re_arg and not verb_w:
                    dev_obj = self.object_devide(re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                    if dev_obj["verb"]:
                        re_arg["lemma"] = dev_obj["object"]
                        re_arg["lemma_end"] = dev_obj["verb_start"] - 1
                        verb_w = dev_obj["verb"]
                        verb["lemma"] = verb_w
                        verb["lemma_start"] = dev_obj["verb_start"]
                        verb["lemma_end"] = dev_obj["verb_end"]
                    if not dev_obj["object"]:
                        re_arg["lemma"] = ''
                        re_arg["lemma_start"] = -1
                        re_arg["lemma_end"] = -1

                ##########################################################################################################################################
                #    複合術部のメインと補助への分割
                ##########################################################################################################################################
                dev_verb = {}
                if verb and verb['lemma']:
                    dev_verb = self.verb_devide(verb["lemma_start"], verb["lemma_end"], *doc)
                elif sub_verb and sub_verb['lemma']:
                    dev_verb = self.verb_devide(sub_verb["lemma_start"], sub_verb["lemma_end"], *doc)
                if dev_verb and dev_verb["sub_verb"]:  # 補助述部がある
                    verb_w = dev_verb["verb"]
                    verb["lemma"] = verb_w
                    verb["lemma_start"] = dev_verb["verb_start"]
                    verb["lemma_end"] = dev_verb["verb_end"]
                    if verb_w and sub_verb_w and sub_verb_is_original:  # 主述部と補助術部の療法がる場合は取得した補助術部はもとの補助術部に追加する
                        sub_verb_w = dev_verb["sub_verb"] + sub_verb_w
                        sub_verb["lemma"] = sub_verb_w
                        sub_verb["lemma_start"] = dev_verb["sub_verb_start"]
                    else:
                        sub_verb_w = dev_verb["sub_verb"]
                        sub_verb["lemma"] = sub_verb_w
                        sub_verb["lemma_start"] = dev_verb["sub_verb_start"]
                        sub_verb["lemma_end"] = dev_verb["sub_verb_end"]

                ##########################################################################################################################################
                #    目的語からの主述部がない場合は補助術部を主述部へもどす
                ##########################################################################################################################################
                if not verb_w and sub_verb_w:  # 目的語からの主述部がない場合は補助術部を主述部へもどす
                    verb_w = sub_verb_w
                    sub_verb_w = ''
                    verb["lemma"] = sub_verb["lemma"]
                    verb["lemma_start"] = sub_verb["lemma_start"]
                    verb["lemma_end"] = sub_verb['lemma_end']

                ##########################################################################################################################################
                #    最終的な述部の整理
                ##########################################################################################################################################
                predicate["id"] = predicate_id
                predicate["lemma"] = verb["lemma"]
                predicate["lemma_start"] = verb["lemma_start"]
                predicate["lemma_end"] = verb["lemma_end"]
                predicate["orth"] = verb_w
                predicate["modality"] = ', '.join([str(x) for x in modality_w])
                predicate["rule_id"] = rule_id
                if sub_verb and sub_verb_w:
                    predicate["sub_lemma"] = sub_verb["lemma"]
                    predicate["sub_lemma_start"] = sub_verb["lemma_start"]
                    predicate["sub_lemma_end"] = sub_verb["lemma_end"]
                    predicate["sub_orth"] = sub_verb_w
                else:
                    predicate["sub_lemma"] = ''
                    predicate["sub_lemma_start"] = ''
                    predicate["sub_lemma_end"] = ''
                    predicate["sub_orth"] = ''
                predicate_id = predicate_id + 1

                ##########################################################################################################################################
                #    主述部のフェイズチェック
                ##########################################################################################################################################
                if main_verb:
                    phase = self.phase_chek(verb["lemma_start"], verb["lemma_end"], re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                    if sub_verb:
                        add_phase = self.phase_chek(sub_verb["lemma_start"], sub_verb["lemma_end"],re_arg['lemma_start'], re_arg['lemma_end'], *doc)
                        for append in add_phase.split(','):  # 重複は登録しない
                            if append != '<その他>' and append != '<告知>' and append not in phase:
                                phase = phase + ',' + append
                    re_arg["phase"] = phase

                single_phase = self.single_phase_get(phase)
            # データダンプ
            if (main_verb):
                ret = ret + self.data_dump_and_save2(text, argument, predicate)
        return ret
##        return single_phase



    def text_treace(self, text):
        """
        デバッグ用に結果を表示
        """
        doc = self.nlp(text)

        for token in doc:
            print(
                token.i,
                token.orth_,
                token.lemma_,
                token.norm_,
                token.morph.get("Reading"),
                token.pos_,
                token.morph.get("Inflection"),
                token.tag_,
                token.dep_,
                token.head.i,
            )
