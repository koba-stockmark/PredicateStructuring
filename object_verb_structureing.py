import spacy
from spacy.symbols import obj


class VerbExtractor:

    def __init__(self):
        """
        関数`__init__`はクラスをインスタンス化した時に実行されます。
        """
        # self.nlp = spacy.load('ja_ginza') # Ginzaのロード
        self.nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル

    def obj_get(self, text):
        """
          目的語の取得
        """
        doc = self.nlp(text)  # 文章を解析

        for tok in doc:
            if tok.dep == obj:  # トークンが目的語なら
                print(tok.text)  # テキストを表示
        return

        """
        名詞のチャンキング
        """

    def num_chunk(self, pt, *doc):
        ret = doc[pt].orth_
        for i in reversed(range(1, pt)):
            if (pt == doc[i].head.i):
                ret = doc[i].orth_ + ret
            else:
                for token in doc[pt:]:
                    if (pt == token.head.i):
                        if (token.orth_ == 'を'):
                            break
                        ret = ret + token.orth_
                break
        #      print(doc[pt].orth_)
        #      return doc[pt].orth_
        return ret

        """
        O-Vの取得
        """

    def v_o_get(self, text):

        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析

        for token in doc:
            obj_w = ''
            rule_id = 0
            if token.dep == obj:  # トークンが目的語なら
                if (token.head.i == token.head.head.i and token.head.pos_ == "VERB"):  # 最後の動詞？
                    obj_w = self.num_chunk(token.i, *doc)
                    if (token.head.lemma_ == "する"):
                        #
                        #             述部が  名詞＋（と、に）する（目標とする　など）
                        #
                        if (doc[token.head.i - 1].orth_ == 'に' or doc[token.head.i - 1].orth_ == 'と'):  # 【名詞】に(と)する
                            verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + token.head.lemma_
                            obj_w = self.num_chunk(token.i, *doc)
                            if (doc[token.head.i - 2].tag_ == '補助記号-括弧閉'):
                                verb_w = self.num_chunk(token.head.i - 3, *doc) + token.head.lemma_
                            rule_id = 1
                        #
                        #             述部が  ○○の＋名詞＋を＋する（調査をする　など）、　名詞＋サ変名詞＋する（内部調査をする　など）
                        #
                        elif (doc[token.head.i - 1].orth_ == 'を' and doc[token.head.i - 2].pos_ == 'NOUN'):
                            if (doc[token.head.i - 3].orth_ == 'の'):
                                obj_w = self.num_chunk(token.head.i - 4, *doc)  # 内部の調査をする -> 内部を　調査する
                                verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + token.head.lemma_
                                rule_id = 2
                            elif (doc[token.head.i - 3].pos_ == 'NOUN' and doc[token.head.i - 2].tag_ == '名詞-普通名詞-サ変可能'):
                                obj_w = self.num_chunk(token.head.i - 3, *doc)  # 内部調査をする -> 内部を　調査する
                                verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + token.head.lemma_
                                #                verb_w = doc[token.head.i - 2].orth_  + token.head.lemma_
                                rule_id = 3
                            elif (doc[token.head.i - 3].pos_ == 'VERB' and doc[token.head.i - 3].head.i == doc[token.head.i - 3].i):
                                obj_w = self.num_chunk(token.head.i - 3, *doc)  # 内部調査をする -> 内部を　調査する
                                verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + token.head.lemma_
                                #                verb_w = doc[token.head.i - 2].orth_  + token.head.lemma_
                                rule_id = 30
                            #
                            #             述部が  名詞＋を＋する（調査をする　など）
                            #
                            else:
                                obj_w = self.num_chunk(token.i, *doc)
                                #                  verb_w = doc[token.head.i - 2].orth_ + doc[token.head.i - 1].orth_ + token.head.lemma_
                                verb_w = token.head.lemma_
                                rule_id = 4
                        #
                        #             述部が  形容詞＋する（少なくする　など）
                        #
                        elif (doc[token.head.i - 1].pos_ == 'AUX'):
                            if (token.head.i - 4 >= 4 and (doc[token.head.i - 1].tag_ == '接尾辞-形容詞的'  or doc[token.head.i - 1].tag_ == '助動詞' )and doc[token.head.i - 2].pos_ == 'VERB'):
                                obj_w = self.num_chunk(token.i, *doc)
                                verb_w = doc[token.head.i - 2].orth_ + doc[
                                    token.head.i - 1].orth_ + token.head.lemma_  # ○○を使いやすくする -> 使いやすくする
                                rule_id = 5
                            else:
                                obj_w = ''
                        elif (doc[token.head.i - 1].pos_ == 'ADJ'):
                            if (token.head.i - 4 >= 4 and doc[token.head.i - 1].tag_ == '形容詞-非自立可能' and doc[token.head.i - 2].pos_ == 'NOUN'):
                                obj_w = self.num_chunk(token.head.i - 4, *doc)
                                verb_w = doc[token.head.i - 2].orth_ + doc[
                                    token.head.i - 1].orth_ + token.head.lemma_  # ○○を余儀なくする -> 余儀なくする
                                rule_id = 6
                            elif (doc[token.head.i - 1].tag_ == '形容詞-一般'):
                                obj_w = self.num_chunk(token.i, *doc)
                                verb_w = doc[token.head.i - 1].orth_ + token.head.lemma_  # ○○を少なくるする -> 少なくする
                                rule_id = 7
                            obj_w = ''
                    #
                    #           ○○する　以外の動詞
                    #
                    else:
                        if (doc[token.head.i + 1].tag_ == '動詞-非自立可能'):          # 動詞　＋　補助動詞
                            verb_w = token.head.lemma_ + doc[token.head.i + 1].lemma_
                            rule_id = 8
                        else:
                            verb_w = token.head.lemma_
                            rule_id = 9
                        obj_w = self.num_chunk(token.i, *doc)
                        obj_w = ''  # デバッグ用

                #            if(token.head.pos_ == "ADJ" and token.head.head.i == token.head.head.head.i and token.head.head.pos_ == "VERB"):
                #              obj_w = doc[token.head.i - 3].orth_
                #              verb_w = doc[token.head.i - 1].orth_ + token.head.lemma_    # ○○を美しくする -> 美しくする
                #              rule_id = 10

                #
                # 最終述部でない場合
                #
                elif (doc[token.head.i].pos_ == "VERB" and doc[token.head.i].head.i == doc[token.head.i].head.head.i and doc[token.head.i].head.pos_ == "VERB"):  # 最後の動詞を修飾する動詞？
                    #            print(doc[token.head.i].head.lemma_ , doc[doc[token.head.i].head.i - 1].lemma_)
                    if (doc[token.head.i].head.lemma_ == 'する' and doc[doc[token.head.i].head.i - 1].lemma_ != 'を'):  # かかり先の動詞が　○○をする　ではなく　○○する
                        obj_w = self.num_chunk(token.i, *doc)
                        verb_w = token.head.lemma_
                        rule_id = 11
                elif (token.head.head.head.lemma_ == "する" and doc[token.head.i + 1].lemma_ == '決定'):
                    verb_w = token.head.lemma_
                    obj_w = self.num_chunk(token.i, *doc)
                    rule_id = 12
                if (obj_w):
                    print(text)
                    print('【', obj_w, verb_w, '】 rule_id =', rule_id)
        #              print('【', token.lemma_, token.head.lemma_, '】')
        return

    def verb_get(self, text):
        """
         動詞の塊を抽出する
        """

        # 形態素解析を行い、各形態素に対して処理を行う。
        doc = self.nlp(text)  # 文章を解析

        """
        デバッグ用に結果を表示
        """
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

        """
        形態素をチェック
        """
        for token in doc:
            if token.dep == obj:
                """
                 かかり先による例外処理
                """
                if token.head.orth_ == "行う":
                    print(token.head.i, token.head.orth_, token.head.head.orth_)
                """
                一般処理
                """
                print(token.i, token.orth_, token.head.orth_)
        return
