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
text = '株式会社Nabocul Cosmeticsは、2022年1月12日から14日まで東京ビッグサイトで開催された「2022年東京化粧品展覧会COSME TOKYO」に初出展し、新しいエイジングケア分野の最新テクノロジー化合物「OLANDU」を発表しました。'
text = 'ミニストップは、人気の「やみつキッチン」シリーズから登場する菓子パンの新商品「やみつきになる!、チョコクリームパン」を、2022年1月11日より国内のミニストップ店舗にて発売します。'
text = 'ヤマハ発動機は、電動アシスト自転車の新型モデル「WABASH RT」を10日発売。'
text = '富士フイルムビジネスイノベーションは3月1日、同社のドキュメントハンドリング・ソフトウェア「DocuWorks」を基に開発した新クラウドサービス「DocuWorks Cloud」の提供を発表した。'
text = 'グローバル刃物メーカーの貝印株式会社は、「ねこ」をテーマとしたビューティーツールシリーズ「Nyarming」の新商品「ねこのシャンプーグローブ」「ねこの洗顔ブラシ」を、2022年3月8日より、貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売いたします。'
text = 'Googleがペン入力対応のタブレットの開発を水面下で進めているとの噂が、海外を中心に話題になっている。'
text = '東京ガスは2月24日、横浜市、三菱重工グループと共同で、ごみ焼却工場の排ガス中に含まれるCO2を分離・回収し、CO2を資源として利活用する技術の確立に向けた実証試験を行うと発表した。'
text = 'これによりアイティーエムは、オープンソースや内部ホストの脆弱性管理サービスの提供範囲を拡大し、セキュリティ運用をアウトソースする企業もyamoryを利用可能になります。'
text = '内田くんは「光の波紋」をテーマにプログラミングで光の色や強弱を変化させ、水の波紋が広がるような「落ち着くLED照明」を制作。'
text = '北海道を中心に宿泊運営事業などを展開するレッドホースコーポレーション株式会社は、工事事業者専用宿「ワークマンハウスニセコ」を北海道虻田郡倶知安町に2022年2月7日オープンしました。'
text = '伊藤ハムも2020年、大豆ミートを使った同社初の家庭向け代替肉商品「まるでお肉!」シリーズを発売した。'
text = '同社は千種川河口東側に広がっていた東浜塩田の伝統製法を受け継ぎ、高知県室戸沖の海洋深層水を活用する「天海」の水やにがりも販売する。'
text = '加賀市のホテルアローレは今夏をめどに、敷地内に高級志向のキャンプ「グランピング」を楽しめる施設をオープンさせる。'
text = '近鉄不動産は、玄関横に設置する宅配ボックスと防災用品収納スペースが一体となった専用ボックスを開発した。'
text = 'そんななか北欧・フィンランド発の「WOLT」は、食品小売業との提携を加速させるほか、ダークストアを活用した独自の食品配達サービスにも着手するなど、新たな動きを見せている。'
text = 'パナソニック株式会社は、モバイルの本質「軽量」「長時間」「頑丈」「高性能」を追求したモバイルノートパソコン「レッツノート」の2016年春モデルの発売を記念し、2016年1月14日から3月31日まで「新生活応援キャンペーン」を実施しています。'
text = 'IHI運搬機械は12月28日、機械式駐車装置において、省電力で、全ての電気自動車への充電を可能とする新システムを開発したと発表した。'
text = '東京大学、Human & Environment Informatics Labの研究チームは、物理的なファンによる風がないにもかかわらず、風の感覚を耳で得られるヘッドフォン型ウェアラブルデバイスを開発した。'
text = 'エステーは、この環境下での快適な生活をサポートするとともに、環境に配慮した生活ができるよう商品開発を強化。'
text = '立命館大学と、立命館アジア太平洋大学が、AIチャットボットを導入しました。'
text = '離乳食販売の、ippeは、和食だしと国産材料にこだわった「無添加離乳食」を毎日の食事から、贈答品まで幅広くお使いいただける商品として開発しました。'
text = '環境に優しい「西宮市指定ごみ袋」12種類を発売!、日本サニパック株式会社は、兵庫県西宮市で2022年4月1日より開始される「指定袋制度」に先立ち、環境に優しい素材を使用した家庭用の「もやすごみ」用と「その他プラ」用、事業系の「可燃ごみ」用のごみ袋12種類を1月24日に発売しました。'
text = 'デジタルAVCマーケティング本部は、世界最小・最軽量1でスタイリッシュなボディながら、写真もハイビジョン動画も撮影可能なレンズ交換式デジタル一眼カメラ「DMC-GF1」を9月18日より発売します。'
text = '滋賀銀行、、は18日、滋賀県内を中心にスーパーを展開する平和堂、、のスマートフォンアプリ「HOPウォレット」と、オープンAPIを活用した口座連携を19日から開始すると発表した。'
text = '甲一、以下トッパンフォームズ)とブルーイノベーション株式会社は、AGV自動巡回点検ソリューションの共同提供を開始したことをお知らせします。'
text = '間もなく中国の旧暦正月を迎えるのを機に、中国の嵩山少林寺と世界各地の少林文化センターは、国際的なカンフーコンテストである「Happy Chinese New Year: Shaolin Kung Fu Online Games」を開始した。'
text = '株式会社ゲームオン、は、超大型MMORPG「ArcheAge」において、2022年1月5日より、荷物を運ぶと"福袋"が手に入るイベント「福を呼ぶ配達」を開始いたしました。'
text = 'パナソニック株式会社は、ドローンと大型風船を融合し、スポーツやイベントなどでさまざまな演出が可能なドローンシステム"バルーンカム"の試作機を開発いたしました。'
text = 'CNNを傘下に抱えるメディア大手ワーナーメディアは同業のディスカバリーとの経営統合を進めているほか、CNNは新たなストリーミング・サービスを春に開始する計画。'
text ='ご提供〜オリックス・リニューアブルエナジー・マネジメント株式会社は、このたび、大規模太陽光発電所の運営状況を第三者の視点から評価・分析し、効果的なマネジメント方法を提案する「ターンアラウンドサポートサービス」を開始しますのでお知らせします。'
text = '「よいお茶を、いつもそばに」をコンセプトとした日本茶ブランド「CRAFT TEA」を運営する株式会社クラフト・ティーは、新商品、玄米ほうじ茶「島田やぶきた玄米ほうじ」を2022年3月7日〜3月6日の期間限定で、「CRAFT TEA、大手町」「CRAFT TEA、銀座」「CRAFT TEA、丸の内」で提供します'
text = '現地時間2月15日、ソニーは新型完全ワイヤレスイヤホン、「LinkBuds」、を発表した。'
text = '株式会社デイトナ・インターナショナルが運営するコンセプトストア「Firsthand、」、は、地球環境や人々に優しいハッピーなチョコレートを提案するプロジェクト「100% POSITIVE CHOCOLATE」イベントを2月5日~開催する。'
text = '和歌山県は、県産品・中間加工食品の事業者とバイヤーを結ぶオンライン商談システム「おいしく食べて和歌山モール-FOR BUSINESS-」=写真=の運用を1月21日、開始した。'
text = '法人会員向けに与信管理ASPクラウドサービスを提供するリスクモンスター株式会社は、2月22日より、iOSおよびAndroid向けスマートフォンアプリ「リスモンかんたんコンプラナビ」の提供を開始する。'
text = '株式会社オージャストは、展示会や見本市で製作される展示ブースを、全て使い回しができる資材で制作することで、環境に優しく、かつ費用を抑えた、「Re:ブース」を2022年03月より提供いたします。'
text = 'NTNは、逆入力遮断クラッチ「トルクダイオード」の新ラインアップとして、従来品に対して外輪外径を1/3、重量を1/14にした小型・軽量のトルクダイオード「TDL8」を開発した。'
text = '株式会社WIPは、CBDを配合したフレグランスやオーガニックオイルなどライフスタイルに特化した日本発のウェルネスCBDブランド「METASU|ミタス」にて、CBD配合の発砲タブレットタイプの入浴剤「CBD BATH TABLET」の販売を公式オンラインショップにて開始。text = '
text = '大創産業は、「メルペイ」「au PAY」を2022年2月1日から、「楽天ペイ」を3月1日から100円ショップのDAISO、新業態のStandard Products by DAISO、THREEPPY、CouCou、Plus Heart2730店で導入する。'
text = '薬剤ラベルのカラー化による医療安全向上・医療従事者の働き方改革を加速する検証を開始:時事ドットコム、大阪大学医学部附属病院にカラーラベルプリンターを導入、エプソン販売株式会社は、大阪大学医学部附属病院の薬剤部門で使用する注射薬自動払出システム用にカラーラベルプリンター「CW-C6020AM」を6台、病棟に「TM-C3500」を60台導入いただき、2022年4月より薬剤ラベルのカラー化による医療安全向上・医療従事者の働き方改革の加速を目的とした検証を開始いたします。'
text = '株式会社SAKAMAは11日、魚介類の蓄養事業および販売などを手がける株式会社ダイチク佐渡とコラボし、佐渡島沖で漁れた活きた状態の南蛮エビを5尾、生鮮のものを25尾セットにして届ける食育セット「はねっ娘セット」の販売を始めた。'
text = 'ハウスクリーニング・リペア産業をIT化する日本最大級のプラットフォーム「ユアマイスター」を運営するユアマイスター株式会社は、ビルメンテナンス業界の生産性や収益性を向上するSaaS型業務支援サービス「ビルメンクラウド」を提供しています。'
text = 'スズキは、スポーツアドベンチャーツアラー「V-ストローム650」シリーズを平成32年国内排出ガス規制に対応して「V-ストローム650 ABS」を4月27日、ワイヤースポークホイール仕様の「V-ストローム650XT ABS」を3月28日より発売する。'
text = '凸版印刷株式会社は、幅広い業界/業種向けの製造DX支援ソリューション「NAVINECT」を2019年4月より、クラウド型で手軽に導入可能な「NAVINECTクラウド」を2020年5月より提供している。'
text = 'パナソニック株式会社は、モバイルの本質「軽量」「長時間」「頑丈」「高性能」を追求したモバイルノートPC「レッツノート」の2013年秋冬モデルの第2弾として、Windows 8.1を搭載した「AX3」シリーズを10月18日、「LX3」のタッチパネルモデルを11月15日より発売します。'
text = 'トップゲーム・アニメ、通販サイト大手のAmazonは、同社が展開するオーディオブック販売サービス「Amazon Audible」について、1月27日からオーディオブックの聴き放題サービスを新たに提供すると発表した。'
text = 'アスキーストアでは、細かい作業をする時に使えるライト付きのスタンドルーペ「LEDライト付ロングスタンドルーペ、」を販売中。'
text = 'パナソニック株式会社は、20,000時間の長寿命と、白と黒のコントラスト感をアップし、文字をくっきり読みやすくした「文字くっきり光」を搭載した丸形蛍光灯「パルック、20000」を2015年6月1日より発売します。'
text = '移転を機に、鉄筋コンクリート造マンション・ビル、木造建築事業を拡大する。'
text = '全日空商事は、フェイラーとのコラボ商品「FEILER for ANA」を2020年から販売。'
text = '大創産業は、「メルペイ」「au PAY」を2022年2月1日から、「楽天ペイ」を3月1日から100円ショップのDAISO、新業態のStandard Products by DAISO、THREEPPY、CouCou、Plus Heart2730店で導入する。'
text = '全国のミニストップでは、2022年1月7日から飲めちゃうデザート「グルクル飲むチーズケーキ」を販売中です。'
text = '「SINN PURETE」は、贅沢に天然由来成分を配合し、ハイブリッドナチュラル処方で植物の力を最大限に引き出した日やけ止めシリーズを新発売することをお知らせいたします。'
text = '三井不動産レジデンシャル株式会社は、2022年1月14日に当社初となるホテルライセンス型サービスアパートメント「オークウッドホテル&アパートメンツ麻布」を開業いたします。'
text = 'これによりアイティーエムは、オープンソースや内部ホストの脆弱性管理サービスの提供範囲を拡大し、セキュリティ運用をアウトソースする企業もyamoryを利用可能になります。'
text = 'そんななか北欧・フィンランド発の「WOLT」は、食品小売業との提携を加速させるほか、ダークストアを活用した独自の食品配達サービスにも着手するなど、新たな動きを見せている。'
text = '医療廃棄物などを処理する企業が、新型コロナ対応の最前線にいる医療スタッフに野菜の詰め合わせや寿司などを無料で届ける活動を始めました。'
text = 'トヨタカスタマイジング&ディベロップメントは、新型「ノア」「ヴォクシー」の発売に伴い、GRブランドのカスタマイズパーツをラインアップし、1月13日より販売を開始した。'
text = ' 株式会社ツクルバは、2022年2月10日より新サービス「ウルカモ」を提供開始します。'
text = 'LDBでは、「与信が難しいことが理由で、受けられる金融サービスが限定的になってしまっている」という中小企業の課題に対して、業界特有のデータやAIを活用した与信システムの開発に取り組み、2020年9月より一部を実用化、第一弾サービスとして建設業向けの金融サービスを提供開始しました。	'
text = 'ミニストップは、人気の「やみつキッチン」シリーズから登場する菓子パンの新商品「やみつきになる!、チョコクリームパン」を、2022年1月11日より国内のミニストップ店舗にて発売します。'
text = 'イマジニアは,氷上で行うウィンタースポーツ「カーリング」を手軽に楽しめるNintendo Switch向けソフト「みんなのカーリング」を,本日発売した。'
text = '全但バスと自動車用電子機器メーカーのデンソーテンなどは、観光客らの予約を受けて自動で経路を選び、運行するオンデマンド予約バスの実証実験を始めた。'
text = '新潟市は、自動車道の一部を歩行空間にしてテーブルやベンチを置きにぎわい空間を創出する社会を実験いたします。'
text = 'ブルボンが「ホワイトロリータアイス」を2月14日からコンビニや鉄道売店で販売開始ました。'
text = '詳しくはこちらソフトバンクと日本気象協会は1月31日、小売り・飲食業界向けの人工知能需要予測サービス「サキミル」を共同開発したと発表した。'
text = 'ASUS JAPANは、パワフルなゲーミングノートパソコンにも高いデザイン性を求めたい方に向けた、デザインにこだわったウルトラスリムなゲーミングノートパソコン「ROG Zephyrusシリーズ」4製品を発表ました。'
text = '株式会社一条工務店は、4つのインテリアスタイルを軸に、理想の空間を叶える"デザイン性"と、業界最高レベルの住宅性能により健康・快適・省エネな暮らしを実現する"住環境"を兼ね備えた、一条工務店の新ラインアップ「GRAND SMART」を、2022年1月より発売開始しました。'
text = 'ファッションとビューティーを軸にブランドディレクション、ODM事業を展開する株式会社レザボアは、コスメブランド「uneven、」より「coloring soft eyeliner thaw」「coloring soft eyeliner accumulate」「uneven eye shadow patience」を発売開始致しました。'
text = '秋田市の企業と秋田県総合食品研究センターがこのほど、秋田杉の葉の成分を配合した除菌スプレー「杉の雫」を共同開発した。'
text = '株式会社エイブル、は、エイブルにてお部屋をお申込みいただく方、これからご契約いただく方を対象とした入居者様向けアプリ「sumca」の提供を開始いたしました。'
text = '映像の企画から制作、映像編集、配信・流通に至るまでを、グローバルにワンストップでお届けする株式会社IMAGICA GROUPのグループ会社で、放送/映像関連機器の開発・製造・販売・輸出入を手掛ける株式会社フォトロンは、高品質・低遅延、映像伝送/共有クラウドサービス「Photron Live Cloud Service」のサービス提供開始に際して、任意の利用開始日から2週間無償でサービスをご利用いただける「「Photron Live Cloud Service」無償利用キャンペーン」を2022年2月14日より実施します。'
text = '合同会社フロッグワークスは、全国の視覚に障害をお持ちの方に向けたサービス「視覚障害者向けパソコン・スマホITサポートと視覚障害者専用パソコン・支援機器の販売」を行う事業「ブラインドITヘルパー」を、令和3年12月1日から開始いたしました。'
text = '加古川の仏壇・仏具店が「ファンタジー仏壇」、カスタマイズも 仏壇・仏具店「素心」が1月31日、プラスチック加工会社「匠工芸」とのコラボ仏壇「ファンタジー仏壇Prayer Spot~旅立ち~」の販売を始めた。'
text = '不動産各社が防災分野でデジタル活用を積極化している。'
text = '"日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'
text = 'ハウスクリーニング・リペア産業をIT化する日本最大級のプラットフォーム「ユアマイスター」を運営するユアマイスター株式会社は、ビルメンテナンス業界の生産性や収益性を向上するSaaS型業務支援サービス「ビルメンクラウド」を提供しています。'
text = 'LDBでは、「与信が難しいことが理由で、受けられる金融サービスが限定的になってしまっている」という中小企業の課題に対して、業界特有のデータやAIを活用した与信システムの開発に取り組み、2020年9月より一部を実用化、第一弾サービスとして建設業向けの金融サービスを提供開始しました。'
text = 'コーエーテクモゲームスは、三国志の世界を舞台にした歴史アクション&シミュレーションゲーム「真・三國無双8 Empires」を2021年12月23日に発売した。'
text = '株式会社GOESWELLは、サブスクリプションサービス「GOESWELL PLUS+」を2022年1月5日より提供開始いたします。'
text = 'NBCユニバーサル・スタジオ・グループの一つであるNBCUniversal Formatsは、カイロを拠点とするメディア制作会社TVisionとOSN、そしてUMSとタッグを組んでアラブ版の「SUITS」製作を進めている。'
text = 'テックウインドは、PGAのトッププロもパター練習ツールとして採用しているパタートレーニングツールブランド「Wellputt」から世界最古のオープンゴルフ競技である「全英オープン」とコラボレーションしたスペシャルエディション「Wellputtマット4m、全英オープンモデル」とパターストロークの軌道を矯正するストロークテンプレート「Wellstroke」の2製品を発売した。'
text = '詳しくはこちら発表日:2022年02月16日菱洋エレクトロ、光触媒技術を有するカルテックと代理店契約締結~独自の光触媒材料を用いた除菌・脱臭製品の販売を開始~エレクトロニクス商社の菱洋エレクトロ株式会社は、独自の光触媒技術を応用した除菌脱臭機の開発・販売を手掛けるカルテック株式会社と代理店契約を締結し、光触媒によりウイルスや浮遊菌を分解する除菌・脱臭製品の販売を開始しました。'
text = 'アスキーストアでは、設定した圧力なると自動停止、空気圧チェック機能もあるハイパワー電動空気入れ「PONPRO、ポンプロ、3R-IFL01」を発売中。'
text = 'パナソニック株式会社、エコソリューションズ社は、太陽光発電システムとリチウムイオン蓄電システムを連携させ、日常時も停電時も電力を安定供給する「創蓄連携システム」の新製品として、従来比約1/3のコンパクトサイズで大幅な省施工化を実現した、「創蓄連携システム パワーステーションS」の受注を、2017年4月5日より開始します。'
text = 'ロジテックINAソリューションズが、スティック型ポータブルSSD「LMD-SPBU3」シリーズを発売しました。'
text = '株式会社マネーフォワードは、2022年の確定申告シーズン到来に先立ち、個人事業主の開業支援サービス「マネーフォワード クラウド開業届」導入促進のための特設ページ「好きを仕事にする、ということ」を開設した。'
text = 'スプリングバレーブルワリーは1月28日、日本産ホップのおいしさを楽しめる限定ビール「JAPAN HOP~ペールエールタイプ~」をスプリングバレーブルワリー京都で数量限定で提供を開始する。'
text = 'ボックス型ブース「隠れ家ワークスペース「森の箱」」を開発、受注販売を始めた。'
text = '湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'
text = 'グローバル刃物メーカーの貝印は、デリケートゾーンの毛量を適度に調整できる「FEMINICARE、すきカミソリ、2本入」を、2022年3月8日より貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売しました。'
text = '1933年の創業以来、フェルト帽や天然草を加工する型物を中心に帽子づくりをおこなってきた東ハットは、思い出の通園・通学帽を小さくリメイクするサービス「思い出ハットプロジェクト」を始動。'
text = 'グローバル刃物メーカーの貝印株式会社は、「ねこ」をテーマとしたビューティーツールシリーズ「Nyarming」の新商品「ねこのシャンプーグローブ」「ねこの洗顔ブラシ」を、2022年3月8日より、貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売いたします。'
text = '4大共通ポイントの事業者が運営するシステムと1つのゲートウェイで接続できるクラウドサービス「PointInfinity、マルチポイントゲートウェイ」を1月26日から提供開始します。'
text = '伊藤忠商事グループの株式会社Belongは、同社が提供する法人向け中古端末のレンタル・販売サービス「Belong One」にて、「Android Enterprise Device Reseller、認定取得」及び「Android Enterprise Essentials」の提供を記念し、法人のお客様により手軽かつセキュアな状態で、Android、端末をご導入頂けるよう、キャンペーンを開始いたします。'
text = 'テックウインドは、PGAのトッププロもパター練習ツールとして採用しているパタートレーニングツールブランド「Wellputt」から世界最古のオープンゴルフ競技である「全英オープン」とコラボレーションしたスペシャルエディション「Wellputtマット4m、全英オープンモデル」とパターストロークの軌道を矯正するストロークテンプレート「Wellstroke」の2製品を発売した。'
text = '日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'
text = 'アジア太平洋地域で最大級の独立系再生可能エネルギー発電事業者であるヴィーナ・エナジーは、鳥取県西部エリア4町において、自分たちの暮らしている地域をもっと元気に、より良くしたいなどの熱い思いで"地域共創"を目指す事業者や個人を応援するファンディング・プロジェクト「地域の元気、応援プロジェクト、Powered by、日本風力エネルギー」を開始します。'
text  = 'バックアップサービスの提供開始について:時事ドットコム、~バックアップ・復元の一元管理機能・セキュリティ機能をまとめてご提供~、エヌ・ティ・ティ・スマートコネクト株式会社は、お客さまのオンプレミス環境や当社が提供するクラウド環境等の様々なプラットフォームにおいて、データのバックアップ・復元の一元管理が可能となる「バックアップサービス」を提供開始いたします。'
text = 'すべての人に「美」と「健康」の提供を目指す総合美容メーカーの株式会社エストラボは、2022年2月28日までに、業務用脱毛機「LUMIX-A9」または、最新ダイエットマシン「LUMIX MAGFORCE」の無料デモ体験会、無料出張デモをお申し込み後、成約頂いたお客様にラジオ派マシン「Cutey UP」を1台プレゼントする、お年玉キャンペーンを実施いたします。'
text = '"持たない豊かな住まい方"を実現する新サービスをパナソニックが開始した。'
text = 'Lenovoは5日、ゲーミング向けノートPC「Legion」シリーズを第12世代Core、および次世代Ryzenプロセッサ搭載モデルに刷新した。'
text = '"アウトドアを通して生活を明るく豊かに"がコンセプトのキャンプ・アウトドア用品メーカー「outstand」から登場した、新感覚LEDライト「エアーチューブライト」が、応援購入サービス「Makuake」にて、2月24日より先行販売中だ。'
text = '読売新聞の記事によれば、防衛省が敵対的なドローンを無力化できる「高出力マイクロ波」兵器の研究開発に乗り出すそうだ。'
text = 'ソラコムは1月18日、オンラインセミナー・ワークショップ「事例から学ぶ!失敗しないIoTプロジェクトの始め方」を開催する。'
text = 'パナソニック株式会社、デジタルAVCマーケティング本部は、日本語・英語活字カラーOCRソフトの最新製品「読取革命Ver.14」を2月12日より発売します。'
text = 'Supership株式会社とKDDI株式会社は、共同運営するSMS送信サービス「KDDI Message Cast」を、新型コロナウイルス感染者への連絡手段として効果的に活用頂くため、お申込みいただいた即日からSMS送信のご利用が可能な全国の自治体および医療機関を対象とした特別プランの提供を開始しました。'
text = '松屋フーズは、同社が展開する牛めし・カレー・定食の「松屋」において、「キムチ牛鍋」を1月11日15時に、「焼キムチ牛めし」を1月18日10時に発売する。'
text = '株式会社Lentranceは、同社の学習用ICTプラットフォーム「Lentrance」と連動して動作する学習履歴データ分析基盤、「Lentrance Analytics」の商用提供開始を発表いたします。'
text = '株式会社、学研ホールディングスのグループ会社、株式会社、学研プラスは、iOSアプリ「英語の図鑑で楽しく学ぼう!、こどもえいごずかん」を2022年1月5日に配信開始いたしました。'
text = '株式会社湖池屋は、ホクレン農業協同組合連合会の協力により原料に北海道産米を使用した、濃厚ノンフライ・たんぱく質入りの新しい米スナック「愛をコメて、ガリシュリ」、「愛をコメて、ミートドリア」を2022年1月24日より全国コンビニエンスストア、湖池屋オンラインショップにて発売します。'
text = '中小機構北陸本部、鯖江市、鯖江商工会議所は、持続可能な開発目標への対応を通じた企業の経営課題解決の取組みとして、3機関の連携により、SDGsに貢献する商品の販路開拓支援を開始します。'
text = '*、西日本鉄道株式会社は、いすゞ自動車株式会社、三菱商事株式会社、福岡国際空港株式会社と共同で、福岡空港内において大型自動運転バスを用いた自動運転の実証実験を2022年3月8日より実施いたします。'
text = '詳しくはこちらゆでたマカロニとあえるだけで、おつまみを作れるエスビー食品はマカロニとあえるだけでおつまみを作れる「OTSUMAMI Trattoria」を2月7日に発売する。'
text = '長野県塩尻市は、2021年10~11月にネットワンシステムズと共同で、物理破壊ではなくデータ消去を行う方法でのプロセスを実証実験で検証した。'
text = 'ゼロ・エミッション型のイベントの実現を目指す株式会社、博展は、プラスチック総合商社の緑川化成工業株式会社と、当社が展示会・イベント等で排出するアクリルを再生率80%のアクリルに再生し、再活用をするクローズド・リサイクルの試験運用を開始いたしました。'
text = '*、西日本鉄道株式会社は、いすゞ自動車株式会社、三菱商事株式会社、福岡国際空港株式会社と共同で、福岡空港内において大型自動運転バスを用いた自動運転の実証実験を2022年3月8日より実施いたします。'


