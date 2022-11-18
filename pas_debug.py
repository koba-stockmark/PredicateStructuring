import json
import spacy
from data_dump import DataDumpSave
from pas_analysis import PasAnalysis

pas_model = PasAnalysis()
d_d_s = DataDumpSave()

nlp = spacy.load('ja_ginza_electra')  # Ginzaのロード　tranceferモデル


def pas_get(debug, text):
    ##########################################################################################################################################
    # 形態素解析
    ##########################################################################################################################################
    doc = nlp(text)  # 文章を解析
    d_d_s.text_treace(*doc)
    ##########################################################################################################################################
    # 述語項構造解析
    ##########################################################################################################################################
    pas_result = pas_model.pas_analysis(debug, text, *doc)
    argument = pas_result[0]["argument"]
    predicate = pas_result[0]["predicate"]
    ret = d_d_s.data_dump_and_save3(text, argument, predicate)
    return ret

###############################################

text = '太郎はお腹が空いてラーメンを食べたので太った。'
text = '電車が空いてくる。'
text = 'サンワサプライ株式会社は、座った際に膝の上でノートやタブレット、スマートフォンの操作を快適に行なえるラップトップテーブル「200-HUS015GY」、「200-HUS016GY」を発売した。'

text = '交通系ICカードやイーウォレットを展開する決済サービスのタッチ・アンド・ゴーは、ファミリーマート・マレーシアとの提携により、「TNGイーウォレット」を利用してファミリーマート商品の配送サービスが利用できるようになったと発表した。'

#text = '食べる。食べれる。読む。読める。利用する。利用できる。'
text = '総務省が所管する地方公共団体情報システム機構は26日、マイナンバーカードを使って、コンビニで住民票など証明書を交付するサービスが各地で一時利用できなくなっていると明らかにした。'
###text = '日本製紙は9日、同社が開発したストローがない学校給食用牛乳パックの採用が4月以降に広がり、年100トンのプラスチックが削減できる見通しになったと明らかにした。'
#text = 'Tronsmartはまたしても特許取得済みの最先端技術を獲得し、屋外パーティースピーカー分野にチャレンジした。'

text = 'リンガーハットなど外食各社が自動販売機を使った「夜営業」に乗り出している、と2日付の日本経済新聞朝刊が報じている。'
text = '2010年代にはミレニアル世代には「様々な業界をぶち壊し、アボカドトーストには出費を惜しまない」という固定観念があったが、今や大きく成長している。'
text = '同社は保温機能を備えたスマートマグカップで知られているが、以前からコールドチェーン、特に医薬品の長距離輸送に注目したきた。'
text = 'DMM GAMESは、PC用タワーディフェンスRPG「モンスター娘TD ~ボクは絶海の孤島でモン娘たちに溺愛されて困っています~」を3月14日に配信する。'

text = '株式会社リアライズは、3月2日~3月5日までの期間中、アニメ・漫画専門ECサイトであるAnimoで「名探偵コナン アクリルフィギュア、PALE TONE series flower ver.」の予約販売を開始いたします!'

text = 'ソラコムは1月18日、オンラインセミナー・ワークショップ「事例から学ぶ!失敗しないIoTプロジェクトの始め方」を開催する。'
#text = '「事例から学ぶ!失敗しないIoTプロジェクトの始め方」'

#text = 'トヨタは東京オートサロン2022で「GRMNヤリス」を発表。'

#text = "前者は電気自動車で世界一になり、太陽光発電を広め、宇宙開発でも成果をあげた。"
#text = "単年の個人の納税額としては米国で過去最大になると主張している。"
#text = "本数不足は管理コストを増大する要因になっているといい、同システムを日本酒やクラフトビール、ワインのメーカーなどに売り込む。"
text = "2022年がどんな年になるか、と質問されたのだが、手短に言えば「本格的に「市民データサイエンス」の波が訪れる年」なのではないかと考えている。"
#text = "教科書のオンライン化が進んだり、リモート学習のためのプラットフォームが整備されたりといった話題は多いわけだが、学習のオンライン化が現実の大学教育自体のあり方を再考させるきっかけになっている点が興味深い。"

