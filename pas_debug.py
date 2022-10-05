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

# あとで
text = 'ベーカリーカフェ「パンとエスプレッソと」をはじめ、国内で22店舗を展開する日と々とが、パニーニ専門店「パニーニ一番」を千駄ヶ谷に出店する。'
text = 'ゼンハイザージャパン株式会社はクリエーターやビデオグラファー、モバイルジャーナリストが動画の音質を向上させるオンカメラマイク、MKE 400-IIと、スマートホンクランプおよびミニ三脚を付属したMKE 400-II Mobile Kit、を1月27日より発売いたします。'
text = '株式会社フォーティーズ株式会社フォーティーズは50歳以上限定の西なびグリーンパス、JR西日本管轄の普通車自由席が乗り放題と当社提携ホテルもしくはお客様がご希望のホテル・旅館などをお手配するプランを2022年1月14日より追加発売開始しました。'
# に　格
text = '新エネルギー・産業技術総合開発機構はこのほど、未利用熱エネルギー革新的活用技術研究組合、産業技術総合研究所とともに熱関連材料の熱物性情報と関連データを収集・体系化したデータベースシステム「PropertiesDB Web」を開発し、TherMATのHPで公開した。'

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

# 独立して処理する 分けたい
text = 'パナソニック四国エレクトロニクス株式会社、パナソニック補聴器株式会社は、"聞きたい音をよりくっきり、よりはっきり"と題し、入力音を128バンドの周波数帯域に分割し独立して処理することのできる高性能DSPを搭載したデジタル補聴器「ONWAモデルEJシリーズ」5形状、全8機種を2007年8月20日より発売いたします。'

# 〇〇」と　、と　も同じ　　　　　　　　　　する→最大限協力する　　　　　　　　　大きな意味がある
text = '長崎知事は「リニアは東京から少なくとも名古屋までつながることに大きな意味がある。JR東海には静岡県の理解を得て工事を進められるようにしてもらいたい。山梨県も最大限協力する」とこれまでの考え方を改めて強調した。'

text = '株式会社リアライズは、3月2日~3月5日までの期間中、アニメ・漫画専門ECサイトであるAnimoで「名探偵コナン アクリルフィギュア、PALE TONE series flower ver.」の予約販売を開始いたします!'

text = 'ソラコムは1月18日、オンラインセミナー・ワークショップ「事例から学ぶ!失敗しないIoTプロジェクトの始め方」を開催する。'
#text = '「事例から学ぶ!失敗しないIoTプロジェクトの始め方」'

#text = 'トヨタは東京オートサロン2022で「GRMNヤリス」を発表。'
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

#text = "カツ丼チェーン「かつや」や唐揚げ店「からやま」を運営するアークランドサービスホールディングスが新型コロナウイルス下で安定した収益をあげている。"
#text = "コロナ下で大ヒットを記録した商品がある。辞任する覚悟がある。"
#text = "当初は現地で実施する予定だったが、新型コロナウイルスの変異型「オミクロン型」の感染拡大を受け変更する。"
#text = "2021年のビジネス界は、各産業の地殻変動が表面化したような出来事が目立った。"
#text = "携帯電話各社は料金を引き下げた新プランを出し、競争が新たな土俵に移った。"
#text = "個別サーバーを新設して同種システムを開発する場合に比べ、導入費用を半分程度に抑える。"
text = "新たに開発したフィルムはEVのパワーコントロールユニットに搭載するコンデンサー用フィルムで、800ボルト超の高電圧にも耐えられる強度を持たせた。"

text = "文部科学省は2030~40年代を見据えた次世代の宇宙輸送機の開発方針を大筋でまとめた。"
text = "デジタル庁は2025年度末までに政府共通の「ガバメントクラウド」を整備し、自治体の税や住民基本台帳などの業務基幹システムを移す方針だ。"

# debug
pas_get(True, text)