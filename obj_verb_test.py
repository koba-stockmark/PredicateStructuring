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
text = '重症化リスクの高い大人を対象にした緊急使用を承認をした。'
text = '緊急使用を承認をした。'
text = 'データの言語処理をする。データの緊急使用をする。'
text = '番組を主要コンテンツの一つにする。'
text = '自動車の輸出などをスムーズにする。'
text = '脱炭素を掲げる都市が増えるなか、目標達成への道筋を「見える化」する。'
text = 'マレーシアの工場の稼働を一時停止したと明らかにした。マレーシアの工場の稼働を調査したと明らかにした。'
text = 'マレーシアの工場の稼働を一時停止したと明らかにした。マレーシアの工場の稼働を一時停止したことを明らかにした。マレーシアの工場の稼働を一時停止すると明らかにした。'
text = 'マレーシアの工場の稼働を一時停止したと明らかにした。'
text = '各自治体の圃場でドローンを用いて農薬散布などをする。'
text = '現地での工夫には何があり、アイリスグループとしての一体感を保つため何をしているのか。'
text = '不正を自ら申し出た社員は懲戒処分の対象にしないことを明らかにした。'
text = '国の脱炭素のあり方をどうするのか。'
text = 'コロナ収束後は世界で観光客誘致が激しくなるとみて、今のうちに九州の知名度を高める「種まき」をする。'
text = '併せて29駅を無人駅とする。'
text = 'ソニーグループはテレビ事業の主力拠点のマレーシアで工場を大幅に自動化する。'
text = '機体重量を軽くし、短距離でも発着できるようにする。機体重量を軽くする。'
text = '亜鉛の国内相対取引の目安となる建値を3万円引き上げ、1トン47万8千円とした。'
text = '諸般の事情を総合的に勘案した結果、和解することを決定した」としている。'
text = '最高裁第3小法廷は18日、発動差し止めの仮処分を求めた投資会社のアジア開発キャピタルの訴えを退ける決定をした。'
text = '米国上場を検討していると明らかにしていた。'
text = 'ルネサスが同日開催した経営説明会で、23年までの能力見通しを明らかにした。'
text = 'おむつ交換の人手や費用を減らし施設運営を効率化する。'
text = '商品化に至るまでの技術供与をビジネスとしている。当面は12月末までの予約を対象にする。'
text = '発動差し止めの仮処分を求めた投資会社のアジア開発キャピタルの訴えを退ける決定をした。'
text = '予定していた記者会見を、オンラインのみでの実施に切り替えると明らかにした。予定していた記者会見を、オンラインのみでの実施に切り替えると発表した。予定していた記者会見を、オンラインのみでの実施に切り替えると発表をしていた。'
text = 'パナソニックは30日、2022年1月に米ラスベガスで開催する技術見本市「CES2022」で予定していた記者会見を、オンラインのみでの実施に切り替えると明らかにした。'
text = '2回接種からどの程度経過した人を研究対象としたのかや、2回接種からどの程度経過した人を研究対象とした。'
text = 'AIが手書きの文字を読み取るソフトウエアを主力としてきたが、法人向けのAI開発サービスやコア技術の提供を通じて企業のAI活用の黒子になろうとしている。'
text = 'コア技術の提供を通じて企業のAI活用の黒子になろうとしている。'
text = 'パフェには川根茶の中でも希少な品種「山のいぶき」を使用し、上品な味わいにした。'
text = '米食品医薬品局は23日、米製薬大手メルクなどが開発した新型コロナウイルスの飲み薬「モルヌピラビル」について、重症化リスクの高い大人を対象にした緊急使用を承認をした。'
text = 'この素粒子を調べることで、宇宙がどのようにして生まれ、なぜ物質しか存在しないのかを解き明かそうとしている。'
text = '情報処理の外部資格であるITパスポートの取得者を「DXサポーター」、提案実績を積んだ人材を「DXアドバイザー」、実践型研修の修了者らを「DXシニアアドバイザー」とする。'
text = '大型船を受け入れられるよう岸壁を整備し、自動車の輸出などをスムーズにする。'
text = 'ワインの試飲や販売、商談を建物内でしていたが、新たに屋外に面したショップと、感染対策を施した屋内のテイスティング・商談室に分離した。'
text = '個人データを提供するか否かを消費者が事前に選べるようにした。'
text = '必要な場合は出社しての勤務を可とする。友達との友情を大事にする'
text = 'マレーシアの工場の稼働を一時停止したと明らかにした。マレーシアの工場の稼働を一時停止したことを明らかにした。マレーシアの工場の稼働を一時停止すると明らかにした。'
text = '新型コロナウイルス禍などいくつものハードルを乗り越え'

