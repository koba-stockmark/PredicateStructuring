import spacy
import json
import copy
import sys

#sys.path.append('../PredicateStructuring')

from chunker import ChunkExtractor
from data_dump import DataDumpSave
from phase_extractor import PhaseExtractor

class GovernmentNewsAnalysis:

    debug = False

    ##########################################################################################################################################
    #    主述部のフェイズチェック
    ##########################################################################################################################################

    def __init__(self):

        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        chnker = ChunkExtractor()
        self.num_chunk = chnker.num_chunk
        d_s = DataDumpSave()
        self.text_treace = d_s.text_treace
        p_e = PhaseExtractor()
        self.phase_get = p_e.phase_get

    seifu_busho = ["省", "庁", "部", "課", "局", "グループ", "室", "官房"]


    ##########################################################################################################################################
    # ニュースからの政府活動のチェック
    ##########################################################################################################################################

    def government_phase_extract(self, text):
        return self.phase_get(text, 1)

    ##########################################################################################################################################
    # 政府発行ニュースからの政府活動の取得
    #
    #    政府刊行物からの取得で主語は政府であることが前提でチェックを行わない。
    #    入力は複数の文の場合があるのでここでは「。」で文を分割、最初に政府活動が取得できた時点でそれを答えとする。
    ##########################################################################################################################################

    def government_action_extract(self, text):
        pre_ret = ""
        a_text = ""
        for c_text in text.split("。"):
            if c_text.endswith("いう") or c_text.endswith("号"):
                if a_text:
                    a_text = a_text + c_text + "。"
                else:
                    a_text = c_text + "。"
                continue
            else:
                if a_text:
                    a_text = a_text + c_text + "。"
                else:
                    a_text = c_text + "。"
            ret = self.phase_get(a_text, 2)
            if ret:
                return ret
        #                    if "その他" not in ret:
        #                        return ret
        #                    pre_ret = ret
        return pre_ret


    ##########################################################################################################################################
    #    部署か否かのチェック
    ##########################################################################################################################################

    def busho_chek(self, word):
        for check in self.seifu_busho:
            if check in word:
                return True
        return False

    ##########################################################################################################################################
    #    部署情報のチャンキング
    ##########################################################################################################################################

    def word_chunk(self, pt, *doc):
        ret = doc[pt].orth_

        for i in reversed(range(0, pt)):
            if doc[i].lemma_ == "：":
                break
            if(doc[i].head.i == pt or doc[i].head.i == doc[pt].head.i or i <= doc[i].head.i <= pt) and "人名" not in doc[i].tag_:
                ng_word = False
                if doc[i].lemma_ == '　':
                    break
                for check in self.seifu_busho:
                    if doc[i].orth_.endswith(check):
                        ng_word = True
                if not ng_word:
                    if ret.endswith("省"):
                        break
                    ret = doc[i].orth_ + ret
                else:
                    break
            else:
                ok_word = False
                for check in self.seifu_busho:
                    if doc[i].head.orth_.endswith(check):
                        ok_word = True
                if ok_word:
                    ng_word = False
                    if doc[i].lemma_ == '　' or doc[i].pos_ == "PUNCT":
                        break
                    for check in self.seifu_busho:
                        if doc[i].orth_.endswith(check):
                            ng_word = True
                    if not ng_word:
                        if ret.endswith("省"):
                            break
                        ret = doc[i].orth_ + ret
                else:
                    break
        return ret

    ##########################################################################################################################################
    #    部署情報の分解とチャンキング
    #      テキストから部署部分を切り出す
    ##########################################################################################################################################

    def busho_get(self, text):
        busho = ""
        if text:
            ##########################################################################################################################################
            # 形態素解析
            ##########################################################################################################################################
            doc = self.nlp(text)  # 文章を解析
            if self.debug:
                self.text_treace(*doc)
            for token in doc:
                for check in self.seifu_busho:
                    if check in token.lemma_ and "人名" not in token.tag_:
                        chunk_word = self.word_chunk(token.i, *doc)
                        chunk_word = chunk_word.lstrip()
                        chunk_word = chunk_word.lstrip("（")
                        if "省エネルギー" == chunk_word:
                            continue
                        if busho:
                            busho = busho + ',' + chunk_word
                        else:
                            busho = chunk_word
        return busho


    ##########################################################################################################################################
    #    政府発行ニュースのパースと内容分類
    ##########################################################################################################################################
#    error_id = ["82638573"]

    def government_news_analysis(self, new_doc):
        with open(new_doc, 'r') as f:
            input_news = json.load(f)
            o_text = ""
            out_data = []
            news_data = {}
            for row in input_news:
                d_id = row["id"]
#                if self.debug:
#                    if d_id not in self.error_id:
#                        continue
                title = row["preprocessed_title"]
#                print(row)
                busho_f = 0
                busho = ""
                pre_text = ""
                for text in row["text"].split("\n"):
                    if busho_f and "。" in text:
                        busho_f = busho_f - 1
                    if not o_text and "。" in text:
                        o_text = text
                    if (busho_f and len(text) > 4 and self.busho_chek(text) and
                            "一覧" not in text and "事務局" not in text and "担当課" not in text and
                            "省令" not in text and "部会" not in text and "部門" not in text and
                            "部品" not in text and "課題" not in text and "等へ" not in text and
                            ("。" not in text or (self.busho_chek(text) or "〒" in text))):
                        busho = text
                        busho_f = False
                    if not busho and ("お問合せ" in text or "担当" == text.lstrip()) and "担当大臣" not in text and "担当副大臣" not in text and text.count("。") < 2:
                        pre_text = text
                        busho_f = 3    # その後ｎ行以内に組織記述を探す
                if not busho and self.busho_chek(pre_text):
                    busho = pre_text
                news_data["id"] = d_id
                news_data["soshiki"] = row["media_name"]
                busho_t = busho.lstrip()
                news_data["busho"] = self.busho_get(busho_t)
                news_data["title"] = title.lstrip()
                news_data["title_type"] = self.government_action_extract(title.lstrip())
                news_data["head"] = o_text.lstrip()
                news_data["head_type"] = self.government_action_extract(o_text.lstrip())
                out_data.append(copy.deepcopy(news_data))

                if self.debug:
                    print(" id = %s \n busho = %s \n title = %s \n title_type = %s \n text = %s \n text_type = %s \n" % (news_data["id"] , news_data["busho"], news_data["title"], news_data["title_type"], news_data["head"], news_data["head_type"]))
                o_text = ""
            json_file = open("news_out.json", mode="w")
            json.dump(out_data, json_file, indent=2, ensure_ascii=False)
            json_file.close()