# 解析誤り
text = 'ホンダは二足歩行の人型ロボット「ASIMO」に代表されるロボティクス技術の開発を長年行ってきた。'

#################
#text = '調査を開始した。調査を開始している。調査を開始する。調査を開始したい。調査を開始したくない。調査を開始してこなかった。'

# subject のとり方　連体修飾を取りたい
text = 'ファッションとビューティーを軸にブランドディレクション、ODM事業を展開する株式会社レザボアは、コスメブランド「uneven、」より「coloring soft eyeliner thaw」「coloring soft eyeliner accumulate」「uneven eye shadow patience」を発売開始致しました。'
# subject のとり方　アイリスオーヤマと、ソフトバンクグループの子会社　が取りたい
text = '生活用品メーカー大手のアイリスオーヤマと、ロボット開発を手がけるソフトバンクグループの子会社が資本業務提携し、飲食店やホテル向けに配膳ロボットの開発・販売を強化することになりました。'
#　〇〇から〜発売中　→　〇〇　が　発売する　　〇〇が発売中　→　〇〇　を　発売中　に解釈する
text = 'オンラインショップ「KALE FARM」から、無農薬・無化学肥料で育てたケールのコールドプレスジュースと、イギリス発のオーガニックオーツミルクを組み合わせた新作ケールジュース「ケールオーツミルク」が、1月21日より発売中だ。'
# 計画　を取りたい
text = '金沢大発ベンチャー「Kanazawa Diamond」が、独自技術で人工的に製造した黒いダイヤモンドの販売を2022年秋ごろに始める計画だ。'
# 代名詞の照応
text = '同社傘下のベンチャー企業で酸化ガリウムウエハーの開発及び製造販売を手掛けているノベルクリスタルテクノロジーが、昨年12月下旬に酸化ガリウムを材料とする高電圧対応のパワー半導体ダイオードの開発を発表、これがタムラの株価を強く刺激する形となり、ストップ高を交え828円まで急騰する経緯があったが、その後は売り物に押され急反落を余儀なくされていた。'