text = '開発陣は経営危機、新型コロナウイルス禍などいくつものハードルを乗り越え、ついに旗艦車が日の目を見ようとしている。'

text = 'この指定は開発から審査までの迅速化を目的としており、FDAとの協議を持つ機会が増える。'
text = '吉利はウェイモとの連携をテコに米国の自動運転分野の先進技術を吸収するとともに、米国事業の拡大をめざす。'
text = '効果を少なくする。アジア太平洋地域で最大級の独立系再生可能エネルギー発電事業者であるヴィーナ・エナジーは、鳥取県西部エリア4町において、自分たちの暮らしている地域をもっと元気に、より良くしたいなどの熱い思いで"地域共創"を目指す事業者や個人を応援するファンディング・プロジェクト「地域の元気、応援プロジェクト、Powered by、日本風力エネルギー」を開始します。'
text = '自宅で簡単に運動不足の解消とリフレッシュができるB5サイズの2Wayバランスボードを新発売'
text = 'これによりアイティーエムは、オープンソースや内部ホストの脆弱性管理サービスの提供範囲を拡大し、セキュリティ運用をアウトソースする企業もyamoryを利用可能になります。'
text = 'Coinbase国内におけるカスタマーサポート強化に向け、電話サポートサービスを開始:時事ドットコム。'
text = 'YKK APでは、こうした課題を解決する工法や商品開発、人材育成に取り組んでおり、その一つとして、省施工や工期短縮に貢献するパネル住宅の普及促進に向けて、パネルに最適な窓の研究・開発を進めてまいりました。'
text = 'KDDIは、SNSなどウェブを中心に活躍する関西在住の19人のアーティストとコラボした「#大阪環状線をアートでつなぐ」企画を開始した。'
text = '松下電器産業株式会社、パナソニック オートモーティブシステムズ社は、2007年2月13日にETC車載器の生産累計500万台を達成しました。'
text = '詳しくはこちらカメラを使って戸建ての工事現場を遠隔管理できる大和ハウス工業は17日、戸建て住宅のすべての工事現場にウェブカメラの設置を始めたと発表した。'
text = '株式会社エネルギア・コミュニケーションズは、広島県三次市様の新型コロナワクチン接種記録確認業務へ、AI-OCRサービス「Seisho」とRPAサービス「EneRobo」を導入し、紙帳票の読取り・データ突合等の自動化を行い、想定される作業時間を約8割削減しました。'
text = '新潟市は、自動車道の一部を歩行空間にしてテーブルやベンチを置きにぎわい空間を創出する社会実験を今秋に行う。'
text = 'これまで気候資金の用途は、温暖化ガス削減の取り組みである「緩和策」と、気候変動の影響を軽減・回避するための「適応策」とされてきた。影響を食べるための「適応策」とされてきた。'
text = '電気事業連合会の池辺和弘会長は17日、2021年~22年冬にかけての電力需給対策について、「燃料の確保や火力発電所の保安を徹底し、電力の安定供給に支障をきたさないようにする」と話した。'
text = 'イマジニアは,氷上で行うウィンタースポーツ「カーリング」を手軽に楽しめるNintendo Switch向けソフト「みんなのカーリング」を,本日発売した。'
text = 'ロジテックINAソリューションズが、スティック型ポータブルSSD「LMD-SPBU3」シリーズを発売しました。'
text = '創業初期から、NIMASOは、スマートフォンに関連するアクセサリーの開発販売に力を入れ、ブラントを発展させました。'
text = '春の訪れを告げるイチゴを使ったテイクアウトスイーツ「イチゴとルバーブのベイクドケーキ」を販売します。'
text = '名古屋エアゾール株式会社のPR・販売会社である株式会社メイゾルは、"爪まで丁寧に育む"をコンセプトとした、ハンド&ネイルケアシリーズ「寧寧」のシリーズ第二弾として、爪やその周辺の特に、"荒れや乾燥"、が気になる部分を集中ケアするネイル用保湿パック「、寧寧、ネイルケアパック、」を、2022年3月1日より自社販売サイトにて販売開始いたします。'
text = 'ミニストップは、人気の「やみつキッチン」シリーズから登場する菓子パンの新商品「やみつきになる!、チョコクリームパン」を、2022年1月11日より国内のミニストップ店舗にて発売します。'
text = 'プラント大手の日揮や全日空、日本航空、日清食品など16社は温室効果ガスの排出量が少ない次世代航空燃料=SAFを商用化する。'
text = '金沢大発ベンチャー「Kanazawa Diamond」が、独自技術で人工的に製造した黒いダイヤモンドの販売を2022年秋ごろに始める計画だ。'
text = 'パナソニック株式会社は、20,000時間の長寿命と、白と黒のコントラスト感をアップし、文字をくっきり読みやすくした「文字くっきり光」を搭載した丸形蛍光灯「パルック、20000」を2015年6月1日より発売します。'
text = '東京・大阪・京都ほか全17施設の三井ガーデンホテルにて、ワクチン接種予約をされた接種者ご本人およびその付き添いの方にご利用いただける。内部調査をする。'
text = 'アジア太平洋地域で最大級の独立系再生可能エネルギー発電事業者であるヴィーナ・エナジーは、鳥取県西部エリア4町において、自分たちの暮らしている地域をもっと元気に、より良くしたいなどの熱い思いで"地域共創"を目指す事業者や個人を応援するファンディング・プロジェクト「地域の元気、応援プロジェクト、Powered by、日本風力エネルギー」を開始します。'
text = 'FRONTIERブランドでPC等を販売するインバースネットは1月19日、Alder Lakeこと第12世代Intel Coreプロセッサを搭載するコンパクトなデスクトップPCを、「GKシリーズ」「GXシリーズ」からあわせて6機種発売した。'
text = 'エンジンの開発を東京でする'
text = 'ネッツトヨタ岩手は、子どもたちに車への興味・関心と楽しめる空間を提どもするため、本社中央店にトミカとコラボした「トミカコーナー」を開設した=写真。'
text = '現在、和歌山県は防災情報システムの更改を行っています。'
text = '「森の箱」」を開発、受注販売を始めた。「森の箱」」を開発、学校は楽しい。'
text = '3社は新会社を設立、金融デジタルプラットフォームの提供を加速する。'
text = 'コンパクトサイズを2014年1月6日より順次発売、合計98品番に品種拡充していきます。'
text = 'パナソニック補聴器株式会社は、"聞きたい音をよりくっきり、よりはっきり"と題し、入力音を128バンドの周波数帯域に分割し独立して処理することのできる。'
text = '「繭の小道」を発表、展示いたします。'
text = '?、ハーバード大学などがAIを開発、株式会社PR TIMES'
text = '森永乳業では、ヘルスケア事業として、「全世代の健康で幸せな毎日の実現へ」をテーマに、2021、年、1、月より健康セミナー事業「健幸サポート栄養士」を本格的に開始、健康経営を推進される企業や自治体に向けて健康セミナーを開催しています。'
text = '新型コロナウイルスの影響で鉄道の利用が落ち込み、同社ではコロナ前の需要に戻らないとみており、運行体制をスリム化して動力や保守コストを削減する。'
text = 'バイデン米政権が監視技術の輸出を管理する多国間の枠組みについて表明したことを受け、協議に入る。'
text = '関西スーパーマーケットの経営権を巡る争奪戦の行方は法廷闘争となり、地裁と高裁が正反対の判断を示したことで最高裁までもつれ込んだ。'
text = '世界大学ランキングのトップ100位に日本からは2校のみ、最近では中国をはじめアジアの大学が躍進しており、日本が相対的にさらに見劣りしてきました。'
text = 'マスク氏はインサイダー取引を回避するためのルールに沿ったテスラ株の取引計画を9月に策定。'
text = '詳しくはこちら発表日:2022年02月07日テックウインド、抗菌・抗ウイルスの効果がある法人様向けガラスコーティング剤の画面塗布サービス開始のお知らせ~画面の強度を上げ破損を防止、防汚効果・割れ耐性向上効果もあり~*参考画像は添付の関連資料を参照テックウインド株式会社は法人様を対象に、抗菌・抗ウイルスの効果があるガラスコーティング剤「Dr.HardoLass」の画面塗布サービスを2022年2月7日から開始します。'
text = 'ステランティスのブランド、独オペルは2022年2月2日、Cセグメントツーリングワゴン「アストラ スポーツツアラー」を発表、そのデザインを初公開しました。'
text = '東京都をガイド、案内などする。東京都内&周辺の"端っこ"をめぐる散歩エッセイ&ガイド、「東京休日端っこ散歩」を2022年2月17日に刊行しました。'
text = '株式会社、学研ホールディングスのグループ会社、小中学生向け学習参考書の出版社である株式会社、文理は、2022年3月より、「毎日ちょっと、365日ドリル、英語」を発売します。'
text = '西日本電信電話と京都大学は2月17日、京都大学プラットフォーム学卓越大学院プログラムにおいて連携し、社会に存在するさまざまなデータを活用して連携する次世代のプラットフォームに関する実証実験を行うための検証環境「Platform Initiative Lab」を共同で整備することを発表した。'
text = '株式会社、マリークヮント コスメチックスは、2022年2月4日より、簡単に眉メイクの完成度を上げながら眉毛ケアも叶う眉マスカラ「ブロウ フィニッシュ<眉墨>」の販売を開始いたします。'
text = '株式会社Mirrorlaが「スキンケア・ヘアケアを通して、自分自身と向き合う習慣を一緒につくる」コンセプトのもと、肌と髪のオールインワン・ケアを叶える基礎化粧品「Collajenne」のサブスクリプションプランを開始しました。'
text = '「ペヤングソースやきそば」を製造する「まるか食品」が、宮城県南三陸町の県立志津川高校の生徒と協力して、ペヤングソースやきそばの新バージョン「たこめし風」と「わさび?油味」を開発した。'

