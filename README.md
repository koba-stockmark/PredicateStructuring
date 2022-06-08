# 述部を書用いた企業活動のフェイズチェックプログラム

## 必要ライブラ
SpaCy
からダウンロード

## 入出力

### 入力
+ テキスト

### 出力：フェイズ情報
1. 研究・開発　　　　：　研究開発段階
2. 商用化・サービス化：　商用化段階
3. その他　　　　　　：　展示や協業、参画などその他の企業活動
4. 空白　　　　　　　：　企業活動以外             　

## 出力サンプル

## ルール・辞書
+ phase_rule_dic.py
:フェーズの判別辞書
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

### ライブラリ
+ phase_chek.py (述語項構造からフェーズの獲得)
+ main_verb_chek.py (主述部か補助述部かの判断)
+ pas_analysis.py (述語項構造の作成)
+ predicate_get.py (基本術部から主述部と補助述部に別れた述部の獲得)
+ predicate_phrase_analysis.py　（基本述部の解析。結合するとルールIDも返る）
+ predicate_split.py　（主述部と補助述部の分離処理）
+ case_information_get.py　（格情報の獲得）
+ subject_get.py (主語の獲得)
+ parallel_get.py (並列項の獲得)
+ kanyouku_check.py (慣用句処理)
+ modality_get.py   (モダリティ処理、TBD　現在はテストプログラムのみ)
+ chunker.py (名詞と動詞のチャンキングと格情報の獲得、各項の生成はここで行う)
+ data_dump.py (デバッグ用のデータダンプ)

