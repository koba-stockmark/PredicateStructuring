from phase_extractor import PhaseExtractor
model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

text = '「北陸でんちゅうサーチ」を3月から提供開始すると発表した。	'
text = 'ダウンブランドの「カナダグース」が、自社のサプライチェーンからアップサイクルした余剰生地を使用したパッチワークパーカを2月19日に発売する。'

# もれなくプレゼント
text = 'BRUTALHACKは2月14日、恋愛シミュレーションゲーム「DOKI DOKI RAGNAROK」をSTEAMにて正式にリリースした。'
text = '日本\・欧州・アジア・豪州・米州で飲料事業を展開するサントリー食品インターナショナルは、このことを知らしめPETの分別・回収を促すためのコミュニケーションを強化するとともにPETの100%サステナブル化をグローバルで加速させる。'
text = 'アートのサブスクリプションサービス「Casie」を運営する株式会社Casieは、初心者でも自分にぴったりなアートがわかる新Webコンテンツ、アート診断を2022年3月1日に公開いたしました。'
text = '近鉄不動産は、玄関横に設置する宅配ボックスと防災用品収納スペースが一体となった専用ボックスを開発した。'
text = 'インクジェット立体物印刷装置の量産工程における実用化を加速:時事ドットコム、-、さまざまな立体物へフルカラーのダイレクト印刷が可能に、-セイコーエプソン株式会社は、さまざまな立体物の表面へダイレクトに印刷ができるインクジェット立体物印刷装置に関して、フルカラー印刷の実現とお客さまとの接点強化により、さまざまな量産工程における実用化を加速させます。'
text = '伊藤忠商事グループの株式会社Belongは、同社が提供する法人向け中古端末のレンタル・販売サービス「Belong One」にて、「Android Enterprise Device Reseller、認定取得」及び「Android Enterprise Essentials」の提供を記念し、法人のお客様により手軽かつセキュアな状態で、Android、端末をご導入頂けるよう、キャンペーンを開始いたします。'
text = '上質なサウナを簡単に導入可能、コンクリートの持つ高いデザイン性と耐久性を備えたサウナ用筐体「CUBERU」を発売、様々な温浴施設やキャンプ場、宿泊施設などへ高品質のサウナを導入可能に'

text = '中国塗料は、鋼材の加工時にさびを防ぐための塗料「ショッププライマー」で、塗る厚さを従来品より3割薄くできる新製品を開発した。'
#text = '同社は臨床試験のプロトコルや技術の設計・開発に患者中心の手法を取り入れるための「デザインによる患者中心主義の実現」プロセスを持つ。'

#text = 'パナソニック ソリューションテクノロジー株式会社は、企業の情報システム責任者を対象にしたセミナー「データの外部保管、成功のキーワードはオンプレミスクラウド「3つの安心・安全バックアップ法」大公開セミナー」を開催します。'

#text = 'ラーメンに熱い'
#text = 'ラーメンを食べることができる'
# なる尿酸
#text = '高尿酸血症・痛風に関する情報を発信する専門サイト「気になる尿酸値.jp」において、本日1月17日より疾患啓発動画「腎臓の機能低下に気をつけて!」の配信を開始しました。'
# 難しさや楽しい
#text = 'JAわかやまは、野菜の栽培体験を通じて野菜を育てる難しさや楽しさ、食の大切さを感じてもらおうと、和歌山市内の小学校と幼稚園などを対象に、袋の中で野菜を育てる「袋栽培」の体験学習を行っています。'

# ・横
#text = '詳しくはこちら発表日:2022年01月06日バッグや小物をデスクの下・横に置けるバッグワゴンを発売サンワサプライ株式会社は、バッグや小物をデスクの下・横に置けるバッグワゴン「FDM-BWG1BK」を発売しました。'
# 度
#text = 'この度、本プロジェクトの内、「革新的モノづくり技術開発プロジェクト2」の研究テーマの一つである「積層造形技術の高度化と先進デザインの融合による高機能部材の創製3」において、名古屋大学の小橋、眞教授、旭精機工業株式会社、株式会社フジミインコーポレーテッド及びあいち産業科学技術総合センターの研究グループは、3Dプリンターを用いて内部構造を有する超硬合金の金型の開発に成功しました。'
#text = 'JVCケンウッドは、ケンウッドブランドのドライブレコーダーとして、前後撮影対応2カメラドライブレコーダー「DRV-MR570」と、駐車録画対応電源ケーブル同梱の「DRV-MR575C」を1月下旬に、360度撮影できる2カメラモデル「DRV-C770R」を2月下旬に発売する。'
#text = '株式会社日立製作所と株式会社ソラコムは、このたび、両社における協業を加速し、IoTの活用により業務の効率化や価値創出などに取り組むさまざまな企業向けに、IoTサービスを強化します。'
text = '用語リンク大百科用語リンク東計電算は2月2日、クラウド型の決済情報管理システム「K-front」の「web明細照会サービス」をパッケージ化し、教育機関向けに4月より提供すると発表した。'

text = '太郎が気になる'
text = '酒菜と串揚げ、釜めしが自慢のレストラン「ごはん酒菜」は、アジフライ専用「味和伊ソース」を開発し、オンラインショップで販売している。'
#text = '引き続き各社は若年層や女性のドリンク剤未使用層の開拓に注力'
#text = 'イオンシネマは、新型コロナウイルス感染症の感染拡大をうけ、前後左右1席ずつ間隔を空けた座席の販売を17日より実施する。'
text = '株式会社ビームスが日本の魅力を発信するBEAMS JAPANは、福島県と共同で県の魅力を発信するプロジェクト「ふくしまものまっぷ」第32弾として、福島の多様な牛乳文化を味わえる牛乳と乳製品19種を2022年2月10日より販売します。'
text = '”おいしい” ”ワクワク” ”ハッピー”、をご届けするライフコーポレーションは、惣菜バイヤーが素材・製法にこだわった商品を発信していく取り組みである「バイヤーこだわりの一品」を毎月実施しております。'
# の思い

# イオンは2月10日より順次、「イオン」「イオンスタイル」約240店舗1)
text = 'イオンは2月10日より順次、「イオン」「イオンスタイル」約240店舗1)と発売します。'
# "爪
#text = '名古屋エアゾール株式会社のPR・販売会社である株式会社メイゾルは、”爪まで丁寧に育む”をコンセプトとした、ハンド&ネイルケアシリーズ「寧寧」のシリーズ第二弾として、爪やその周辺の特に、”荒れや乾燥”、が気になる部分を集中ケアするネイル用保湿パック「、寧寧、ネイルケアパック、」を、2022年3月1日より自社販売サイトにて販売開始いたします。'

#text = 'モノのインターネット)デバイスの正当性を担保し、なりすましや改ざんを防ぐためのサービスをIIJグローバルソリューションズが2021年11月30日に開始した。'

#text = '創業4年の同社はこれまで、中国のゴビパートナーズ、セコイア・キャピタル・チャイナ、ZhenFundなどの支援を受け、Eバイクや電動自転車のシェアリングサービスを行ってきた。'