text = "学校なのではないかと考える"
text = "学校だと考える"
text = "学校なのではないか"

text = "今から15年以上前、静岡県東部の自治体や企業の健康診断で栄養指導を行った際、食生活を変えようとやる気になったにもかかわらず、健康的な食事を入手する方法がなく挫折する人々に出会った。"

text = "輸送の低炭素化に必要不可欠なバイオ燃料だが、原料によっては本当に温暖化ガスの排出量を削減できるのか疑問の声もある。"
text = "温暖化ガスの排出量を削減できるのか不透明感もある。"

text = "五反田はオフィス賃料の低さや周辺の暮らしやすさが魅力の半面、会社が大きくなり渋谷や都心へ移るまでのステップにもされがちだ。"
text = "「的外れな業績なら辞任する覚悟はあるのか」。"
#text = "太郎はラーメンならば勉強する"
#text = "的外れな業績なら"
#text = "食べる準備はある"

#text = "東芝は17日、2022年2月に投資家向けの経営戦略説明会を開催する予定だと明らかにした。"
#text = "大商は授賞理由について「新型コロナウイルスワクチンの職域接種について、取引先や周辺飲食店にも声をかけて従業員数の3倍以上の約1600人に実施。地元経済を支える中小零細企業に安心して働ける環境を提供し、地域社会に貢献した」とした。"
#text = "青森県に次ぐ量で、都道府県全体では11%増の1740トンとした。"

#text = "カツ丼チェーン「かつや」や唐揚げ店「からやま」を運営するアークランドサービスホールディングスが新型コロナウイルス下で安定した収益をあげている。"
#text = "コロナ下で大ヒットを記録した商品がある。辞任する覚悟がある。"
#text = "当初は現地で実施する予定だったが、新型コロナウイルスの変異型「オミクロン型」の感染拡大を受け変更する。"
#text = "2021年のビジネス界は、各産業の地殻変動が表面化したような出来事が目立った。"
#text = "携帯電話各社は料金を引き下げた新プランを出し、競争が新たな土俵に移った。"
#text = "個別サーバーを新設して同種システムを開発する場合に比べ、導入費用を半分程度に抑える。"

#text = "カツ丼チェーン「かつや」や唐揚げ店「からやま」を運営するアークランドサービスホールディングスが新型コロナウイルス下で安定した収益をあげている。"
#text = "売上高は前期比9%減の270億円、営業損益は31億円の赤字を見込む。"

#text = "混乱を極めたのは、株式会社の意思を決定する最高機関である株主総会に向き合う株主一人の未熟な行為があったからだが、実は裁判を招いた株主以外にも、議決権行使を巡り、株主の本来の意思とは逆にとられたケースがあったようだ。"

#text = "脱炭素の流れを受けて化石燃料から再生可能エネルギーへの転換が急速に進む中、石油元売り業界が抜本的な事業構造の変革を迫られている。"
#text = "合弁会社は両社を折半出資とし、半導体ウエハーの洗浄剤に使われる高純度イソプロピルアルコールの工場を韓国南東部の蔚山市に新設する。"
# ようにする
#text = "高速回転時でも内部の油の流れを見えるようにした装置で、高品質な軸受けをより短い納期で提供できるようになる。"

#text = "独禁訴訟の一審を扱った米カリフォルニア州の連邦地裁は9月10日付の判決で、アプリ内に外部の決済手段に誘導するリンクの設置を認めていないアップルの規約が反競争的だと認定。"
#text = "一部の住宅は宿泊体験ができるようにし、住み心地を体感してもらう。"
#text = "「すでに世界中でオミクロンが確認されるなか、渡航禁止措置は馬が逃げた後に小屋の扉を閉めるようなもので効果がない」と述べた。"
#text = "緊急事態宣言が解除され、外で飲めるようになり安心している。"
#text = "「Buykは、蛇口をひねったら水道から水が出るような感覚で、食品を届けたいと思っている。"
#text = "クラシックで高級感のあるデザインにしたほか、写真をプリントするためのレバーを備えるなどアナログな操作感を追求した。"