#text = '酒菜と串揚げ、釜めしが自慢のレストラン「ごはん酒菜そのに」は、アジフライ専用「味和伊ソース」を開発し、オンラインショップで販売している。'
#text = '株式会社伊と幸は、2022年2月8日から2月9日に開催の「KIMONOの森、音楽ライブ&展示会」において、サステナブル素材としての「絹」の魅力と価値を、楽しく、簡単に学ぶことができるメタバース「繭の小道」を発表、展示いたします。'
#text = '日東工業のEV普通充電器「Pit-2G」とENECHANGEが開発したEVドライバー向け専用システムを連携させたサービスを開始した。'
#text = 'インプレスグループで山岳・自然分野のメディア事業を手がける株式会社山と溪谷社は、東京都内&周辺の"端っこ"をめぐる散歩エッセイ&ガイド、「東京休日端っこ散歩」を2022年2月17日に刊行しました。'
#text = 'プラント大手の日揮や全日空、日本航空、日清食品など16社は温室効果ガスの排出量が少ない次世代航空燃料=SAFの国内での商用化と普及を目指す団体を立ち上げました。'
#text = 'Y&Y STOREは、本日2022年2月24日よりコスパ抜群のレーザー彫刻機「Runmecy D4」を、GREEN FUNDINGにて販売を開始しました。'
#text = 'オーダーメイド枕の店まくらぼは、2017年から横浜F・マリノスを睡眠の観点からサポートし、オーダーメイド枕などの寝具の提供や、アスリートがパフォーマンスを発揮するための睡眠学セミナーなどを行っています。'
#text = 'ホンダアクセスは、ホンダが展開するカーシェアサービス「EveryGo」の一部車両に、運転支援や車内の快適性を高めるための純正アクセサリーを装着し、EveryGoでの安心・快適なドライブをサポートする。'
#text = 'コロナ禍で住まいの環境をよくするため家具への関心が高まり、需要が見込めると判断した。'
#text = '株式会社ワンインチはカンナビジオールを含む機能性食品素材を健常志願者が摂取した時の安全性確認オープンラベル試験をアポプラスステーション株式会社に委託し実施した。'
#text = '大建工業株式会社は、多湿時に湿気を吸収して乾燥時に放出し、においも抑制する調湿壁材「さらりあ〜と」シリーズを、5月21日より大幅にリニューアルして発売します。'
#text = '暮らしにイロドリとプラスの価値を創造する製品・サービスを提供するライフオンプロダクツ株式会社から、柔らかい食材や、切りずらい食材も力や技術を使わずに断面をキレイにスッと切れる充電式電動ナイフ"PRISMATEコードレスオートマルチナイフ"を2022年2月18日より販売いたします。'
#text = 'GHG排出量算定・可視化クラウドサービス「zeroboard」を開発・提供する株式会社ゼロボードは、大崎電気工業株式会社、エネルギーアンドシステムプランニング株式会社とともに、企業の脱炭素化に向けた支援に関する協業を開始いたします。'