text = '茨城県央地域で地域密着型の介護事業「介護グループ野ばら」を展開する株式会社マネジメントセンターは、水戸地区で唯一となる夜型デイサービス「デイサービス野ばら、しもいち館」を開業しました。'
text = '高校、大学や企業などにお金やビジネスに関する研修を提供している合同会社「FPal」では、「お金」についての知識をつけることで、前向きに生きていく学生や社会人になってもらおうと、ファイナンシャル・プランナー資格を持つ社員が独自に開発したゲーム形式のプログラム「Gトレ」を展開しています。'
text = '1日付で買い先行となった。'
text = '光ファイバー・システム企業として定評あるFibre Based Integrationsは、ライダーベースの車両検知ソリューションを南アフリカのケープタウンで開発し、街全体でスマート交通インフラを実現するために協力しています。'
text = 'eギフトプラットフォーム事業を展開する株式会社ギフティのマレーシアの現地法人であるGIFTEE MALAYSIA SDN. BHD.は、eギフト販売システム、「eGift System」を、LAZO DIAMOND JEWELLERY SDN. BHD.がマレーシアで展開する国内最大手のホワイトゴールド&ダイアモンドジュエリー専門チェーン「Lazo Diamond」に提供し、「Lazo Diamond」のeギフト販売ページにて、マレーシア全国の「Lazo Diamond」31店舗ならびに公式オンラインストアでご利用いただける個人を対象としたeギフトの販売を、2022年2月15日より開始しました。'
text = '東京都内および近郊のハイヤーの手配・運行・観光サービスを行う株式会社アウテックは、ご自宅やご希望の場所からドアツードアで観光しながら目的地へ移動ができる「観光ハイヤー」を利用した車いすでも楽しめる「冬のイルミネーション本命馬プラン」の販売をアウテックのホームページにて2021年1月7日より開始いたします。'
text = '藤沢市教育委員会はこのほど、市立小中学校に通う児童生徒に配布されている学習用タブレット端末を通じて教員にいじめなどの相談ができる「市子ども相談フォーム」を導入した。'
#text = 'LIXILは1月17日、脱炭素社会の実現に向けた「新・高性能窓」として、トリプルガラスを採用した「TW」と1日でトリプルガラスの高性能窓へリフォームができる「リプラス、高断熱汎用枠」を発表した。'
text = '国税庁の国税電子申告・納税システムにおいて、二次元バーコードをスマートフォン端末で読み取ることで、マイナンバーカード方式によるe-Tax送信ができるようになった。'

# 連体形主語　名詞＋の＋ある
text = 'トヨタ自動車は、「MIRAI」で採用実績のある樹脂製高圧水素タンクを活用した貯蔵モジュールを開発。'
#text = '彼に太郎が倒す'

#text = '株式会社Nabocul Cosmeticsは、2022年1月12日から14日まで東京ビッグサイトで開催された「2022年東京化粧品展覧会COSME TOKYO」に初出展し、新しいエイジングケア分野の最新テクノロジー化合物「OLANDU」を発表しました。'
#text = 'OKRや1on1、リアルタイムフィードバック、人事評価等などパフォーマンス・マネジメントを実現するオールインワンクラウド「HiManager」を提供する、ハイマネージャー株式会社は、経営者・人事担当者様の1on1への理解と導入支援を目的にした、「1on1パーフェクトガイド」を無料公開しました。'

#text = 'Coinbase国内におけるカスタマーサポート強化に向け、電話サポートサービスを開始:時事ドットコム カスタマーサポートサービスを強化し更なる顧客対応の向上を目指します世界最大級の暗号資産取引所「Coinbase」を運営するCoinbase株式会社は、顧客の利便性を高める為に、国内での電話サポートサービスを開始致しました。'

text = '”日本全国に料理と飲み物を1箱にしたフードボックス”をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'

text = 'ポップでさわやかなアフリカのビーチをイメージしたカラーを採用した、エチオピア発のエシカルなレザーブランドを製造・販売するアンドゥアメットは、アップサイクルコレクション「Shubu-Shubu」のトートバッグ「メイクマイデイ」から、設立10周年を記念したカラーの「アフリカンサーフライダー」を販売している。'

text = 'さまざまな生体情報をモニターできる新製品のシリーズを発表した。'

text = '同社は24日、業界最小・最軽量クラスを実現した3軸加速度センサー「NP-3550」を発売すると発表しており、これが材料視されているようだ。'

text = 'ファーウェイは、MWC Barcelona 2022のHuawei Full-Stack Data Center Forumで「Flash-to-Flash-to-Anything」のビジョンを提案し、あらゆるシナリオを加速させるためのオールフラッシュストレージの使用を推奨した。'

#text = '車載アフターサービスプラットフォームの実現を目指すビズピット株式会社は、自動車整備業者さまが日本の輸出車マーケットにおいて新規事業の基盤構築を行うための支援サービスを開始しました。'

text = 'NECネッツエスアイと住友理工、バイタルセンサーを活用したホテルサービスの実証実験を開始:時事ドットコム、~睡眠状態の可視化により快適な宿泊環境と良質な眠りを実現~NECネッツエスアイと住友理工は、ルームマネジメントシステムとバイタルセンサー「モニライフ」を組み合わせたホテル向けサービスの実証実験を本日よりホテル コレクティブにて開始します。'
text = '詳しくはこちら発表日:2022年02月03日ロボットのビル内移動を支援、オフィスの利便性向上とビル管理の省人化・省力化を実現「アーバンネット名古屋ネクスタビル」で「ロボット移動支援サービス」を提供三菱電機株式会社は、1月31日に竣工した「アーバンネット名古屋ネクスタビル」に、サービスロボットと連携するエレベーターと入退室管理システムを納入し、ロボットのビル内自律移動を支援する「ロボット移動支援サービス」を提供します。'

# 省略主語OK
text = '新社会システム総合研究所は、1996年12月6日に設立、創業以来26年以上、法人向けビジネスセミナーを年間約500回企画開催する情報提供サービスを主な事業としております。'
text = 'GMOインターネットグループのGMOフィナンシャルホールディングス株式会社の連結会社で、暗号資産取引業を営むGMOコイン株式会社は、GMOフィナンシャルホールディングスで培われた金融サービス提供のノウハウを活かし、安心して暗号資産のお取引ができる環境を提供しています。'
text = '西日本電信電話と京都大学は2月17日、京都大学プラットフォーム学卓越大学院プログラムにおいて連携し、社会に存在するさまざまなデータを活用して連携する次世代のプラットフォームに関する実証実験を行うための検証環境「Platform Initiative Lab」を共同で整備することを発表した。'
text = '東京ガスは2月24日、横浜市、三菱重工グループと共同で、ごみ焼却工場の排ガス中に含まれるCO2を分離・回収し、CO2を資源として利活用する技術の確立に向けた実証試験を行うと発表した。'
text = 'パナソニック株式会社、エコソリューションズ社は、「20歳のリフォーム」キャンペーンの一環として、同キャンペーンの期間中にパナソニックの住宅設備建材製品を採用し、リフォームするお客様を対象に優遇金利を適用するリフォーム専用ローン「20歳のリフォーム」ローンの提供を開始します。'
text = 'パナソニック株式会社は、マイクロ波を用いてパワーデバイス、、を制御する電力変換システムを世界で初めて開発し、半導体チップに集積化することに成功しました。'
text = 'Supership株式会社とKDDI株式会社は、共同運営するSMS送信サービス「KDDI Message Cast」を、新型コロナウイルス感染者への連絡手段として効果的に活用頂くため、お申込みいただいた即日からSMS送信のご利用が可能な全国の自治体および医療機関を対象とした特別プランの提供を開始しました。'
text = 'コールセンター・バックオフィスの構築・運営を行うセコムグループの株式会社TMJは、在宅コンタクトセンター化に向け設計・構築・マネジメントまでを一気通貫でサポートするサービスとして、「在宅オペレーション」の提供を開始しました。'

