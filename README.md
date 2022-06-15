# 述部を書用いた企業活動のフェイズチェックプログラム

## 必要ライブラ
SpaCy
+ SpaCyからダウンロード

## 入出力

### 入力
+ テキスト（文字列）
  + （文末に句読点やカッコがない場合は、文末に「。」を付与するとSpaCyの解析エラーを回避できる）

### 出力
+ フェイズ情報(文字列)

1. 研究・開発　　　　：　研究開発段階
2. 商用化・サービス化：　商用化段階
3. その他　　　　　　：　展示や協業、参画などその他の企業活動、及び企業活動以外

### フェイズの判定基準（優先順位）
1. 主述部に企業活動キーワードがある
2. 限定された格（phase_analyze_case[]）で補助用言（sub_verb_dic）につながる項で企業活動キーワードがある
3. 補助用言の中で企業活動キーワードに属するもの

## 評価データ
+ solution_sentnece.txt (5000文)

## ルール・辞書
+ phase_rule_dic.py
:フェーズの判別関係の辞書
  + フェーズルール (kousou_dic, kenkyuu_dic, kaihatsu_dic, jikken_dic, seihin_dic, koushin_dic, tyuushi_dic, sankaku_dic, riyou_dic, soshiki_dic, renkei_dic, tsuuchi_dic, tetsuzuki_dic, sonota_dic)
  + フェーズ処理の対象になる格の定義 (phase_analyze_case)
  + 時制に関する補助用言 (kako, genzai, mirai)
  + マルチラベルをシングルラベルに変換するルール (single_rule)
+ sub_verb_dic.py
:補助用言辞書
+ special_verb_dic.py
:企業活動動詞辞書
+ kanyouku_dic.py
:慣用句辞書
## プログラムリスト
### サンプルプログラム
+ phase_extractor_sample.py

### メインプログラム
+ phase_extractor.py
  + 関数

  class PhaseExtractor:
                   
  def single_phase_extract(self, text):


テキスト入力に対してフェーズ情報を返す。
"debug"フラグによりdebugモードにすると解析結果をダンプできる。
debugモードのときは解析結果のログ(tsv)が出力となる。


### ライブラリ
+ phase_check.py (述語項構造からフェーズの獲得)
+ main_verb_check.py (主述部か補助述部かの判断)
+ pas_analysis.py (述語項構造の作成)
+ predicate_get.py (述部の判断と基本術部の獲得)
+ predicate_phrase_analysis.py　（基本述部の解析。結合するとルールIDも返る）
+ predicate_split.py　（主述部と補助述部の分離処理）
+ case_information_get.py　（格情報の獲得）
+ subject_get.py (主語の獲得)
+ parallel_get.py (並列項の獲得)
+ kanyouku_check.py (慣用句処理)
+ modality_get.py   (モダリティ処理、TBD　現在はテストプログラムのみ)
+ chunker.py (名詞と動詞のチャンキングと格情報の獲得、各項の生成はここで行う)
+ data_dump.py (デバッグ用のデータダンプ)