#text = 'AvePoint、安全性の高いデジタル コラボレーションを実現するバーチャル データ ルーム、「Confide」、をリリース:時事ドットコム、Confide、は、効率性を損なうことなく機密データを保護したいというニーズの高まりに対応します。'
#text = '日本ピザハット株式会社が展開する世界最大のピザチェーン「ピザハット」は、おひとりさま専用ピザセット「MY BOX」が2022年1月12日で全国発売1周年を迎えることを記念して、1月11日より"この冬食べたい「MY BOX」ランキング"1位を獲得し、チーズ好きにはたまらない「ピザ」と「グラタン」をセットにした「グラタンMY BOX」を販売開始いたします。'

#text = 'すべての人に「美」と「健康」の提供を目指す総合美容メーカーの株式会社エストラボは、2022年2月28日までに、業務用脱毛機「LUMIX-A9」または、最新ダイエットマシン「LUMIX MAGFORCE」の無料デモ体験会、無料出張デモをお申し込み後、成約頂いたお客様にラジオ派マシン「Cutey UP」を1台プレゼントする、お年玉キャンペーンを実施いたします。'

#text = 'パナソニック株式会社は、グランフロント大阪、南館内に展開する、お客様と共に新しい価値を生み出すショウルーム「パナソニックセンター大阪」の2階「LIFE STYLE Floor」にあるセルフエステ&パウダールームCLUXTAにおいて、2014年11月21日から、関西で唯一、Panasonic Beauty PREMIUMシリーズ3機種をじっくりお試しいただける「PREMIUMセルフエステコース」がスタートいたします'
#text = '大丸松坂屋百貨店は、アートとアートを買うことの魅力をお届けする初のアートメディア「ARToVILLA」を、2022、年、1、月、7、日スタートいたします。'

