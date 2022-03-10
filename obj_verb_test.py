from object_verb_structureing import VerbExtractor

model = VerbExtractor() # KeywordExtractorのクラスのインスタンス化
text = 'ストックマーク株式会社は自然言語処理を活用した情報収集サービス「Anews」の運営をして利益を得ている。国の民主化を行う。サービスを運営すると発表した。サービスの発表をした。' # キーワード抽出を行うテキスト
text = '会社の内部の調査をする。社内調査委員会が調査をしていた。従来は新型コロナウイルス禍からの回復で20年比7%近くの伸びを見込んでいたが、半導体不足で下方修正を余儀なくされた。月額制サービスで導入後の管理も請け負うことで、導入にかかる負担を少なくした。'
text ='大田勝幸社長に、業態をどう変えていくべきなのか聞いた。'
text ='監査法人から指摘を受けて、社内調査委員会が調査をしていた。'
text = '再建案を承認した。'
text = '新風を起こそうとしている。'
text = '海外の情勢を調査しながら発表する。海外の情勢の精査をしながら報告する。海外の情勢を勉強しながら発信をする。'
text = '導入にかかる負担を少なくした。平面盤と大小2つの立体盤をセットにした。'
text = '完全子会社化を目指し、1日から1株2200円でTOBをしている。'
text = '実家の母や兄と食事をしながら「新しい会社の名前をどうしようか。マルチメディアのようなかっこつけたものでなく、直球がいいのだけど」と問うと、兄の元道が「スマイル」を口にしたのです。'
text = 'スウェーデンの高級車大手ボルボ・カーは今後発売するすべての新型電気自動車の内外装を、動物の皮革を使わない「レザーフリー」にする。'
text = 'パナソニックは30日、2022年1月に米ラスベガスで開催する技術見本市「CES2022」で予定していた記者会見を、オンラインのみでの実施に切り替えると明らかにした。'
text = '「スマイルとか?」。三菱商事の"社内ベンチャーゼロ号"としてスープストックトーキョーの運営会社設立が決まったとき。実家の母や兄と食事をしながら「新しい会社の名前をどうしようか。マルチメディアのようなかっこつけたものでなく、直球がいいのだけど」と問うと、兄の元道が「スマイル」を口にしたのです。'
text = '数週間以内に写真に写っている人を自動で認識してタグ付けを提案するといった機能を使えなくする。使いやすくする。'
text = '最高裁第3小法廷は18日、発動差し止めの仮処分を求めた投資会社のアジア開発キャピタルの訴えを退ける決定をした。'
text = '重症化リスクの高い大人を対象にした緊急使用を承認をした。'
text = '緊急使用を承認をした。'
text = 'データの言語処理をする。データの緊急使用をする。'
text = '番組を主要コンテンツの一つにする。'
text = '自動車の輸出などをスムーズにする。'
text = '脱炭素を掲げる都市が増えるなか、目標達成への道筋を「見える化」する。'
#text = 'マレーシアの工場の稼働を一時停止したと明らかにした。マレーシアの工場の稼働を調査したと明らかにした。'
#text = 'マレーシアの工場の稼働を一時停止したと明らかにした。マレーシアの工場の稼働を一時停止したことを明らかにした。マレーシアの工場の稼働を一時停止すると明らかにした。'
##text = 'マレーシアの工場の稼働を一時停止したと明らかにした。'
text = '各自治体の圃場でドローンを用いて農薬散布などをする。'
text = '現地での工夫には何があり、アイリスグループとしての一体感を保つため何をしているのか。'
text = '不正を自ら申し出た社員は懲戒処分の対象にしないことを明らかにした。'
text = '2回接種からどの程度経過した人を研究対象としたのかや、2回接種からどの程度経過した人を研究対象とした。'
keyword_list = model.verb_get(text) # キーワードの候補の抽出
keyword_list = model.v_o_get(text) # キーワードの候補の抽出
print(keyword_list)