from chunker import ChunkExtractor

class VerbSpliter:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        chunker = ChunkExtractor()
        self.num_chunk = chunker.num_chunk
        self.head_connect_check = chunker.head_connect_check
        self.connect_word = chunker.connect_word


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
        for i in reversed(range(start, end)):
            if doc[i].norm_ in self.sub_verb_dic:
                return self.compaound(start, i - 1, *doc), self.compaound(i, end, *doc)
        return self.compaound(start, end, *doc), ''