# NG
text = 'NECネッツエスアイと住友理工、バイタルセンサーを活用したホテルサービスの実証実験を開始:時事ドットコム、~睡眠状態の可視化により快適な宿泊環境と良質な眠りを実現~NECネッツエスアイと住友理工は、ルームマネジメントシステムとバイタルセンサー「モニライフ」を組み合わせたホテル向けサービスの実証実験を本日よりホテル コレクティブにて開始します。'
text = '詳しくはこちら発表日:2022年02月03日ロボットのビル内移動を支援、オフィスの利便性向上とビル管理の省人化・省力化を実現「アーバンネット名古屋ネクスタビル」で「ロボット移動支援サービス」を提供三菱電機株式会社は、1月31日に竣工した「アーバンネット名古屋ネクスタビル」に、サービスロボットと連携するエレベーターと入退室管理システムを納入し、ロボットのビル内自律移動を支援する「ロボット移動支援サービス」を提供します。'
text = '大建工業は、犬の歩行に配慮した”滑りにくさ”というペット視点の機能はもちろん、傷に強い、汚れにくい、変色しにくいといったユーザー視点の機能も併せ持つペット共生住宅用フローリング「ワンラブフロア」を、8月21日から全国発売いたします。'
text = '伊藤忠商事グループの株式会社Belongは、同社が提供する法人向け中古端末のレンタル・販売サービス「Belong One」にて、「Android Enterprise Device Reseller、認定取得」及び「Android Enterprise Essentials」の提供を記念し、法人のお客様により手軽かつセキュアな状態で、Android、端末をご導入頂けるよう、キャンペーンを開始いたします。'
text = '詳しくはこちらゆでたマカロニとあえるだけで、おつまみを作れるエスビー食品はマカロニとあえるだけでおつまみを作れる「OTSUMAMI Trattoria」を2月7日に発売する。'
text = 'これによりデータセンタおよびテレコムアプリケーション向けにパワー効率のよい超高帯域EO変換をサポートする。'
##text = '東北大学大学院工学研究科、東芝は、車載用等の小型モーター向けに、性能は現在と同等で、より継続的に生産を続けられ、さらに安価に生産できる可能性のある新しい等方性ボンド磁石を開発した。'
#text = 'KDDIは、2月26日?3月10日の間、自動運転車の移動中の位置情報に連動して変化するARコンテンツをスマートグラス上に表示する「自動運転車と未来のメガネで巡るメタバースの実証実験」を、東京臨海副都心・お台場エリアで実施する。'
#text = '日鉄エンジニアリング株式会社は、このたびクリーンテックベンチャー企業であるAltum Technologies Oyとライセンス契約を締結し、Deep tech IoT DX技術を活用した、カーボンニュートラルに資する新たなサービス型事業である、プラント設備のスマート洗浄サービスHiPEA EcoFUL2を開始いたします。'
#text = 'グローバル刃物メーカーの貝印株式会社は、「ねこ」をテーマとしたビューティーツールシリーズ「Nyarming」の新商品「ねこのシャンプーグローブ」「ねこの洗顔ブラシ」を、2022年3月8日より、貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売いたします。'

text = 'Coinbase国内におけるカスタマーサポート強化に向け、電話サポートサービスを開始:時事ドットコム カスタマーサポートサービスを強化し更なる顧客対応の向上を目指します世界最大級の暗号資産取引所「Coinbase」を運営するCoinbase株式会社は、顧客の利便性を高める為に、国内での電話サポートサービスを開始致しました。'
text = 'イマジニアは,氷上で行うウィンタースポーツ「カーリング」を手軽に楽しめるNintendo Switch向けソフト「みんなのカーリング」を,本日発売した。'
text = 'スマホで買える太陽光発電所「CHANGE」を提供する株式会社チェンジ・ザ・ワールドは、「グリーンワット」第2弾の販売を2022年2月9日より開始しましたので、お知らせいたします。'
text = '”日本全国に料理と飲み物を1箱にしたフードボックス”をお届けする「nonpi foodboxTM」を展開する株式会社ノンピは、2022年3月4日から「神田明神下みやび、桜満開お花見プラン」を販売開始いたします。'
text = 'FTTOソリューション:ファーウェイは、IPと光製品の技術的優位性を統合して、環境に優しく、簡素化されたキャンパスネットワークの構築に向けてFiber To The Officeソリューションの提供を開始した。'
#text = '太郎が走る'
text = 'パナソニック株式会社は、マイクロ波を用いてパワーデバイス、、を制御する電力変換システムを世界で初めて開発し、半導体チップに集積化することに成功しました。'

#text = 'LDBでは、「与信が難しいことが理由で、受けられる金融サービスが限定的になってしまっている」という中小企業の課題に対して、業界特有のデータやAIを活用した与信システムの開発に取り組み、2020年9月より一部を実用化、第一弾サービスとして建設業向けの金融サービスを提供開始しました。'
#text = 'スマートフォンやデジタルオーディオ端末等のアクセサリーブランド「Premium Style」の企画・製造・販売を手掛ける株式会社PGA 、は、このたび赤外線センサー内蔵でスマートフォンを近づけると自動ホールドする車載用ワイヤレス充電ホルダーを2022年02月10日より発売をいたします。'

