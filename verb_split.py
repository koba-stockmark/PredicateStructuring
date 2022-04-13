from chunker import ChunkExtractor

class VerbSpliter:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.connect_word = chunker.connect_word
        self.num_chunk = chunker.num_chunk
        self.compaound = chunker.compaound




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
            if sub_verb_w in check_w:
#            if check_w.startswith(sub_verb_w):
                return True
        return False


    """
    述部に対するobjを探索
    """
    def object_serch(self, start, *doc):
        for token in doc:
            if token.head.i == start and token.dep_ == 'obj':
                return self.num_chunk(token.i, *doc)['lemma']
        return ''


    """
    目的語の中の述部を分割

    ret : 目的語　＋　主述部　＋　主述始点　＋　主述部終点
    """
    def object_devide(self, start, end, *doc):
        if start == end or doc[end].lemma_ == 'サービス':
            return self.compaound(start, end, *doc), '', -1, -1
        for i in reversed(range(start, end + 1)):
            if doc[i].pos_ == 'PUNCT':
                break
#            if doc[i].lemma_ == 'の' and doc[i - 1].lemma_ != 'へ' and doc[i].pos_ == 'ADP':      # の　で分割。　への　は例外
            if doc[i].lemma_ == 'の' and doc[i].pos_ == 'ADP':      # の　で分割。　への　は例外
                if doc[end].tag_ == '名詞-普通名詞-サ変可能' and i + 4 >= end:    # 述部の複合語を4語まで許す
#                if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                    return self.compaound(start, i - 1, *doc), self.compaound(i + 1, end, *doc) + 'する', i + 1, end
            elif doc[i].lemma_ == 'こと':
                if doc[i - 1].lemma_ == 'する':
                    return self.object_serch(start, * doc), self.compaound(start, i - 2, *doc) + 'する', start, i - 2, end
        return self.compaound(start, end, *doc), '', -1, -1


    """
    複合術部を主述部と補助術部に分割
    
    ret : 主述部　＋　補助術部　＋　主述始点　＋　主述部終点　＋　補助述部始点　＋　補助述部終点
    """
    def verb_devide(self, start, end, *doc):
        if start == end:
            return self.compaound(start, end, *doc), '', start, end, -1, -1
        for i in reversed(range(start, end + 1)):
            if doc[i].norm_ in self.sub_verb_dic:
                if doc[i - 1].tag_ != '名詞-普通名詞-サ変可能':  # 本格始動　など普通名詞との合成
                    if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                        return '', self.compaound(i, end, *doc) + 'する', -1, -1, i, end
                    else:
                        return '', self.compaound(i, end, *doc), -1, -1, i, end
                if doc[end].tag_ == '名詞-普通名詞-サ変可能':
                    return self.compaound(start, i - 1, *doc) + 'する', self.compaound(i, end, *doc) + 'する', start, i - 1, i, end
                else:
                    return self.compaound(start, i - 1, *doc) + 'する', self.compaound(i, end, *doc), start, i - 1, i, end
        return self.compaound(start, end, *doc), '', start, end, -1, -1