# NG　〇〇や〇〇の〇〇
text = "パクスロビドは新型コロナ患者の治療に用いる飲み薬で、点滴による抗体カクテル療法に比べて患者や医療現場の負担を軽減できるとされる。"
text = "品種や検疫の問題から国産への切り替えが難しく、「芋騒動」の収束にはなお時間がかかりそうだ。"

# OK　〇〇や〇〇の〇〇
text = "ベトナムの小売り最大手マサングループは2022年、傘下のコンビニエンスストアの半数以上にカフェや金融機関の店舗を併設する。"
text = "巨額買収や新分野への投資に取り組むENEOSホールディングスの大田勝幸社長に、業態をどう変えていくべきなのか聞いた。"
text = "医療機関や販売パートナーの企業が求める情報を常に先回りして収集し、いち早く提供して導入施設数を2倍余りに伸ばした。"
text = "ところが、気温や海面の上昇、異常気象などによる損失と被害の拡大に危機感を強める途上国が支援の上積みを主張。"
text = "AGCは寝具や自動車のシートなどのクッション材に使うウレタンの原料を2022年1月1日納入分から値上げする。"

# あとで
text = 'ベーカリーカフェ「パンとエスプレッソと」をはじめ、国内で22店舗を展開する日と々とが、パニーニ専門店「パニーニ一番」を千駄ヶ谷に出店する。'
text = 'ゼンハイザージャパン株式会社はクリエーターやビデオグラファー、モバイルジャーナリストが動画の音質を向上させるオンカメラマイク、MKE 400-IIと、スマートホンクランプおよびミニ三脚を付属したMKE 400-II Mobile Kit、を1月27日より発売いたします。'
text = '株式会社フォーティーズ株式会社フォーティーズは50歳以上限定の西なびグリーンパス、JR西日本管轄の普通車自由席が乗り放題と当社提携ホテルもしくはお客様がご希望のホテル・旅館などをお手配するプランを2022年1月14日より追加発売開始しました。'
# に　格
text = '新エネルギー・産業技術総合開発機構はこのほど、未利用熱エネルギー革新的活用技術研究組合、産業技術総合研究所とともに熱関連材料の熱物性情報と関連データを収集・体系化したデータベースシステム「PropertiesDB Web」を開発し、TherMATのHPで公開した。'

# 連体修飾
text = "新たに開発したフィルムはEVのパワーコントロールユニットに搭載するコンデンサー用フィルムで、800ボルト超の高電圧にも耐えられる強度を持たせた。"
text = "小売店向けのシステムを手掛けるgooddaysホールディングスは、クラウド上でPOSデータを管理できるシステムを開発した。"
# 一度は
text = "「一度は死んだ身。思い切ったことができる」と話し、事業モデル変革を推し進める。"

### 「ちょいさき」とタイアップ
text = '丸井織物株式会社、の運営するオリジナルT、シャツ作成サービス「Up-T」は、FM NACK5のラジオ番組「ちょいさき」とタイアップしてオリジナルの公式コラボグッズの販売を2022年2月14日から開始します。'
# 今夏をめどに
text = '加賀市のホテルアローレは今夏をめどに、敷地内に高級志向のキャンプ「グランピング」を楽しめる施設をオープンさせる。'
# 白と黒
text = 'パナソニック株式会社は、20,000時間の長寿命と、白と黒のコントラスト感をアップし、文字をくっきり読みやすくした「文字くっきり光」を搭載した丸形蛍光灯「パルック、20000」を2015年6月1日より発売します。'
# 枯死させる の対象が　特定外来生物のオオバナミズキンバイとナガエツルノゲイトウ　である関係を導きたい
text = '県や琵琶湖岸の10市などで作る琵琶湖外来水生植物対策協議会は2日、特定外来生物のオオバナミズキンバイとナガエツルノゲイトウの駆除に向け、遮光シートで覆って枯死させる実験を草津市で始めた。'
# 様々な分野
text = '株式会社ジャパンナノコートが開発した可視光熱触媒コート剤:時事ドットコム、密着性能の高い無機バインダー及びシングルナノ粒子の精製技術により、和紙や金属などあらゆる素材へ固着するコーティング剤は、医療現場や伝統工芸など様々な分野で実用化。'
#text = 'Media Data Tech Studioの協力のもとシステムを導入しております。'
text = 'オークネットは、サステナビリティポリシーとして「価値あるモノを、地球規模で循環させる~Circulation Engine.」を制定し、あらゆる「価値あるモノ」を「必要な人のもと」へ循環させる"循環型流通"の構築に取り組んでおります。'
# 「暮らす」ように「泊まる」という理念のもと
text = 'リソル不動産では、「暮らす」ように「泊まる」という理念のもと、高級別荘やリゾートマンションを1泊から1ヶ月以上の長期滞在まで多目的に楽しめる「リソルステイ」事業を展開。'