# GMO 活かす
text = 'GMOインターネットグループのGMOフィナンシャルホールディングス株式会社の連結会社で、暗号資産取引業を営むGMOコイン株式会社は、GMOフィナンシャルホールディングスで培われた金融サービス提供のノウハウを活かし、安心して暗号資産のお取引ができる環境を提供しています。'
# 効率化
text = 'ADAPTER INC.は、食品業界の自主マーケティングリサーチ活動を効率化し、これまで社員個人が保有していたデータを社内にオープンにして、社内全体で情報共有を推進するサービス「FDC」のスマートフォンアプリ...'
# 総務省が　使う
text = '総務省が所管する地方公共団体情報システム機構は26日、マイナンバーカードを使って、コンビニで住民票など証明書を交付するサービスが各地で一時利用できなくなっていると明らかにした。'
#再生
text = 'DVDに変わる新しいメディアとして、スマートフォンや再生用ドライブを搭載しないPCでも再生が可能な動画ダウンロードカードパッケージを発売。'
# ひげを剃る
text = '株式会社リアライズは、1月9日?1月13日までの期間中、アニメ・漫画専門ECサイトであるAnimoで「ひげを剃る。そして女子高生を拾う。アクリルスタンド」の予約販売を開始いたします!'
# サイズを入力する
text = 'ハクロマーク製作所が運営するECサイト「オーダーのれんドットコム」は、サイズを入力するだけで簡単に注文ができるシステムを導入し、21年12月15日にリニューアルオープンした。'
# 五感を介する
text = '日本テレビと慶應義塾大学、「五感を伝送する体験型メディア技術の研究開発」をテーマに共同研究を開始:時事ドットコム デジタル世界と実世界を結ぶ革新的なインターフェース、及び新たなコミュニケーションや表現手法の具体化を目指す日本テレビ放送網株式会社と、慶應義塾大学大学院メディアデザイン研究科は、マテリアルインタラクションや感覚再現技術を活用した、五感を介して伝える新たなメディア表現やコンテンツの開発に関する共同研究を開始いたしました。'
#課題を整理する
text = 'PwC JapanグループのPwC税理士法人およびPwCアドバイザリー合同会社は本日、特定の税務リスクに対応した効率的かつ効果的な税務データの分析を実施し、実際の税務調査での指摘が懸念される取引や課題を整理して報告としてまとめるオリジナルサービス、「Tax Risk Data Analyser」を発表しました。'
# 購入する
text = 'ダイドードリンコ株式会社は、阪神電気鉄道株式会社の協力を受け、子育て世代の方々が紙おむつの持ち合わせを心配することなく外出できるよう、ベビー用、紙おむつ自動販売機を飲料とあわせて購入できる自動販売機、以下「自販機」)を、2月2日に阪神電車本線、大物駅に設置しました。'
# 優しい
text = '株式会社オージャストは、展示会や見本市で製作される展示ブースを、全て使い回しができる資材で制作することで、環境に優しく、かつ費用を抑えた、「Re:ブース」を2022年03月より提供いたします。'
# 方向で検討する
text = 'JR東日本が、夜間に勤務する駅員に常時装着する「ウエアラブルカメラ」を4月から配備する方向で検討していることが24日分かった。'
# カバーする
text = '一方、マスクたるみやマスクしわなどの肌悩みを抱える人は増えていることから、明色化粧品は、肌悩みをピンポイントでカバーしながら、シワ改善と美白ケアができるコンシーラーを開発しました。'
# 予測する
text = '航空機が雷を受けやすいエリアを予測し飛行ルートの設定などに役立てようと、宇宙航空研究開発機構が福井県坂井市の福井空港に気象レーダーを設置し研究に着手する。'
# 展開する
text = ':時事ドットコム、~ホテル内の空いているスペースを活かしてパーソナルトレーナーによるトレーニングが受けられるフィットネスジムの事業を展開~株式会社岡京は、自社ブランドである24時間完全個室のパーソナルジム「FOUND」とビジネスホテルを運営する株式会社レガロホテルシステムと提携し、コロナ禍のその先を見込んだ施策を試みる。'
# 標準機能
text = '法人向けソフトウェアの開発、販売を行うサイバーソリューションズ株式会社は、企業がスムーズなテレワーク導入を支援するため、自社が提供するクラウドメールサービス「CYBERMAIL、」と統合型セキュア・メールサーバシステム「CyberMail」にコンプライアンス対応ビジネスチャット「CYBERCHAT」オプション機能を標準機能として、2022年4月1日より提供開始することをお知らせします。'
# ファン
##text = 'クリエーターの成功をテクノロジーで支援するZAIKO株式会社、は、クリエイターとファンが直接つながれるプラットフォームをコンセプトに、デジタルイベント、動画配信、データアナリティクス、NFTなどの幅広い領域でプロダクト/サービスを多角的に展開しております。'
# データを活用する
##text = '社会に存在するさまざまなデータを活用して連携するプラットフォームに関する実証実験を行うための検証環境「Platform Initiative Lab」を共同で整備することを発表した。'
# 、
#text = 'シャッターチャンスを自動で判断して撮影するキヤノンの新コンセプトカメラ「PowerShot PICK」の一般販売が2021年11月末に開始されました。'

#text = 'ジャガイモの皮を使用してつくったフレーバーソルトが登場。'
# かける
#text = 'ウッドワンは、1990年からニュージーランドに自社森林を保有し、苗木を植え、約30年かけて育て、無垢の木の内装ドア、床材、階段材、システムキッチンなどの住宅用内装建材、設備を製造販売しています。'
#主語
#text = '楽天グループは25日、アニメやスポーツの動画や画像を「非代替性トークン」と呼ばれるデジタル資産に加工して販売するサービスを始めた。'

#text = '太郎は本を読んで終わった。'
# かけて
#text = 'パナソニック システムコミュニケーションズカンパニー ヨーロッパは、スペインのバルセロナで2015年3月2日〜5日にかけて開催された展示会「モバイル・ワールド・コングレス2015」において、欧州でMVNOサービスを立ち上げたことを発表しました。'
# 上
#text = '1日付で、関西みらい銀行、みなと銀行などの持株会社・関西みらいフィナンシャルグループの法人顧客向けにクラウド型健康管理サービス「first call」の提供を開始と発表して好感された上、3日はSMBC日興証券が投資判断を中立の「2」から強気の「1」に引き上げたと伝えられ、買い先行となった。'

#text = '日本から生み出される様々なデジタルアートを世界に向けて発信するサービスを展開してゆきます。'
#text = '北海道の南富良野町で冬の新たな観光の呼び物にしようと、湖の氷を円く切り抜き人を乗せて回転させる「アイスカルーセル」の実証実験が行われました。'

#text = 'ノックオンザドア株式会社、一般社団法人、mina family、ミツフジ株式会社、豊島株式会社の3社1団体は、てんかん患児のバイタルデータを取得し、アプリ内のデータと合わせて分析することで、患児やその家族の心理的・身体的負担の軽減に繋げていくことを目指す小児てんかん患児向けデバイス開発の共同プロジェクトをスタートいたします。'

#text = 'ノックオンザドア株式会社、一般社団法人、mina family、ミツフジ株式会社、豊島株式会社の3社1団体は、てんかん患児のバイタルデータを取得し、アプリ内のデータと合わせて分析することで、患児やその家族の心理的・身体的負担の軽減に繋げていくことを目指す小児てんかん患児向けデバイス開発の共同プロジェクトをスタートいたします。'

text = '新社会システム総合研究所は、1996年12月6日に設立、創業以来26年以上、法人向けビジネスセミナーを年間約500回企画開催する情報提供サービスを主な事業としております。'
# 主語
#text = 'HDMI出力対応のデジタルカメラをUSB接続Webカメラとして使えるようにするHDMIキャプチャアダプタ「UCP-HD31」がミヨシから発売された。'
#text = '株式会社オトナルは、ポッドキャスト間のリスナー送客を定量的に可視化するトラッキングサービスの提供を開始しました。'
#text = '<英語スピーキング力測定の習慣化>「PROGOS」アプリ提供開始無料で受けられるAIビジネス英語スピーキングテスト:時事ドットコム、国際基準CEFRに基づくレベル診断で効果的な英会話学習を、世界39、の国と地域でも同時リリース。人にまつわるデータを活用し、グローバルに活躍する人々を生み出す株式会社レアジョブの法人向け事業子会社、株式会社プロゴスはAIビジネス英語スピーキングテスト「PROGOS」のモバイルアプリを提供開始いたしました。'