# 解析誤り
text = 'ホンダは二足歩行の人型ロボット「ASIMO」に代表されるロボティクス技術の開発を長年行ってきた。'

#################


text = '日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'

text = 'テックウインドは、PGAのトッププロもパター練習ツールとして採用しているパタートレーニングツールブランド「Wellputt」から世界最古のオープンゴルフ競技である「全英オープン」とコラボレーションしたスペシャルエディション「Wellputtマット4m、全英オープンモデル」とパターストロークの軌道を矯正するストロークテンプレート「Wellstroke」の2製品を発売した。'

text = 'プラント大手の日揮や全日空、日本航空、日清食品など16社は温室効果ガスの排出量が少ない次世代航空燃料=SAFの国内での商用化と普及を目指す団体を立ち上げました。'

text = '伊藤忠商事グループの株式会社Belongは、同社が提供する法人向け中古端末のレンタル・販売サービス「Belong One」にて、「Android Enterprise Device Reseller、認定取得」及び「Android Enterprise Essentials」の提供を記念し、法人のお客様により手軽かつセキュアな状態で、Android、端末をご導入頂けるよう、キャンペーンを開始いたします。'
text = '"日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'

text = '4大共通ポイントの事業者が運営するシステムと1つのゲートウェイで接続できるクラウドサービス「PointInfinity、マルチポイントゲートウェイ」を1月26日から提供開始します。'