#text = 'バッグメーカーのエース株式会社は、働く女性が1週間を最高に気持ち良く始めるためのお仕事バッグを提案するブランド「W&.Day/Night」より、廃棄予定だったりんごの皮や廃材などをリサイクルした素材を使用したサステナブルなビジネスリュック「ポエット アップルレザーリュック」と「リッカ スクエアリュック」を、公式オンラインストアにて発売開始しました。'

#text = 'アイディアファクトリー株式会社の子会社である株式会社コンパイルハートは、本日Nintendo Switch版「限界凸旗、セブンパイレーツ、H」を発売開始しました。'
#text = 'ウィメンズアパレルブランド「RANDEBOO」が、1月14日18:00より「2022 PRE Spring/Summerコレクション」を発売開始した。'
#text = '太郎を共同開発したと発表した。'

#text = '"日本全国に料理と飲み物を1箱にしたフードボックス"をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'

text = 'NBCユニバーサル・スタジオ・グループの一つであるNBCUniversal Formatsは、カイロを拠点とするメディア制作会社TVisionとOSN、そしてUMSとタッグを組んでアラブ版の「SUITS」製作を進めている。'

text = '立命館大学と、立命館アジア太平洋大学が、AIチャットボットを導入しました。'
text = '太郎と、花子は本を読んだ。太郎と花子は本を読んだ。'
text = '生活用品メーカー大手のアイリスオーヤマと、ロボット開発を手がけるソフトバンクグループの子会社が資本業務提携し、飲食店やホテル向けに配膳ロボットの開発・販売を強化することになりました。'
text = '太郎がテーブルと椅子を運んだ。'

#text = '自転車こいで靴下編もう、「チャリックス」、体験施設、奈良県広陵町の靴下メーカー「創喜」が、自転車をこいで靴下を編める機械を作り、自社の敷地内に体験施設「S.Labo」を開いた。'

text = '「Grandioso M1X」、エソテリックは、発売を延期していたモノブロック・パワーアンプ「Grandioso M1X」を、3月に販売開始する。'

text = 'NECネッツエスアイと住友理工、バイタルセンサーを活用したホテルサービスの実証実験を開始:時事ドットコム、~睡眠状態の可視化により快適な宿泊環境と良質な眠りを実現~NECネッツエスアイと住友理工は、ルームマネジメントシステムとバイタルセンサー「モニライフ」を組み合わせたホテル向けサービスの実証実験を本日よりホテル コレクティブにて開始します。'
text = 'ベーカリーカフェ「パンとエスプレッソと」をはじめ、国内で22店舗を展開する日と々とが、パニーニ専門店「パニーニ一番」を千駄ヶ谷に出店する。'
text = '株式会社グランディール ジャパンは、今だけでなく将来のためにも肌のベースづくりと栄養補給が大切であることに着目し、ヒト臍帯血細胞順化培養液をはじめとする4つの"覚醒"成分1 2とプラセンタエキスなどの有用成分1を黄金比で配合した"攻めの美容液"「FABULOUS ONE、スキンセラムRE」を開発し、2022年1月26日に公式サイトにて販売を開始いたします。'
text = 'Supership株式会社とKDDI株式会社は、共同運営するSMS送信サービス「KDDI Message Cast」を、新型コロナウイルス感染者への連絡手段として効果的に活用頂くため、お申込みいただいた即日からSMS送信のご利用が可能な全国の自治体および医療機関を対象とした特別プランの提供を開始しました。'
text = '中小機構北陸本部、鯖江市、鯖江商工会議所は、持続可能な開発目標への対応を通じた企業の経営課題解決の取組みとして、3機関の連携により、SDGsに貢献する商品の販路開拓支援を開始します。'
text = '大成建設など9社は1月20日、新宿駅西口エリアにおいて自動運転車を使ったサービスの実現へ向けた実証実験を開始すると発表した。'
text = 'パナソニック株式会社、オートモーティブ&インダストリアルシステムズ社は、SSDポータブルカーナビゲーション「ゴリラ」の新製品5機種を9月20日より順次発売します。'
text = '東京を中心に認可保育所をはじめとする子ども・子育て支援事業を展開する株式会社さくらさくプラス、の子会社、株式会社みらいパレット、は、テクノロジーと情報で子育て世帯をサポートするサービスの開発をしています。'
text = '小田急電鉄は2022年1月20日、新宿駅前の「小田急ホテルセンチュリーサザンタワー」にて、シミュレータによる運転体験ができる宿泊プランを2月1日に開始すると発表しました。'
text = '神奈川県・三崎発祥のドーナツ専門店「ミサキドーナツ」と横浜生まれのチョコレートブランド「VANILLABEANS」がコラボドーナツ「カカオジュエリー」を1月7日から発売。'
text = 'パナソニック システムソリューションズ ジャパン株式会社は1日、株式会社読売巨人軍、株式会社読売新聞東京本社、株式会社東京ドームの3社が、東京ドームでの一般来場者を対象とした入場・決済サービスにパナソニックの顔認証技術を採用したと発表した。'
text = '間もなく中国の旧暦正月を迎えるのを機に、中国の嵩山少林寺と世界各地の少林文化センターは、国際的なカンフーコンテストである「Happy Chinese New Year: Shaolin Kung Fu Online Games」を開始した。'
text = '名刺管理サービスを新たに「名刺バンク2」として提供開始独立系データセンタープロバイダーである株式会社アイネットは、2013年より法人向けクラウド型名刺管理サービス「名刺バンク」を提供しており、延べ約550社以上の企業様にご利用いただいてまいりましたが、新たに「名刺バンク2」を2022年1月より提供開始します。'
text = '株式会社日立製作所、SBテクノロジー株式会社、国立大学法人東京大学、日本電気株式会社、富士通株式会社、大学共同利用機関法人、情報・システム研究機構、国立情報学研究所、株式会社NTTデータ、JIPテクノサイエンス株式会社の8団体は28日、「ビッグデータ・AIを活用したサイバー空間基盤技術」の研究開発において、分散型の分野間データ連携基盤技術を開発し、社会実装に向けて実証を開始したと発表した。'
text = 'パナソニック、、ロフトワーク、、カフェ・カンパニーが運営する100年先を豊かにするための実験区・100BANCHで活動する異言語Lab.は、、手話を取り入れた謎解きゲーム「異言語脱出ゲーム」の最新作「うしなわれたこころさがし」を、、東京・渋谷の100BANCHで、、3月20日、、21日の2日間に渡って開催。'

