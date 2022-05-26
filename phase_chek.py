from chunker import ChunkExtractor
from sub_verb_dic import SubVerbDic
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



    def phase_chek(self, start, end, obj_tart, obj_end, *doc):
        rule = PhaseRule()
        s_v_dic = SubVerbDic()
        ret = ''
        verv_word = self.compaound(start ,end, *doc)
        if(verv_word in rule.kousou_dic):
            ret = ret + '<構想・目標>,'
        if(verv_word in rule.kenkyuu_dic):
            ret = ret + '<研究>,'
        if(verv_word in rule.kaihatsu_dic):
            ret = ret + '<開発>,'
        if(verv_word in rule.jikken_dic):
            ret = ret + '<実験>,'
        if(verv_word in rule.seihin_dic):
            ret = ret + '<製品・サービス化>,'
        if(verv_word in rule.koushin_dic):
            ret = ret + '<更新>,'
        if(verv_word in rule.tyuushi_dic):
            ret = ret + '<中止>,'
        if(verv_word in rule.sankaku_dic):
            ret = ret + '<参画>,'
        if(verv_word in rule.riyou_dic):
            ret = ret + '<利用>,'
        if(verv_word in rule.soshiki_dic):
            ret = ret + '<組織変更>,'
        if(verv_word in rule.renkei_dic):
            ret = ret + '<連携>,'
        if(verv_word in rule.tsuuchi_dic):
            ret = ret + '<告知>,'
        if(verv_word in rule.tetsuzuki_dic):
            ret = ret + '<手続き>,'
        if(verv_word in rule.sonota_dic):
            ret = ret + '<その他>,'
        if(verv_word in s_v_dic.sub_verb_dic and obj_tart):
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