#text = '「カーリング」を手軽に楽しめるNintendo Switch向けソフト「みんなのカーリング」を,本日発売した。'
#text = '東京ガスは2月24日、横浜市、三菱重工グループと共同で、ごみ焼却工場の排ガス中に含まれるCO2を分離・回収し、CO2を資源として利活用する技術の確立に向けた実証試験を行うと発表した。'

text = 'ハリウッド株式会社は、3月5日=珊瑚の日に併せて、珊瑚を死滅させる原因となっているオキシベンゾン、オクチノキサート、ナノ粒子酸化チタン、ナノ酸化亜鉛の4つを使用しない、珊瑚にやさしいコーラルフレンドリーUVスキンケアの開発に成功、今後のハリウッド化粧品の全商品に展開していく計画を発表しました。'
#text = 'パナソニック株式会社、エコソリューションズ社は、発光部をひとつにまとめた集積型LEDを搭載し、多重影のない自然で、ムラのない美しい光を実現したLEDダウンライト ワンコアタイプ高出力型にコンパクトサイズを2014年1月6日より順次発売、合計98品番に品種拡充していきます。'
#text = 'パナソニック株式会社、システムソリュションズ社は、工場見える化システムに新たな機能として、ディスクレコーダによる録画映像を用いて解析をおこなう「動線描画ソフト」を発売します。'
#text = '詳しくはこちら発表日:2022年03月11日「IoT、ルータ統合管理システム」サービス提供開始NEC、マグナスコミュニケーションズは、IoT/M2M市場に向けに、多地点に設置・運用中のLTE対応ルータの統合管理を可能とする「IoT、ルータ統合管理システム」のサービス提供を開始いたします。'
#text = '森永乳業では、ヘルスケア事業として、「全世代の健康で幸せな毎日の実現へ」をテーマに、2021、年、1、月より健康セミナー事業「健幸サポート栄養士」を本格的に開始、健康経営を推進される企業や自治体に向けて健康セミナーを開催しています。'

text = 'パナソニック株式会社、エコソリューションズ社、ハウジングシステム事業部傘下のパナソニックES、テクノストラクチャー株式会社は、独自の耐震住宅工法「テクノストラクチャー」のZEH、対応住宅、「FORCASA Zero」を全国のテクノストラクチャー、工法採用ビルダーを通じて、2017年4月24日より発売します。'
# 通じて＋発売する　を作る　ただし、全国のテクノストラクチャー工法採用ビルダー　のときだけで　他のときは　発売する　にする
text = 'パナソニック株式会社 エコソリューションズ社 ハウジングシステム事業部傘下のパナソニックES テクノストラクチャー株式会社は、独自の耐震住宅工法「テクノストラクチャー」のZEH （ネット・ゼロ・ エネルギー・ハウス）対応住宅、「FORCASA Zero（フォルカーサ ゼロ）」を全国のテクノストラクチャー 工法採用ビルダーを通じて、2017年4月24日より発売します。'
# 一緒に
text = '福岡県大牟田市と熊本県荒尾市で配食サービスを展開するキュリアスは、新型コロナウイルスの影響で自宅待機になった人に、生活必需品などを弁当と一緒に届ける事業「配達冷凍弁当」を4日から始める。'
# とともに
text = 'サムスンは3日、CES 2022にあわせて最新のミニLEDテレビ「Neo QLED」やディスプレイ「MICRO LED」とともに、テレビ上でNFTの売買ができる「NFT Platform」を発表した。'
#text = '株式会社ファイターズ スポーツ&エンターテイメントと、株式会社ヤッホーブルーイングは、新球場ES CON FIELD HOKKAIDOのセンターバックスクリーンに”世界初のフィールドが一望できるクラフトビール醸造レストラン”をオープンすることを決定しました。'

#text = '太郎と花子が公園と動物園を歩く'
text = '太郎は花子とゲームをしたことを発表した'
text = '3月9日、AIベンチャーのグリッドは、仮想空間上に現実世界の企業活動を再現する「デジタルツイン」を活用して、製造業やサプライチェーンの経済コストや二酸化炭素排出量をシミュレーションする「ReNom GX」を開発したことを発表した。'


text = '株式会社Lentranceは、同社の学習用ICTプラットフォーム「Lentrance」と連動して動作する学習履歴データ分析基盤、「Lentrance Analytics」の商用提供開始を発表いたします。'

text = '太郎は遊ぶ'
text = '台湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'

# all = 【「toroa」(を) - 楽しめる】 subj = 【「極濃いちごとろ生ガトーショコラ」】 がおかしい
text = '「toroa」にて、いちごを楽しめる「極濃いちごとろ生ガトーショコラ」「極濃いちごとろ生チーズケーキ」の一般発売を、1月18日に開始する。'

text = '「LINE Pay」を運営するLINE Pay、LINEの暗号資産事業やブロックチェーン関連事業を展開するLVC、LVC傘下でシンガポール企業のLINE TECH PLUSの3社は2月3日、LINEの暗号資産「LINK」をLINE Payで支払える「LINK支払い」を試験的に開始すると発表した。'

text = 'タイトーのアーケードゲーム筐体「EGRETII」をモチーフにした小型ゲーム機が登場、「EGRETII mini」が発売された。'
text = '鈴研.陶業は、新規事業で美濃焼タイルを素材にしたジュエリーシリーズ「Re.Juile」を立ち上げた。'
text = '「おいしく栄養を摂取して楽しくからだづくりができる時代へ」をミッションに掲げるEVO FOOD/エボフードは、ダイエット中やからだづくりにおいて罪悪感なくおいしく食べられる新たな食文化を志し2021年8月に販売をスタートした栄養生パスタにと組み合わせる完全無添加ソースとして新たに3種類の提供を開始したことをお知らせします。'

text = 'ワイヤレスイヤホンは音楽リスニングだけでなく、リモート会議のコミュニケーションにも役立つアイテムとして注目されている。'
text = 'ザ ストリングス、表参道では、春の期間限定アフタヌーンティーセット「NYアフタヌーンティー?ストロベリーピスタチオハニー?」を、2022年3月10日から4月26日までの期間限定で提供する。'
text = '女性に寄り添う化粧品・健康食品の開発・販売を行うCoCoRo株式会社は、スキンケア商品、北海道産サラブレッド馬生プラセンタ原液「プラセンタダイレクト」を2022年2月より公式サイト「ここはぴ公式オンラインショップ」にて一般発売を開始いたしました。'

text = ')は、Amphenolの産業製品部門であるAmphenol Industrial Products Groupの主に産業用途向けコンパクト大電流・高圧コネクタなどの国内販売を開始いたします。'
text = ':時事ドットコム テクノロジーによる痛み・不安の軽減を理念とする、株式会社xCuraは、治療体験をエンターテイメント体験に変え、快適な治療体験を提供するXR Therapy"の試験運用を、広島で開始したところお知らせ致します。'

text = '?、ハーバード大学などがAIを開発、株式会社PR TIMES'
text = 'UX重視の農業事業、アプリ開発事業を手掛ける、Agri Creationは、家庭菜園特化型SNS「MYplant」のアプリ開発を、2022年4月より開始します。'

#text = '太郎が花子と学校の調査などをする。'
text = '東北大学と東芝はこのほど、ネオジムボンド磁石と同等の磁力を有するサマリウム鉄系ボンド磁石を、希土類であるサマリウムの含有量を約半分に削減して開発したと発表した。'
text = 'そんななか北欧・フィンランド発の「WOLT」は、食品小売業との提携を加速させるほか、ダークストアを活用した独自の食品配達サービスにも着手するなど、新たな動きを見せている。'

