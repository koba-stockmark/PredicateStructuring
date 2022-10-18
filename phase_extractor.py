import spacy
from phase_check import PhaseCheker
from data_dump import DataDumpSave
from pas_analysis import PasAnalysis


class PhaseExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """

        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル
        pas_model = PasAnalysis()
        self.pas_analysis = pas_model.pas_analysis
        phase_model = PhaseCheker()
        self.phase_get_and_set = phase_model.phase_get_and_set
        self.government_action_get_and_set = phase_model.government_action_get_and_set
        d_d_s = DataDumpSave()
        self.data_dump_and_save = d_d_s.data_dump_and_save
        self.data_dump_and_save2 = d_d_s.data_dump_and_save2
        self.data_dump_and_save3 = d_d_s.data_dump_and_save3
        self.text_treace = d_d_s.text_treace

    """
    フェーズの取得
    """

    def single_phase_extract(self, text):
        return self.phase_get(text, 0)



    """
    主述部と補助術部に別れた述語項構造の取得
    mode = 0 : フェーズチェク
    mode = 1 : 政府活動チェク
    mode = 2 : 政府HPチェク
    """

    def phase_get(self, text, mode):

        debug = False  # デバッグ用フラグ
        ret = ''
        ##########################################################################################################################################
        # 形態素解析
        ##########################################################################################################################################
        doc = self.nlp(text)  # 文章を解析
        if debug:
            self.text_treace(*doc)
        ##########################################################################################################################################
        # 述語項構造解析
        ##########################################################################################################################################
        pas_result = self.pas_analysis(debug, text, *doc)
        argument = pas_result[0]["argument"]
        predicate = pas_result[0]["predicate"]
        # デバッグ表示用解析データ
        if debug:
            ret = ret + pas_result[1]
        # デバッグ表示用解析データ
        if mode == 0:
            ##########################################################################################################################################
            #    主述部のフェイズチェック
            ##########################################################################################################################################
            single_phase = self.phase_get_and_set(predicate, argument, *doc)
            # デバッグ表示用解析データ
            if debug:
                ret = ret + self.data_dump_and_save2(text, argument, predicate)
                self.data_dump_and_save3(text, argument, predicate)
                print(single_phase)
                return ret
            # デバッグ表示用解析データ
            return single_phase
        if mode == 1 or mode == 2:
            ##########################################################################################################################################
            #    政府活動のチェックチェック
            ##########################################################################################################################################
            government_action = self.government_action_get_and_set(predicate, argument, mode, *doc)
            # デバッグ表示用解析データ
            if debug:
                ret = ret + self.data_dump_and_save2(text, argument, predicate)
                self.data_dump_and_save3(text, argument, predicate)
                print(government_action)
                return ret
            # デバッグ表示用解析データ
            return government_action
