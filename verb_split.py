from chunker import ChunkExtractor

class VerbSpliter:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word



    """
    補助用言のチェック
    """

    # NG '発表', '実現', '拡大', '追加'
    sub_verb_dic = ['開始', 'スタート', '始める', '始まる', '始動', '本格始動', '続ける', '終わる', '終る',
                    '掲げる', '目指す', '達成', '予定', '計画', '実施', '行なう', '行う', '進める', '推進', '加速',
                    '強化', '拡充', '活用', 'お知らせ', '決定',
                    '発表', '報ずる', '検討', '公開', '図る', 'いたす', 'いただく']

    """
    補助動詞かどうかの判別
    """
    def sub_verb_chek(self, check_w):
        for sub_verb_w in self.sub_verb_dic:
            if check_w.startswith(sub_verb_w):
                return True
        return False


    """
    始点から終点までの単語の結合
    """
    def compaound(self, start, end, *doc):
        ret = ''
        for i in range(start, end ):
            ret = ret + doc[i].orth_
        ret = ret + doc[end].lemma_
        return ret


    def objec_devide(self, start, end, *doc):
        return


    def verb_devide(self, start, end, *doc):
        if start == end:
            return self.compaound(start, end, *doc), ''
        for i in reversed(range(start, end + 1)):
            if doc[i].norm_ in self.sub_verb_dic:
                if doc[i - 1].tag_ != '名詞-普通名詞-サ変可能':  # 本格始動　など普通名詞との合成
                    if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                        return '', self.compaound(i, end, *doc) + 'する'
                    else:
                        return '', self.compaound(i, end, *doc)
                if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                    return self.compaound(start, i - 1, *doc) + 'する', self.compaound(i, end, *doc) + 'する'
                else:
                    return self.compaound(start, i - 1, *doc) + 'する', self.compaound(i, end, *doc)
        return self.compaound(start, end, *doc), ''