# 省略主語　ハイダメージ
text = '世界各国のアーティストに支持されている人気のマーカーペンや画材、日常を豊かにする生活雑貨を提供している「Ohuhu」では、「Ohuhuアクリル絵の具、24色」2,699を新発売した。'

#text = 'これによりアイティーエムは、オープンソースや内部ホストの脆弱性管理サービスの提供範囲を拡大し、セキュリティ運用をアウトソースする企業もyamoryを利用可能になります。'
#text = 'グローバル刃物メーカーの貝印株式会社は、「ねこ」をテーマとしたビューティーツールシリーズ「Nyarming」の新商品「ねこのシャンプーグローブ」「ねこの洗顔ブラシ」を、2022年3月8日より、貝印公式オンラインストアをはじめ、全国のドラッグストア、ホームセンター、大手量販店などにて発売いたします。'

text = '金沢大発ベンチャー「Kanazawa Diamond」が、独自技術で人工的に製造した黒いダイヤモンドの販売を2022年秋ごろに始める計画だ。'
text = '台湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'
text = '「G3223Q」、デル・テクノロジーズは、HDMI 2.1を搭載した32型の4Kゲーミングモニター「G3223Q」と、最大165Hzの可変リフレッシュレートに対応した31.5型のQHDゲーミングモニター「G3223D」を、3月11日に発売した。'

text = '「M・A・C」は3月25日、イスラムの夜空に浮かぶ三日月と星からインスパイアされた"マグニフィセント ムーン コレクション"を発売する。'

#text = 'ホテル内の空いているスペースを活かしてパーソナルトレーナーによるトレーニングが受けられるフィットネスジム。'

text = '大手スーパーのベイシアは、小型店舗の「ベイシアマート」を除く全店舗で「アセロラ真鯛」の試験販売を始めた。'
#text = 'ラーメンが嫌いな太郎。'

text = '日本テレビと慶應義塾大学、「五感を伝送する体験型メディア技術の研究開発」をテーマに共同研究を開始:時事ドットコム デジタル世界と実世界を結ぶ革新的なインターフェース、及び新たなコミュニケーションや表現手法の具体化を目指す日本テレビ放送網株式会社と、慶應義塾大学大学院メディアデザイン研究科は、マテリアルインタラクションや感覚再現技術を活用した、五感を介して伝える新たなメディア表現やコンテンツの開発に関する共同研究を中止いたしました。'

text = 'Cloudpickは人々の買い物体験を変革することをミッションに、AI技術とビッグデータを駆使したソフトウェア、ハードウェアを含めた無人・省人店舗におけるソリューションの開発と提供を行っています。'
#text = 'ビジネス現場のコミュニケーションツール「LINE WORKS」を提供するワークスモバイルジャパン株式会社は、お使いのLINE WORKS IDのQRコードが印刷されたシール100枚を、先着500名様に無料でお届けする「"あなた専用のQRコード"、シールでお届けキャンペーン」を開始することをお知らせいたします。'
#text = 'NECネッツエスアイと住友理工、バイタルセンサーを活用したホテルサービスの実証実験を開始:時事ドットコム、~睡眠状態の可視化により快適な宿泊環境と良質な眠りを実現~NECネッツエスアイと住友理工は、ルームマネジメントシステムとバイタルセンサー「モニライフ」を組み合わせたホテル向けサービスの実証実験を本日よりホテル コレクティブにて開始します。'

#text = '株式会社Lentranceは、同社の学習用ICTプラットフォーム「Lentrance」と連動して動作する学習履歴データ分析基盤、「Lentrance Analytics」の商用提供開始を発表いたします。'
#text = '米アップルは次世代通信規格「5G」に対応した廉価版のiPhoneと改良版iPadを、3月8日をめどに発表する計画。'
#text = '創業4年の同社はこれまで、中国のゴビパートナーズ、セコイア・キャピタル・チャイナ、ZhenFundなどの支援を受け、Eバイクや電動自転車のシェアリングサービスを行ってきた。'

text = 'キャンピングカーの製造や販売を行うALFLEXは2月18日、アドセットシリーズの頂点に立つハイエンドモデル「MASTERS LINE」が2月に誕生したと発表。'

text = '株式会社Mr. CHEESECAKEは、2022年1月30日より、華やかな箔を使用したオリジナルデザインのギフトラッピングとギフトバッグの販売を開始します。'

text = '全国人民代表大会代表で中国航天科工集団第二研究院党委書記の馬傑氏が、2022年全国両会の会期中に明らかにしたところによると、世界の高精度・高時空分解能大気リモートセンシングデータの取得を実現するため、中国航天科工集団は世界掩蔽気象探査衛星ネットワークの構築を計画している。'
text = 'そんななか北欧・フィンランド発の「WOLT」は、食品小売業との提携を加速させるほか、ダークストアを活用した独自の食品配達サービスにも着手するなど、新たな動きを見せている。'
text = '株式会社日立製作所と株式会社ソラコムは、このたび、両社における協業を加速し、IoTの活用により業務の効率化や価値創出などに取り組むさまざまな企業向けに、IoTサービスを強化します。'
text = '富士通は2月21日、総務省および経済産業省のガイドラインに基づいてAIシステムの倫理上の影響を評価する方式を開発したことを発表した。'

text = '楽しみながらプログラミングを学習できる教材の開発競争が活発になっている。'
text = 'ARK社は容易に導入できる小型/分散型の閉鎖循環式陸上養殖システムを開発するベンチャーです。'
text = 'いすゞ自動車株式会社、西日本鉄道株式会社、三菱商事株式会社は、いすゞ製大型バスでの自動運転の共同実証実験を実施することに合意した。'
text = 'JR西日本は16日、岡山と山陰地方を結ぶ特急「やくも」用に、新型車両「273系」を新開発すると発表した。'
text = 'PVSQ-Mは、太陽光発電所の技術評価・リスク評価や太陽光パネルの性能・信頼性評価などの専門性の高い評価、調査、技術コンサルティング業務を行っている。'

text = '台湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'
text = 'パナソニック株式会社は、2016年10月5日より、放送中の番組や録画した番組を、ビエラやディーガからスマートフォンやタブレットに転送し、外出先や家の好きな部屋で視聴できるリモート視聴用アプリ「Panasonic Media Access」をより便利により使いやすく、バージョンアップしました。'

#text = '株式会社Nabocul Cosmeticsは、2022年1月12日から14日まで東京ビッグサイトで開催された「2022年東京化粧品展覧会COSME TOKYO」に初出展し、新しいエイジングケア分野の最新テクノロジー化合物「OLANDU」を発表しました。'

text = '医療法人社団、やまびこ、本院、新横浜整形外科リウマチ科は、患者の診察およびリハビリテーション後の会計・処方箋発行待ちによる過密対策のため、SMBCグループ、株式会社プラスメディが開発・運営する患者向けスマホアプリ「MyHospital」を令和4年2月15日から導入しサービスを開始いたします。'
text = '東日本電信電話株式会社北海道事業部は、労働力不足の解消並びにコロナ禍における非接触ニーズへの対応のため、入店から商品選択、決済までをスマートフォン等で完結する「スマートストア」店舗を2021年12月20日社内のNTT大通14丁目ビルに開設しました。'