#text = 'GiRAFFE&Co.は、レンタルオフィスやシェアオフィス、コワーキングスペースなど、運営会社の独自ルールに基づいて提供される「フレキシブルオフィス」と利用者をつなぐマッチングプラットフォーム「OFiT」を立ち上げ、今春の提供開始を予定している、と発表した。'

#text = '店舗運営者・マーケティング担当の方向け~今後のリアル店舗の在り方~:時事ドットコム、~ポップアップイベントの最新動向と空きスペースの活用方法~、印刷・集客のシェアリングプラットフォームを展開するラクスル株式会社は多拠点大企業向けに販促管理ツールを提供しています。'
#text = '自宅でビールを原料から醸造できる新たな家電が登場した。'

#text = 'ホンダとソニーは車と飛行機の開発を進める'

text = '重篤な感染症に対する次世代ワクチンの開発と商品化を専門とするバイオテクノロジー企業Novavax, Inc.は21日、欧州委員会が、SARS-CoV-2が引き起こすCOVID-19予防のため、18歳以上の個人に対する能動免疫法として、NovavaxによるCOVID-19ワクチン「Nuvaxovid」の条件付き販売を承認したと発表した。'
text = '暮らしにイロドリとプラスの価値を創造する製品・サービスを提供するライフオンプロダクツ株式会社から、柔らかい食材や、切りずらい食材も力や技術を使わずに断面をキレイにスッと切れる充電式電動ナイフ"PRISMATEコードレスオートマルチナイフ"を2022年2月18日より販売いたします。'
text = 'ハンファQセルズジャパンと住友電気工業は2022年3月1日、太陽電池モジュールとハイブリッド蓄電システムを一体化した、住宅向けの太陽光発電の自家消費システムを開発すると発表した。'

#text = '東芝、ソニーほか、数社が開発を開始した。'
#text = 'NECは1月4日、警視庁向けに、75歳以上の高齢者が運転免許更新時に受ける認知機能検査時、電話予約に加えスマートフォンやパソコンからインターネットで24時間予約を受付するシステムを構築し、都内の運転免許試験場で運用を開始したと発表した。'
#text = '大建工業は8月1日、上面放熱率が床暖房業界最高の90%以上を達成し、40Cの低温水でも快適な暖かさを実現した省エネタイプの高効率床暖房システム<高効率パネル「エコリード」+専用仕上材「サーモタフ」>を発売します。'
#text = 'そんななか北欧・フィンランド発の「WOLT」は、食品小売業との提携を加速させるほか、ダークストアを活用した独自の食品配達サービスにも着手するなど、新たな動きを見せている。'
#text = '加古川の仏壇・仏具店が「ファンタジー仏壇」、カスタマイズも 仏壇・仏具店「素心」が1月31日、プラスチック加工会社「匠工芸」とのコラボ仏壇「ファンタジー仏壇Prayer Spot~旅立ち~」の販売を始めた。'
#text = '企業向けのデジタルマーケティング支援事業他を手掛ける株式会社バケットは、これまでSNSをはじめとしたデジタルコミュニケーションの企業向け支援サービスを提供し、運用を代行する形で企業と消費者の関係性を築くお手伝いをしてきました。'
#text = 'イオン・シグナ・スポーツ・ユナイテッド株式会社は、スポーツバイクEC専門ショップ「Probikeshop」において、株式会社自転車創業が展開する日本最大級の自転車メディア「FRAME」とコンテンツ面で連携を強化し、EC領域の協業に加え、動画の共同コンテンツ制作を展開していきます。'
#text = 'キリンビバレッジ株式会社は、「トロピカーナ」の、季節のおいしさを楽しみながら栄養補給もできる100%果実飲料"の「ヘルシーフルーツ」シリーズの第3弾として、「トロピカーナ ライチ&グレープフルーツテイスト」を、4月5日より全国で季節限定にて新発売します。'
#text = '日本RV協会は2月9日、今後もさらなる拡大が見込まれるキャンピングカー需要に応えるため、最大240回払いが可能な「JRVA特別オートローン」の提供を開始すると発表した。'
#text = 'NECネッツエスアイは、ビデオ会議サービス「Zoom」を運営する米ズーム・ビデオ・コミュニケーションズが提供するクラウド型の音声サービスに、手軽に利用できる独自サービスを追加すると発表した。'
#text = 'NECは1月4日、警視庁向けに、75歳以上の高齢者が運転免許更新時に受ける認知機能検査時、電話予約に加えスマートフォンやパソコンからインターネットで24時間予約を受付するシステムを構築し、都内の運転免許試験場で運用を開始したと発表した。'
#text = '横浜ゴムは2月22日、スズキのインドにある子会社マルチ・スズキ・インディアが2021年11月に発売した新型「セレリオ」向けに、新車装着用タイヤの納入を開始したと発表した。'

text = '国内製薬会社23社に採用:製薬業界のデジタル化を推進するドキュサインの電子署名:時事ドットコム ドキュサイン・ジャパン株式会社は、国内の製薬企業23社がドキュサインの電子署名ソリューション「DocuSign eSignature」を導入し、業務プロセスのデジタル化を実現していることを発表しました。'

text = '創業初期から、NIMASOは、スマートフォンに関連するアクセサリーの開発販売に力を入れ、ブラントを発展させました。'
text = '国内製薬会社23社に採用:製薬業界のデジタル化を推進するドキュサインの電子署名:時事ドットコム ドキュサイン・ジャパン株式会社は、国内の製薬企業23社がドキュサインの電子署名ソリューション「DocuSign eSignature」を導入し、業務プロセスのデジタル化を実現していることを発表しました。'
#text = '東京建物株式会社のグループ会社で、マンション管理運営部門を担う株式会社東京建物アメニティサポートは、マンション大規模修繕工事の周期を12、年から最大18、年に延長できるサービス「Ever Graceful、」、の提供を開始しますのでお知らせいたします。'
#text = 'グループ傘下の対話アプリViberでは、ウクライナで音声通話機能を無料で利用できるクーポンも配布している。'
#text = 'ブックシェルフスピーカー「SB-C600」、パナソニックは、Technicsブランドの新製品として新開発の同軸ユニットを採用した小型ブックシェルフスピーカー「SB-C600」を2月25日に発売する。'



text = '創業初期から、NIMASOは、スマートフォンに関連するアクセサリーの開発販売に力を入れ、ブラントを発展させました。'
#text = '国内製薬会社23社に採用:製薬業界のデジタル化を推進するドキュサインの電子署名:時事ドットコム ドキュサイン・ジャパン株式会社は、国内の製薬企業23社がドキュサインの電子署名ソリューション「DocuSign eSignature」を導入し、業務プロセスのデジタル化を実現していることを発表しました。'
#text = '「OptiNAND」技術を採用したWestern Digitalのデータセンター向け20TB HDD「Ultrastar DC HC560」が登場、オリオスペックが非SEDモデル「WUH722020ALE6L4」の販売を開始した。'
#text = '株式会社グランディール ジャパンは、今だけでなく将来のためにも肌のベースづくりと栄養補給が大切であることに着目し、ヒト臍帯血細胞順化培養液をはじめとする4つの"覚醒"成分1 2とプラセンタエキスなどの有用成分1を黄金比で配合した"攻めの美容液"「FABULOUS ONE、スキンセラムRE」を開発し、2022年1月26日に公式サイトにて販売を開始いたします。'
#text = 'コンピュータートレーニング教材制作、eラーニング向けコンテンツ制作のアテイン株式会社は、月額2,800円で様々な動画講座が視聴し放題のクラウドeラーニングサービス「動学.tv」に、事務に必須のツール「Microsoft Word 2019」の使い方が字幕付きの動画で学べる「Microsoft Word 2019、使い方」講座を2巻構成で、1月24日に公開します。'
#text = '店舗運営者・マーケティング担当の方向け~今後のリアル店舗の在り方~:時事ドットコム、~ポップアップイベントの最新動向と空きスペースの活用方法~、印刷・集客のシェアリングプラットフォームを展開するラクスル株式会社は多拠点大企業向けに販促管理ツールを提供しています。'