## 付の
text = '25日付の日本経済新聞朝刊は、同社がネットスーパーのスタートアップ、OniGOと組み、注文を受けてから原則10分以内に商品を届けるサービスを月内に始めると報じた。'
# 導入
text = "SGST、キャスコ花葉、CLUB、にて配膳ロボット「BellaBot」を導入、:時事ドットコム、IoT・AI、ソリューション開発の株式会社、SGSTは、新型コロナウィルス対応として飲食店、レジャー施設、医療機関向けにロボットによる非接触サービス化の展開を進めています。"
## そんな利便性
text = 'そんな利便性をさらに高めようと、AppleはスマートフォンのUIを装着したアクセサリーに合わせて変える技術を考案。'
### 可能性がある
text = 'TWITTERが、元ツイートやリプライからタグ付けを解除できる新機能「この会話を離れる」をテストしている可能性があると報じられました。'
### 造り続ける」
text = '新経営体制整備の背景当社は「想いと未来を実現するプロダクトを造り続ける」をミッションに、カスタマーデータプラットフォームやマーケティグオートメーション機能を持つマーケティングDXツール「Aimstar」の開発・販売を...'
### 豚骨スープの飲み残し
text = 'その会社は豚骨スープの飲み残しをラーメン店から集めて、石油に頼らないバイオディーゼル燃料を製造し、運送業務を行っているという。'
### 主語　iOS、Android向け対戦格闘RPG「バキ、KING OF SOULS」　＋　に関する
text = 'パブリッシャーのGrandSoftは2月18日、アニメ「刃牙」シリーズを題材としたiOS、Android向け対戦格闘RPG「バキ、KING OF SOULS」に関する事前登録の受付を開始した。'

# 独立して処理する 分けたい
text = 'パナソニック四国エレクトロニクス株式会社、パナソニック補聴器株式会社は、"聞きたい音をよりくっきり、よりはっきり"と題し、入力音を128バンドの周波数帯域に分割し独立して処理することのできる高性能DSPを搭載したデジタル補聴器「ONWAモデルEJシリーズ」5形状、全8機種を2007年8月20日より発売いたします。'

# 〇〇」と　、と　も同じ　　　　　　　　　　する→最大限協力する　　　　　　　　　大きな意味がある
text = '長崎知事は「リニアは東京から少なくとも名古屋までつながることに大きな意味がある。JR東海には静岡県の理解を得て工事を進められるようにしてもらいたい。山梨県も最大限協力する」とこれまでの考え方を改めて強調した。'