text = 'コンセプトのもと、肌と髪のオールインワン・ケアを叶える基礎化粧品「Collajenne」のサブスクリプションプランを開始しました。'
text = '上空シェアリングサービス「sora:share」を運営するトルビズオンは3月8日、福岡県宗像市と共同でイオン九州の協力のもと、ドローンを用いた物流配送実証実験を同6日に実施したと発表した。'

text = 'ツールをより使いやすく、バージョンアップする'
text = 'スプリングバレーブルワリーは1月28日、日本産ホップのおいしさを楽しめる限定ビール「JAPAN HOP~ペールエールタイプ~」をスプリングバレーブルワリー京都で数量限定で提供を開始する。'
text = 'これまでにも、タップルでは安心・安全の取り組みとして、Media Data Tech Studioの協力のもと「18歳未満の可能性があるユーザーを自動検知するシステム」及び「プロフィール画像において掲載基準に満たない画像を自動検知するシステム」など、機械学習技術を用いた不正利用者の早期検知システムを導入しております。'

text = 'オークネットは、サステナビリティポリシーとして「価値あるモノを、地球規模で循環させる~Circulation Engine.」を制定し、あらゆる「価値あるモノ」を「必要な人のもと」へ循環させる"循環型流通"の構築に取り組んでおります。'

text = 'メタバース「RISA」を提供する株式会社OPSIONは、2022年3月10日、セキュリティ強化の為、情報セキュリティマネジメントシステムを取得したことをお知らせいたします。'

# 28
text = 'パナソニック株式会社は、2016年10月5日より、放送中の番組や録画した番組を、ビエラやディーガからスマートフォンやタブレットに転送し、外出先や家の好きな部屋で視聴できるリモート視聴用アプリ「Panasonic Media Access」をより便利により使いやすく、バージョンアップしました。'

#text = '鹿児島県庁では、庁内情報基盤である行政情報ネットワークの再構築と併せて、職員の在宅勤務実施に向けたコミュニケーションツールの導入を検討していました。'

#text = '自宅でビールを原料から醸造できる新たな家電が登場した。'

# から
#text = 'テマセク財団は、Covid-19から住民を守るための第6回配布運動で、シンガポールのすべての住民に再利用可能なマスクを提供する。'
#text = '東京大学大学院新領域創成科学研究科の門城拓、博士課程学生、永澤慧、特任研究員、鈴木穣、教授、鎌谷洋一郎、教授、東京大学医科学研究所の小井土大、特任助教による研究グループは、組織切片画像から空間的な遺伝子発現量をコンピューター上で予測する、深層学習を応用した新規手法DeepSpaCEを開発しました。'
#text = 'サントリー食品インターナショナルは、牛乳で割ることでフルーツオレが作れる栄養機能食品「ボス カフェベース、贅沢フルーツオレ」を8日発売。'
#text = 'その会社は豚骨スープの飲み残しをラーメン店から集めて、石油に頼らないバイオディーゼル燃料を製造し、運送業務を行っているという。'
#text = 'ホビー通販大手の「あみあみ」は、「Dドールズフロントライン、Gr G36 1/7スケール、完成品フィギュア」を現在発売中です。'
#text = 'XTransferは、ドイツ銀行の国際支店網を活用することで、2022年から米国、欧州、英国、シンガポールと日本の中小企業向けに、現地での送金受取サービスの提供を開始する。'
#text = '大東建託グループのインヴァランスが、いえらぶBB・Web申込みを利用開始:時事ドットコム、不動産業者間プラットフォームの活用で実務のオンライン化・DXを促進!不動産テックに特化したバーティカルSaaSを提供する株式会社いえらぶGROUPは、大東建託グループの株式会社インヴァランスに、リーシング業務を一元化する「いえらぶBB」の提供を開始しました。'
#text = 'パシフィックネットは、IT機器の導入・運用管理・クラウド・セキュリティを「サブスクリプション」モデルで提供し、適正処分に至るまでの包括的な企業の情報システムを支援するITサービスのオンリーワン企業である。'
#text = 'プジョーは、最高出力680psのハイブリッド・パワートレインを搭載した新型ハイパーカー「9X8」で、6月のル・マン24時間レースに復帰する予定だ。'
#text = '動画を起点として1,700社以上の企業にコンサルティング事業を展開する株式会社LOCUSは、高額で効果の見えにくかったTVCMを、手軽に実施且つ効果測定を可能にするサービス「FAST CM」をリリースしましたのでお知らせいたします。'

#　ちょっと別
text = 'ハリウッド株式会社は、3月5日=珊瑚の日に併せて、珊瑚を死滅させる原因となっているオキシベンゾン、オクチノキサート、ナノ粒子酸化チタン、ナノ酸化亜鉛の4つを使用しない、珊瑚にやさしいコーラルフレンドリーUVスキンケアの開発に成功、今後のハリウッド化粧品の全商品に展開していく計画を発表しました。'
text = 'Macお宝鑑定団Blogによると、Appleは今春にiPhone SEとiPad Airを発売する可能性があるという。'
# 発売する可能性がある にまとめて　-> 発売する　+ 可能性がある

# 決済アプリである
text = 'CNBCレポートによると、多目的メッセージングおよびモバイル決済アプリであるWeChat Payは、デジタル人民元決済のサポートを開始するとのこと。'

# 発売中だ
text = 'オンラインショップ「KALE FARM」から、無農薬・無化学肥料で育てたケールのコールドプレスジュースと、イギリス発のオーガニックオーツミルクを組み合わせた新作ケールジュース「ケールオーツミルク」が、1月21日より発売中だ。'

# 工事不要で　利用できる
text = '詳しくはこちらNTTドコモは工事不要で利用できる固定電話サービスを3月下旬から提供するNTTドコモは4日、工事不要で利用できる固定電話サービスを3月下旬から始めると発表した。'

#text = 'プラス株式会社は、テープの長さを8mから10mに25%増量したテープのり「ノリノビーンズ」を2022年2月22日にリニューアル新発売します。'
#text = 'タビナカのレジャー予約プラットフォームのKlookは、人気のレジャーチケットをパッケージ化した「レジャパケ」を設定し、2022年1月24日~2月末まで25%割引で販売する。'
text = 'なお、NECとKNIは、AI技術などICTを活用して医療の質の向上と業務の効率化を目指す「デジタルホスピタル」の実現に向け2017年より共創を開始しており、今回の取り組みはその一環として実施されたものだ。'
text = '今回の取り組みはその一環として実施するものでしょうか？'

text = 'パシフィックネットは、IT機器の導入・運用管理・クラウド・セキュリティを「サブスクリプション」モデルで提供し、適正処分に至るまでの包括的な企業の情報システムを支援するITサービスのオンリーワン企業である。'
# 開発中する
text = '詳細画像はこちらメガパワーのEVフラッグシップ、「秘伝のタレ」搭載レクサスは、LFAの精神的後継モデルとなる電動スーパーカーを、2030年までの発売を目指し開発中だ。'
# Maiｎ
text = 'XTransferは、ドイツ銀行の国際支店網を活用することで、2022年から米国、欧州、英国、シンガポールと日本の中小企業向けに、現地での送金受取サービスの提供を開始する。'