text = 'グローバル刃物メーカーの貝印株式会社は、「ねこ」をテーマとしたビューティーツールシリーズ「Nyarming」の新商品「ねこのシャンプーグローブ」「ねこの洗顔ブラシ」を、2022年3月8日より、貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売いたします。'

text = 'Y&Y STOREは、本日2022年2月24日よりコスパ抜群のレーザー彫刻機「Runmecy D4」を、GREEN FUNDINGにて販売を開始しました。'

text = '調査を開始した。調査を開始している。調査を開始する。調査を開始したい。調査を開始したくない。調査を開始してこなかった。'

text = '"日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'

text = '1933年の創業以来、フェルト帽や天然草を加工する型物を中心に帽子づくりをおこなってきた東ハットは、思い出の通園・通学帽を小さくリメイクするサービス「思い出ハットプロジェクト」を始動。'

text = 'グローバル刃物メーカーの貝印は、デリケートゾーンの毛量を適度に調整できる「FEMINICARE、すきカミソリ、2本入」を、2022年3月8日より貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売しました。'

text = 'オーダーメイド枕の店まくらぼは、2017年から横浜F・マリノスを睡眠の観点からサポートし、オーダーメイド枕などの寝具の提供や、アスリートがパフォーマンスを発揮するための睡眠学セミナーなどを行っています。'