### 副詞
text = 'パナソニック四国エレクトロニクス株式会社、パナソニック補聴器株式会社は、"聞きたい音をよりくっきり、よりはっきり"と題し、入力音を128バンドの周波数帯域に分割し独立して処理することのできる高性能DSPを搭載したデジタル補聴器「ONWAモデルEJシリーズ」5形状、全8機種を2007年8月20日より発売いたします。'
text = 'パナソニック株式会社、エコソリューションズ社は、2012年10月21日発売のホームエネルギーマネジメントシステム「スマートHEMS」を2013年7月末に、3万台販売達成しました。'
text = '東北大学大学院工学研究科、東芝は、車載用等の小型モーター向けに、性能は現在と同等で、より継続的に生産を続けられ、さらに安価に生産できる可能性のある新しい等方性ボンド磁石を開発した。'
# 通してやりたいこと
text = 'キャリアサポーターと1対1でメール形式のワークを通してやりたいことや強みを見つける「大人の自己分析プログラム」を2022年1月24日にリリースします。'
# 人間の手とほぼ同じ
text = 'シンガポールの南洋理工大学からスピンオフした企業であるEureka Roboticsは、産業用ロボットが微細な物を人間の手とほぼ同じ感度で機敏に扱えるようにする技術を開発した。'
# 用語リンク大百科用語リンク
text = '用語リンク大百科用語リンク、株式会社エヌアイデイは、株式会社Studio Ousiaの開発したSaaS型QAシステム「アンサーロボ」と連携し、学習済みAIでFAQ登録後すぐに利用できるAI FAQ「OHGAI」をリリースしました。'
# 主な
text = '新社会システム総合研究所は、1996年12月6日に設立、創業以来26年以上、法人向けビジネスセミナーを年間約500回企画開催する情報提供サービスを主な事業としております。'
# より高いうるおい効果
text = 'アプライアンス・ウェルネス マーケティング本部は、水に包まれた微粒子イオン「ナノイー」を搭載し、加湿と「ナノイー」の相乗効果により、清潔でより高いうるおい効果を実現した加湿セラミックファンヒーター「DS-FKX1201」を9月1日より発売します。'
# 待ち
text = 'JR東日本などは東京駅・八重洲口のタクシー乗り場に並んでいる人の数や待ち時間の見通しをウェブサイトに表示する実証実験を始めました。'
# 8mから
text = 'プラス株式会社は、2022年2月22日にテープの長さを8mから10mに25%増量したテープのり「ノリノビーンズ」をリニューアル新発売します。'
# より便利により使いやすく、バージョンアップしました
text = 'パナソニック株式会社は、2016年10月5日より、放送中の番組や録画した番組を、ビエラやディーガからスマートフォンやタブレットに転送し、外出先や家の好きな部屋で視聴できるリモート視聴用アプリ「Panasonic Media Access」をより便利により使いやすく、バージョンアップしました。'
# 国民保護情報や警報など、緊急時のお知らせの際に鳴動する通 並列
text = "株式会社リットシティは、自社開発の自治体向け広報・防災アプリ「Ap-Portal」に、国民保護情報や警報など、緊急時のお知らせの際に鳴動する通知音を追加し、通常の通知と識別できる新機能を追加開発したことをお知らせ致します。"
# 際に
text = 'JR東日本は、乗客がSuicaを利用した際に記録されるデータを、個人が識別されないよう統計処理したうえで、鉄道等のサービス向上に活用するとともに、自治体のニーズに応じた分析レポートをこれまでも提供してきました。'
# 座った際に
text = 'サンワサプライ株式会社は、座った際に膝の上でノートやタブレット、スマートフォンの操作を快適に行なえるラップトップテーブル「200-HUS015GY」、「200-HUS016GY」を発売した。'
# 〇〇以外にも　その他もおかしい
text = '完全ワイヤレスイヤホン用のケースやミニポーチのほか、<エルメス>ではiPhoneやiPadの「探す」アプリと連動した「AirTag Hermes」が登場するなど、飾る以外にも機能をもつアクセサリーが発売されている。'
# 光の透過具合 並列や重複
text = '東京大学は2月4日、異なる3方向から見たときの光の透過具合、吸収係数が40%以上変化する反強磁性体を発見したと発表した。'

# ダミー主語　
text = '大建工業は、犬の歩行に配慮した"滑りにくさ"というペット視点の機能はもちろん、傷に強い、汚れにくい、変色しにくいといったユーザー視点の機能も併せ持つペット共生住宅用フローリング「ワンラブフロア」を、8月21日から全国発売いたします。'
text = '渡島総合振興局は、道南地域で食産業に携わる事業者を対象に、オンライン商談やSNSを活用した情報発信などの「デジタル力」向上を図る無料セミナーを1月~3月に開催する。'
text = '中小機構北陸本部、鯖江市、鯖江商工会議所は、持続可能な開発目標への対応を通じた企業の経営課題解決の取組みとして、3機関の連携により、SDGsに貢献する商品の販路開拓支援を開始します。'
text = '横浜ゴムは2月17日、ホース配管事業強化の一環として、米国およびメキシコの自動車用ホース配管の生産体制再編を発表した。'