text = 'JSPは発泡プラスチック製品の大手である。'

text = 'NPO法人ラ・レーチェ・リーグ日本は、母乳が楽になる、軌道に乗せやすくなる情報をシンプル&コンパクトに提供する「母乳育児かんたんスタートガイド」を2022年2月16日より発売開始しました。'

#text = 'パナソニック サイクルテック株式会社は、2022年1月から2年間の予定で、集合住宅における居住者向けIoT電動アシスト自転車シェアリングサービスの実証実験を実施します。'

#text = '台湾ASUSは1月6日、薄型軽量で有機ELディスプレイを採用するプレミアムなビジネス向けノートPC「Zenbook OLED」シリーズの製品に、第12世代Intel Coreプロセッサや新しいAMD Ryzen 5000シリーズの搭載で刷新した新モデルを発表した。'
# advcl からの項の生成
#text = '金沢大発ベンチャー「Kanazawa Diamond」が、独自技術で人工的に製造した黒いダイヤモンドの販売を2022年秋ごろに始める計画だ。'
# case から　のカーリング」
##text = 'イマジニアは,氷上で行うウィンタースポーツ「カーリング」を手軽に楽しめるNintendo Switch向けソフト「みんなのカーリング」を,本日発売した。'
#text = '株式会社Nabocul Cosmeticsは、2022年1月12日から14日まで東京ビッグサイトで開催された「2022年東京化粧品展覧会COSME TOKYO」に初出展し、新しいエイジングケア分野の最新テクノロジー化合物「OLANDU」を発表しました。'


#text = 'アルマビアンカは、「日常でも使用できる」をコンセプトにしたオリジナルグッズを展開する通販サイト「AMNIBUS」にて、TVアニメ「東京リベンジャーズ」の商品の受注を2月8日より開始した。'

# ノバルティス ファーマ と
#text = 'セガ エックスディーは、2021年、11、月、25、日にノバルティス ファーマと共同開発した社員教育向けカードゲーム「、emotcha」を用いて、香川県高松市立協和中学校の教職員向けにコミュニケーション力養成を目的としたワークショップを実施した。'
#text = '*、西日本鉄道株式会社は、いすゞ自動車株式会社、三菱商事株式会社、福岡国際空港株式会社と共同で、福岡空港内において大型自動運転バスを用いた自動運転の実証実験を2022年3月8日より実施いたします。'
#text = '東京ガスは2月24日、横浜市、三菱重工グループと共同で、ごみ焼却工場の排ガス中に含まれるCO2を分離・回収し、CO2を資源として利活用する技術の確立に向けた実証試験を行うと発表した。'

#三菱ロジスネクスト と 着手する
text = '荷主三菱重工業は20日、三菱重工グループの三菱ロジスネクストと共同で、三菱重工業が研究開発を進める「SynX」のコア技術を適用して物流を知能化・自動化するプロジェクトに着手したと発表した。'
# ないにもかかわら
text = '東京大学、Human & Environment Informatics Labの研究チームは、物理的なファンによる風がないにもかかわらず、風の感覚を耳で得られるヘッドフォン型ウェアラブルデバイスを開発した。'
# 実験をNTT東日本が　行うにあたり
text = '今回、各種システムを運用するために必要不可欠となる通信領域を高品質で安定提供できるよう、NTTグループのアクセスネットワークに関する研究開発機関であるNTT AS研と共同で、畜産現場でプラチナバンドのIoT向けWi-Fi「IEEE802.11ah」の活用有無を検証する実証実験をNTT東日本が行うにあたり、ネットワークを介して活用するソリューションサービスとして、AIとビッグデータを活用し勘と経験に頼らない養豚を実現するAI家畜管理サービス「PIGI」を提供致しました。'
# 計画段階からの設計・施工 のと同様まとめる
text = '山神運輸工業は、鋼材や機械等の重量物輸送を中心に、海上コンテナ輸送等多様な輸送を行う一般貨物輸送事業と、機械据付・メンテナンス等を実施し、計画段階からの設計・施工といった一貫対応も行うエンジニアリング事業を2大事業として展開している。'

######
# Mainがない
text = 'JAOSは「Experience a New Adventure.」をスローガンに掲げ、1985年の創業以来、一人でも多くのお客様に新たな冒険を体験していただけるよう4WD&SUV用パーツの開発や提供を続けています。'
#text = 'JAOSは「Experience a New Adventure.」をスローガンに掲げます。'
# 正味　ゼロとなる
#text = 'パナソニック株式会社、エコソリューションズ社は、年間の一次エネルギー消費量が正味で概ねゼロとなるネット・ゼロ・エネルギー・ハウスに、安心・健康に配慮した「ウェルネス」の要素を加えた新しいゼロエネルギーの住まい「スマートウェルネス住宅」3タイプを、2015年7月1日よりパナソニックビルダーズグループ加盟店にて販売します。'

text = '株式会社ジェイテクトは、建設機械・農業機械車両のライフサイクルコストにつながるリマニュファクチャリングへの取り組みを進め、ジェイテクトが持つ寿命予測技術や軸受再組付けが可能となる保持器の開発など、軸受再使用技術を確立しました。'
text = 'ロッキードはエアロジェットの推進システムを内製化する予定だったが、合併撤回により米国の防衛に不可欠な極超音速兵器の開発が難航する。'

# となる
text = '株式会社ジェイテクトは、建設機械・農業機械車両のライフサイクルコストにつながるリマニュファクチャリングへの取り組みを進め、ジェイテクトが持つ寿命予測技術や軸受再組付けが可能となる保持器の開発など、軸受再使用技術を確立しました。'
#text = 'サプリメントの販売・卸を手掛ける日本ファーマは2月21日、男性の肌の悩みにアプローチするスキンケアブランドを立ち上げ、シリーズ第1弾となる化粧水の先行販売をクラウドファンディングで開始した。'
##text = '神戸大学大学院理学研究科の津田明彦准教授らの研究グループは、AGC株式会社と協力して、光で酸化したクロロホルムを使って、スポンジ、クッション、断熱材、繊維などに使用されるポリウレタンやその原料となるイソシアネート、および尿素誘導体の合成に成功しました。'
text = '繊維などに使用されるポリウレタンやその原料となるイソシアネート、および尿素誘導体の合成に成功しました。'
#text = 'コダックは、ドイツのWKSグループのエッセン市にある拠点に世界1号機となる「KODAK MAGNUS Q4800プレートセッター」の設置を完了したことを発表した。'
#text = '人気モデル・五明祐子さんとコラボレーションした、特別な日をさらに輝かせる華やぎのあるブラウス2型を2月4日より全国のLEPSIM店舗と公式WEBストア、.stにて発売いたします。'

# とする
text = 'コールセンター・バックオフィスの構築・運営を行うセコムグループの株式会社TMJは、在宅コンタクトセンター化に向け設計・構築・マネジメントまでを一気通貫でサポートするサービスとして、「在宅オペレーション」の提供を開始しました。'

kyword_list = model.text_treace(text) # キーワードの候補の抽出
keyword_list = model.pas_get(text) # キーワードの候補の抽出