#text = 'ホンダアクセスは、ホンダが展開するカーシェアサービス「EveryGo」の一部車両に、運転支援や車内の快適性を高めるための純正アクセサリーを装着し、EveryGoでの安心・快適なドライブをサポートする。'

text = 'コロナ禍で住まいの環境をよくするため家具への関心が高まり、需要が見込めると判断した。'

text = '湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'
text = '株式会社ワンインチはカンナビジオールを含む機能性食品素材を健常志願者が摂取した時の安全性確認オープンラベル試験をアポプラスステーション株式会社に委託し実施した。'

text = 'ボックス型ブース「隠れ家ワークスペース「森の箱」」を開発、受注販売を始めた。'


text = 'スプリングバレーブルワリーは1月28日、日本産ホップのおいしさを楽しめる限定ビール「JAPAN HOP~ペールエールタイプ~」をスプリングバレーブルワリー京都で数量限定で提供を開始する。'

text = '株式会社マネーフォワードは、2022年の確定申告シーズン到来に先立ち、個人事業主の開業支援サービス「マネーフォワード クラウド開業届」導入促進のための特設ページ「好きを仕事にする、ということ」を開設した。'
text = 'ロジテックINAソリューションズが、スティック型ポータブルSSD「LMD-SPBU3」シリーズを発売しました。'


# subject のとり方　アイリスオーヤマと、ソフトバンクグループの子会社　が取りたい
text = '生活用品メーカー大手のアイリスオーヤマと、ロボット開発を手がけるソフトバンクグループの子会社が資本業務提携し、飲食店やホテル向けに配膳ロボットの開発・販売を強化することになりました。'

text = '株式会社Nabocul Cosmeticsは、2022年1月12日から14日まで東京ビッグサイトで開催された「2022年東京化粧品展覧会COSME TOKYO」に初出展し、新しいエイジングケア分野の最新テクノロジー化合物「OLANDU」を発表しました。'

text = 'ミニストップは、人気の「やみつキッチン」シリーズから登場する菓子パンの新商品「やみつきになる!、チョコクリームパン」を、2022年1月11日より国内のミニストップ店舗にて発売します。'
keyword_list = model.verb_get(text) # キーワードの候補の抽出
keyword_list = model.v_o_get(text) # キーワードの候補の抽出