# PAS
text = "トヨタやホンダは脱炭素社会に向け、EVに大きく転換する戦略を打ち出した。"

# 〇〇が〇〇中の〇〇
text = "塩野義製薬は27日、サスメドが開発中の不眠症治療用アプリの販売提携契約を結んだと発表した。"

# 主語　連用修飾
text = "同日記者会見した福原正大社長は「新型コロナウイルスの影響で学校のデジタル化が進み、結果的に追い風になった」と話した。"
text = "政府は1日から1日あたり入国者数の上限を3500人に減らしており、各社はこの範囲内で新規の予約を再び受け付ける見通し。"
text = "新型コロナウイルス禍が長期化する中、首都圏の中小企業が生き残りをかけて苦闘している。"

# 安く買う点に
text = "ブロックチェーン技術開発のブロックストリームのアダム・バック最高経営責任者は100%再生可能エネルギーで電力をまかなうビットコインのマイニング施設について、「余剰電力を安く買う点にコスト競争力がある」と述べた。"
# 考えるようになってきた」と
text = "そのうえで「理想的な姿は東京から名古屋の開通だが、時間がかかるようであれば、そろそろ山梨までの先行開業も議論されてもよいのかなと思う。私もだんだんそのように考えるようになってきた」と心境の変化があったことを打ち明けた。"

# での経験
text = "大手メーカーなどでの商品企画やマーケティングの経験を生かし「新しい切り口の商品を大ヒットさせるステージに引き上げたい」と意気込む。"

text = "文部科学省は2030~40年代を見据えた次世代の宇宙輸送機の開発方針を大筋でまとめた。"
text = "デジタル庁は2025年度末までに政府共通の「ガバメントクラウド」を整備し、自治体の税や住民基本台帳などの業務基幹システムを移す方針だ。"

text = "持ち帰りをにらんだメニューを機動的に投入し、業績変動の少なさは外食大手で最高水準だ。"
text = "ウェザーニューズは28日、2022年5月期の連結純利益が前期比7%増の20億円になる見通しだと発表した。"

text = "この素粒子を調べることで、宇宙がどのようにして生まれ続けるのかを解き明かそうとしている。"
text = "この素粒子を調べることで、宇宙がどのようにして生まれ存在しないのかを解き明かそうとしている。"
#text = "パクスロビドは新型コロナ患者の治療に用いる飲み薬で、点滴による抗体カクテル療法に比べて患者や医療現場の負担を軽減できるとされる。"
#text = "香川県は競争力を発揮できると期待している。"

#text = "合弁会社は両社の折半出資とし、半導体ウエハーの洗浄剤に使われる高純度イソプロピルアルコールの工場を韓国南東部の蔚山市に新設する。"
#text = "合弁会社は両社を折半出資とし、半導体ウエハーの洗浄剤に使われる高純度イソプロピルアルコールの工場を韓国南東部の蔚山市に新設する。"

#text = "大きな災害では家具、畳、廃材などの木質廃棄物が大量に出る恐れがあり、迅速に処理できれば復興も進めやすくなるとみている。"

# fixed　エラー
# OK
text = "ところが、気温や海面の上昇、異常気象などによる損失と被害の拡大に危機感を強める途上国が支援の上積みを主張。"
#NG
text = "これまで気候資金の用途は、温暖化ガス削減の取り組みである「緩和策」と、気候変動の影響を軽減・回避するための「適応策」とされてきた。"
text = "12兆円にも達すると言われる市場をめぐる個人と企業の動きについてまとめました。"
text = "ジンジャーは人事労務のほか勤怠管理や給与計算といった企業などの事務作業に使うシステムを、クラウドでソフトを提供するSaaS型で手掛ける。"
text = "毎年、東工大の同窓会組織である「蔵前工業会」と一橋の「如水会」が合同で移動講座を開いています。"
text = "中国やロシアといった強権国家で疑われている弾圧などの人権侵害行為に悪用されるのを防ぐ。"