#text = '国内製薬会社23社に採用:製薬業界のデジタル化を推進するドキュサインの電子署名:時事ドットコム ドキュサイン・ジャパン株式会社は、国内の製薬企業23社がドキュサインの電子署名ソリューション「DocuSign eSignature」を導入し、業務プロセスのデジタル化を実現していることを発表しました。'
#text = '東京建物株式会社のグループ会社で、マンション管理運営部門を担う株式会社東京建物アメニティサポートは、マンション大規模修繕工事の周期を12、年から最大18、年に延長できるサービス「Ever Graceful、」、の提供を開始しますのでお知らせいたします。'
text = 'くふうグループにおいて、子ども向け社会体験アプリ「ごっこランド」を展開する株式会社キッズスターは、一般社団法人JFTD花キューピット及び花キューピット株式会社とのコラボレーションにより、2022年3月1日~3月31日の期間、「お花1本プレゼントキャンペーン」を実施します。'



#para
#text = '晶合光電は2011年に設立され、完成車工場と共同で発光ダイオードモジュールの研究開発や設計を行い、デジタル化、インテリジェント化された車載用ライトを生産する。'
#text = 'モビリティハウスは20フィートコンテナハウスで、蓄電地、プラグインハイブリットガス発電、温水床暖房、潜熱回収型ガス給湯器、太陽光発電設備、水循環設備、最新高断熱材、LED設備、UV-C空気浄化、24時間換気などの設備を導入した。'
#text = '日本製紙株式会社は、CO2吸収能力が高く成長に優れ、花粉量が少ない等の特徴を持つエリートツリー等の苗生産事業を全国に拡大していきます。'
#text = 'アステリア株式会社は、ノーコード1のモバイルアプリ作成ツール「Platio」が、大型家電・家具の発送・設置などの運輸業を手がける株式会社コネクストに導入されたことを発表します。'
#text = 'コンビニエンスストア「ミニストップ」では、"やみつき"の味が自慢のオリジナルフードブランド・やみつキッチンの新メニュー「チャーシュー弁当」の発売を1月11日よりスタート。'
#text = '宇宙農業の実現に向けて月の模擬砂を用いた植物栽培実験に成功:時事ドットコム、株式会社大林組と、株式会社TOWINGは共同で、月の模擬砂と有機質肥料を用いた植物栽培を実証実験し、作物の栽培に成功しました。'
#text = '親子丼ギフトが大人気の大阪「鼓道」が打ち立て蕎麦の「鴨せいろ」の全国通販を開始。'
#text = 'ヨギボーは座り方に合わせ形状が自由に変わるビーズソファが人気で、日米以外にもカナダや韓国、オランダなど世界8カ国に展開している。'

# subj
text = 'プライベートバンキングやウェルスマネジメントを中心に展開するイタリアの銀行、バンカ・ゼネラリが、ビットコイン企業のConioと協力してビットコインサービスを顧客に提供する予定であることがわかった。'
text = '会社のルーツは1958年にタイルと衛生陶器の販売を始めた大亀商事で、事業拡大の中で環境にも着目していこうと、浄化槽など排水処理技術の開発を進めてきました。'
text = '酒菜と串揚げ、釜めしが自慢のレストラン「ごはん酒菜そのに」は、アジフライ専用「味和伊ソース」を開発し、オンラインショップで販売している。'
text = 'LDBでは、「与信が難しいことが理由で、受けられる金融サービスが限定的になってしまっている」という中小企業の課題に対して、業界特有のデータやAIを活用した与信システムの開発に取り組み、2020年9月より一部を実用化、第一弾サービスとして建設業向けの金融サービスを提供開始しました。'
#text = 'ビジネス現場のコミュニケーションツール「LINE WORKS」を提供するワークスモバイルジャパン株式会社は、お使いのLINE WORKS IDのQRコードが印刷されたシール100枚を、先着500名様に無料でお届けする「"あなた専用のQRコード"、シールでお届けキャンペーン」を開始することをお知らせいたします。'
#text = 'エンブラエル、ウィデロー、そしてロールス・ロイスの3社は2月17日、ゼロ・エミッション型のリージョナル航空機のコンセプトの共同研究を推進する計画を発表した。'
#text = 'NECは10日、地上で撮影された景観画像と、衛星画像・航空写真を照合することで、景観画像が撮影された場所を推定する技術を開発したと発表しました。'
#text = 'さまざまなサービスが存在するが、Kids Publicは産婦人科・小児科に特化してオンライン医療相談を提供、BtoBtoCモデルで企業・自治体の需要を開拓している。'
#text = '10兆ドルを超えるAUMを持つ世界最大の資産運用会社BlackRockが、仮想通貨取引サービスを提供する予定であることを大手メディアが報じた。'
#text = '分散型エコシステムを活用した決済アプリが2022年3月以降にリリース予定であることを発表しました。'
#text = 'ビジネス統計スペシャリストで「Odyssey CBT+」の運用をスタート:時事ドットコム、新しい配信方式「Odyssey CBT+」の運用を開始します470万人が受験しているマイクロソフト オフィス スペシャリストの実施・運営や、VBAエキスパート、ビジネス統計スペシャリストの認定を行う株式会社オデッセイ コミュニケーションズは、2022年2月より、新しい受験方法として「Odyssey CBT+」の運用を開始します。'

text = 'TWITTERが、元ツイートやリプライからタグ付けを解除できる新機能「この会話を離れる」をテストしている可能性があると報じられました。'
text = 'サンワサプライ株式会社が運営している直販サイト「サンワダイレクト」では、テレビやパソコンに接続して迫力あるサウンドを楽しめる薄型サウンドバー「400-SP100」を発売しました。'
text = '毎日のSNSやオンラインゲームに忙しい学生が増えている中、"強制的な学習時間を提供する"というコンセプトの、オンラインサービス「ハビット」が登場した。'
#text = 'サンワサプライ株式会社が運営している直販サイト「サンワダイレクト」では、机上をすっきり整理でき、電源タップやスマートフォン、タブレットの設置も可能なケーブルボックス「200-CB038」を発売しました。'
#text = 'マヴィックジャパンは、アルミリムモデルのKSYRIUMシリーズにおいて、低価格ながらマヴィックの優れたクオリティとパフォーマンスを手にすることができる最新モデルをリリースした。'
#text = "D'Artsは、VRコンテンツ制作にかかる膨大な制作コストと時間、技術の取得が難しくVRクリエイターが育ちにくいという課題に着目し、日本のVR業界全体の活性化に貢献したいという想いから、2020年よりノンコードでVRアニメを制作できる「ハッチポットビルダー」を開発しております。"

text = '湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'


