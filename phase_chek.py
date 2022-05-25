from chunker import ChunkExtractor
from verb_split import VerbSpliter
from phase_rule_dic import PhaseRule
class PhaseCheker:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word
        self.num_chunk = chunker.num_chunk
        self.compaound = chunker.compaound
        v_s = VerbSpliter()
        self.sub_verb_dic = v_s.sub_verb_dic
        rule = PhaseRule()
        self.kousou_dic = rule.kousou_dic
        self.kenkyuu_dic = rule.kenkyuu_dic
        self.kaihatsu_dic = rule.kaihatsu_dic
        self.jikken_dic = rule.jikken_dic
        self.seihin_dic = rule.seihin_dic
        self.koushin_dic = rule.koushin_dic
        self.tyuushi_dic = rule.tyuushi_dic
        self.sankaku_dic = rule.sankaku_dic
        self.riyou_dic = rule.riyou_dic
        self.soshiki_dic = rule.soshiki_dic
        self.renkei_dic = rule.renkei_dic
        self.tsuuchi_dic = rule.tsuuchi_dic
        self.tetsuzuki_dic = rule.tetsuzuki_dic
        self.sonota_dic = rule.sonota_dic


    def phase_chek(self, start, end, obj_tart, obj_end, *doc):
        ret = ''
        verv_word = self.compaound(start ,end, *doc)
        if(verv_word in self.kousou_dic):
            ret = ret + '<構想・目標>,'
        if(verv_word in self.kenkyuu_dic):
            ret = ret + '<研究>,'
        if(verv_word in self.kaihatsu_dic):
            ret = ret + '<開発>,'
        if(verv_word in self.jikken_dic):
            ret = ret + '<実験>,'
        if(verv_word in self.seihin_dic):
            ret = ret + '<製品・サービス化>,'
        if(verv_word in self.koushin_dic):
            ret = ret + '<更新>,'
        if(verv_word in self.tyuushi_dic):
            ret = ret + '<中止>,'
        if(verv_word in self.sankaku_dic):
            ret = ret + '<参画>,'
        if(verv_word in self.riyou_dic):
            ret = ret + '<利用>,'
        if(verv_word in self.soshiki_dic):
            ret = ret + '<組織変更>,'
        if(verv_word in self.renkei_dic):
            ret = ret + '<連携>,'
        if(verv_word in self.tsuuchi_dic):
            ret = ret + '<告知>,'
        if(verv_word in self.tetsuzuki_dic):
            ret = ret + '<手続き>,'
        if(verv_word in self.sonota_dic):
            ret = ret + '<その他>,'
        if(verv_word in self.sub_verb_dic and obj_tart):
            ret2 = self.phase_chek(obj_tart, obj_end, '', '', *doc)
            for ret3 in ret2.split(','):
                if ret3 not in ret:
                    ret = ret + ret3
            for pt in range(obj_tart, obj_end + 1):
                ret2 = self.phase_chek(pt, pt, '', '', *doc)
                for ret3 in ret2.split(','):
                    if ret3 not in ret:
                        ret = ret + ret3
        return ret.rstrip(',')