text = "実家の母や兄と食事をしながら「新しい会社の名前をどうしようか。マルチメディアのようなかっこつけたものでなく、直球がいいのだけど」と問うと、兄の元道が「スマイル」を口にしたのです。"
#text = "当初は現地で実施する予定だったが、新型コロナウイルスの変異型「オミクロン型」の感染拡大を受け変更する。"

text = "米国や中国の企業に比べて高度な自動運転の実用化で出遅れていたが、日本勢は普及車への搭載で巻き返す。"
text = "消毒液としてのほか、加湿器などに入れ噴霧して使う。"
#text = "メーカーが値上げを相次ぎ表明しているものの、消費者離れを懸念する小売りが抵抗し、最終価格になかなか反映されない実情がデータからうかがえる。"

text = "原料の鉄スクラップ価格が高止まりしているものの、「H形鋼など他の建築材に比べ価格改定が進んでいない」という。"
text = "ともに「もめ事」案件として日々の紙面をにぎわしているが、共通点はそれだけではない。"
text = "中国に製造拠点を置く自動車メーカーなどが生産性の向上を急ぐなか、産業ロボ需要が急速に高まっているためだ。"
text = "グループの配送拠点も使いながら、2022年度半ばから試行的に事業を始め、本格展開をめざす。"
text = "中国の独禁当局の動きを警戒しているほか、統合後の新会社の本拠地を日本と米国のどちらかに置くかでも意見が割れたままだ。"

text = "金額などは明らかになっていないが、恒大の資金繰りの改善にある程度つながる可能性がある。"

text = "東芝では4月以降、投資ファンドからの初期段階の買収提案の取り扱いや前社長の突然の辞任、2020年7月の株主総会が公正に運営されていないとされるなど、企業統治を巡る迷走が続く。"
#text = "パナソニックは15日までに、保有するフィルムコンデンサーの特許が侵害されているとして、中国電子部品メーカーのアモイ・ファラトロニックを提訴した。"
#text = "同社は今年に入ってすでに4度の値上げを実施しているが、原料となるチタン鉱石の価格の高騰が続いて採算が悪化しているとしてさらなる価格転嫁に踏み切る。"
#text = "世界でワクチン需要が拡大するなか、配送の遅れがでているほか、生産拡大に伴う一時的な影響が出ているとした。"
#text = "クレジットカード情報は含まれていないとしている。"
#text = "採算が悪化しているとしてさらなる価格転嫁に踏み切る。"

text = "航行時間やアンケート調査から海上交通のニーズを調べるほか、国際会議や展示会など「MICE」を船上で開催できるか実現可能性を探る。"

text = "供給が増えるのは来秋以降との観測もあり、当面は高値が続く見通し。"
text = "ショールームは、顧客にEVの実車を見てもらうほか、使い方を説明したり、商談をしたりする場所として使う。"
#text = "梱包したりするのではなく、ただお店を呼べばいいシンプルさにある。"
text = "新しい食文化と思いきや、実は昭和の子どもたちも知らずに食べていた。"
text = "ショールームは、顧客にEVの実車を見てもらうほか、使い方を説明したり、商談をしたりする場所として使う。"
#text = "動植物などを原料とし温暖化ガスの排出を抑制するバイオ燃料。"

#text = "ANAホールディングスやJTBなどが2023年度に新卒採用を再開すると発表。"
#text = "例えば私の恩師ぐらいの世代であれば、データ分析をしようとすると、大学の大型計算機センターにプログラムとデータを打ち込んだパンチカードを持参しなければならなかった経験があるそうだ。"
#text = "例えば私の恩師ぐらいの世代であればそうだ。"
#text = "田中氏は11月、社内規定に違反する株取引をしていたとして、月額報酬の全額返上などの処分を受けていた。"
#text = "脱炭素の流れを受けて化石燃料から再生可能エネルギーへの転換が急速に進む中、石油元売り業界が抜本的な事業構造の変革を迫られている。"
#text = "できる限りの「無添加」にこだわった理由のひとつは、家内の由美の存在にあります。"
text = "「茨城県笠間市とNTT東日本茨城支店は同市職員を対象に、あらゆるモノがネットにつながる「IoT」を使った健康管理支援の実証事業を始めた。"

# debug
pas_get(True, text)