text = '自宅でビールを原料から醸造できる新たな家電が登場した。'
text = 'そんなサステナブルブランドの先駆者であるパタゴニアから、PC周辺機器を簡単に取り出せるパッド入りスリーブを備えたデイパック「レフュジオ・デイパック」が登場。'
text = 'グループ傘下の対話アプリViberでは、ウクライナで音声通話機能を無料で利用できるクーポンも配布している。'
text = '高校、大学や企業などにお金やビジネスに関する研修を提供している合同会社「FPal」では、「お金」についての知識をつけることで、前向きに生きていく学生や社会人になってもらおうと、ファイナンシャル・プランナー資格を持つ社員が独自に開発したゲーム形式のプログラム「Gトレ」を展開しています。'
text = '福岡市西区のマリノアシティ福岡で、再生可能エネルギーを活用した実証実験が行われています。'
text = 'カスタマイズパーツメーカーで、レンタカーやカーシェアリング事業を展開する動きが広がっている。'
text = '無料診断から始めるDX推進! IT部門や情報システム部/担当の課題負荷低減へ:時事ドットコム、~無料で業務負担の低減と改善を診断・支援可能な、サービス、情報システム コンシェルジュサービスをリリース~株式会社エスエヌシーは、業務負荷が高まっている情報システム業務を、知見を持つ経験者が無料診断で最適サービスの提供を行う「情報システム コンシェルジュサービス」をリリースしました。'
text = 'そのもみ殻に含まれるガラスを使い、高い容量と高い耐久性を持つリチウムイオン電池の製造が、最近、欧米をはじめ複数の研究グループより報告されています。'
text = 'フォーティネットジャパン合同会社は25日、メールセキュリティ製品「FortiMail、セキュアEメールゲートウェイ」を利用する顧客がオプションとして利用できる、クラウドサンドボックス機能「FortiMail Cloud Sandbox」について、国内データセンターでの運用開始を発表した。'
text = '総務省が所管する地方公共団体情報システム機構は26日、マイナンバーカードを使って、コンビニで住民票など証明書を交付するサービスが各地で一時利用できなくなっていると明らかにした。'
text = 'ティアックから、デスクトップでハイレゾ音楽を楽しめるコンパクトサイズのUSB DAC/プリメインアンプ「AI-301DA-Z」が、1月29日に発売される。'
text = '北九州市小倉北区の小倉城で17日夜、城壁や石垣に色鮮やかな映像を投影する「デジタル掛け軸」が披露された。'
text = '1977年よりレトルトおでんを製造している丸善は、あたたかいおでんを食べる機会が少ない春夏の季節にも、日本の伝統的食文化である「和食」のひとつ「おでん」の魅力を発信できるよう、商品開発に励んでおります。'

text = 'ライフカルチャープラットフォーム「北欧、暮らしの道具店」において、雑貨や衣類などの開発・販売、メディア運営などを開発する株式会社クラシコムは、累計3万2千本を販売する「春いちボトムス・秋いちボトムス」シリーズから、「春いちボトムス2022」を2月17日に新発売します。'

text = 'ノーススターでは、"子どもの健康に寄り添うをコンセプト"に、小児の健康相談アプリ「キッズドクター」を展開しておりますが、そのチャット健康相談サービスの中でも、小さなお子様を持つ親御さんより「子どもが発達障害かもしれない」、「体調不良の子どもが発達障害を持っているため言葉がスムーズに出ず、どうしてあげたらよいかわからない」といったご不安の声も頂いております。'
#text = 'LDBでは、「与信が難しいことが理由で、受けられる金融サービスが限定的になってしまっている」という中小企業の課題に対して、業界特有のデータやAIを活用した与信システムの開発に取り組み、2020年9月より一部を実用化、第一弾サービスとして建設業向けの金融サービスを提供開始しました。'
#text = 'グループ傘下の対話アプリViberでは、ウクライナで音声通話機能を無料で利用できるクーポンも配布している。'
#text = '学校では太郎が本を読む'

#text = '工事現場の重機による騒音も将来的には消え去るかもしれない、アメリカの建設機械メーカー、ボブキャット社が、世界初の電動ブルドーザー「T7X Compact Track Loader」を開発した。'
#text = '組織・人材開発コンサルティングのインパクトジャパン株式会社は、新入社員の教育担当を対象とする研修「ENCOURAGE」を、2022年も継続して提供することを決定しました。'
#text = 'バッグメーカーのエース株式会社は、バッグ&ラゲージブランド「ace.」より、移動中も荷物の出し入れが簡単に行える特許取得構造「フレックスルーフTM」を搭載したビジネスソフトキャリー「フレックスルーフ2」を、全国の直営店・オンラインストアならびに全国の主要百貨店・専門店、で発売開始しました。'
text = '今後CAMPFIRE ENjiNEでは、企業におけるクラウドファンディング事業の展開を促進すべく、双方のクラウドファンディングサポートの知見やアセットを活かしてSaaS型クラウドファンディングプラットフォーム「CROWDFUNDING NETWORK Powered by ENjiNE」の共同提供を開始します。'

text = 'シャープは、社内のネットワークに侵入したマルウェアなどによる攻撃を遮断し、被害の拡大を抑制するセキュリティスイッチ<BP-X1PL01>を発売します。'
text = 'プラント大手の日揮や全日空、日本航空、日清食品など16社は温室効果ガスの排出量が少ない次世代航空燃料=SAFの国内での商用化と普及を目指す団体を立ち上げました。'
text = '加古川の仏壇・仏具店が「ファンタジー仏壇」、カスタマイズも 仏壇・仏具店「素心」が1月31日、プラスチック加工会社「匠工芸」とのコラボ仏壇「ファンタジー仏壇Prayer Spot~旅立ち~」の販売を始めた。'
text = '今後CAMPFIRE ENjiNEでは、「CROWDFUNDING NETWORK Powered by ENjiNE」の共同提供を開始します。'

酒菜と串揚げ、釜めしが自慢のレストラン「ごはん酒菜そのに」は、アジフライ専用「味和伊ソース」を開発し、オンラインショップで販売している。
サンディエゴ発-2022年3月1日-、エンタープライズ・アナリティクス向けのコネクテッド・マルチクラウド・データプラットフォーム「Teradata Vantage」を提供するテラデータは、「Everyday AI」のためのプラットフォーム「Dataiku」向けに、新たな分析統合コンポーネント「Teradata Plugins for Dataiku」の提供を開始したと発表しました。
SOICOがCFOに特化した採用支援サービス「CFOパッケージ」を開始: 時事ドットコム、SOICO株式会社は、未上場企業向けにCFO人材の採用支援からストックオプションの発行支援までワンストップでサポートする「CFOパッケージ」を開始いたします。
世界最大の時計企業であるスウォッチ グループ傘下のスイスブランド「オメガ」はクリアスペースと提携し、機能を停止した人工衛星などの宇宙ゴミを回収・除去する事業に参加する。
国立研究開発法人、産業技術総合研究所ゼロエミッション国際共同研究センター、有機系太陽電池研究チーム、村上、拓郎、研究チーム長、小野澤、伸子主任研究員は、日本精化株式会社と共同で、ペロブスカイト太陽電池に使われる有機ホール輸送材料について、ドーパントと呼ばれる添加剤を使用せず、高い光電変換効率が得られる新規材料を開発した。
2022年2月25日、リンクスインターナショナルは、ハイエンドモデルのポータブルゲーミングPC"AYA NEO NEXT Pro"の予約をAmazonなどで開始した。
NTTドコモ、個人投資家向け投資管理アプリ「マイトレード」を提供開始、- Yahoo!ニュース、NTTドコモは、個人投資家の投資管理や振り返りに特化したFinTechサービス「マイトレード」を月額550円で提供開始する。
2021年、プーマ・モータースポーツは、初めて女性ドライバーのためにレースウェアを製作しました。
「ビール業界のDX」クラフトビールスタートアップBest Beer Japan、シードラウンドで7,000万円を調達:時事ドットコム、Best Beer Japanはクラフトビール醸造所を管理するITツールと物流サービスを運営している。
この度、エムエスアイコンピュータージャパン株式会社は、Intel第10、11世代CPUに対応し、B560チップセットを搭載したMicro-ATXサイズのマザーボード「B560M PRO-E」を3月11日に発売いたします。
日刊スポーツPRESSとHOUSEI新聞業界のクラウド組版システム「共通化」を推進:時事ドットコム、日刊スポーツPRESS社とHOUSEIがクラウド組版システムを共同開発する。


keyword_list = model.verb_get(text) # キーワードの候補の抽出
keyword_list = model.v_o_get(text) # キーワードの候補の抽出
