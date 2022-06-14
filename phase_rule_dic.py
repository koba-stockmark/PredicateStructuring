class PhaseRule:
    """
    フェーズルール

    構想、研究、開発、実験、製品、更新、中止、参画、利用、組織、連携、通知、手続き、その他

    """

    # 構想
    kousou_dic = [
        "コンセプト", "ミッション", "めざす", "レイアウト提案", "開拓", "開発計画", "願う", "企画、開発", "企画、販売", "企画",
        "企画及び開発", "企業理念", "掲げる", "計画", "構想", "考える", "考案", "実現", "着手", "着目", "調査", "追求", "分析", "目指す",
        "目的", "予測", "予定", "求める", "ビジョンに", "プランニング", "開発意向表明", "発明", "模索"
    ]

    # 研究
    kenkyuu_dic = [
        "解析研究", "確認", "確立", "企画、開発", "研究", "研究・開発", "研究開発", "共同研究", "発明", "発見"
    ]

    # 開発
    kaihatsu_dic = [
        "アプリ開発", "開発", "開発、受注販売", "開発・提供", "開発・納入", "開発支援", "開発中", "開発提供", "企画・開発", "企画及び開発",
        "技術開発", "構築", "共同開発", "共同開発・投資", "自社開発", "商品開発", "設計", "開発・運営", "開発・実証",
        "開発・販売", "研究・開発", "研究開発", "再資源化技術開発", "新開発", "展開・開発", "不動産開発", "開発したこと", "サービスの開発"
    ]

    # 実験
    jikken_dic = [
        "クローズドテスト", "サンプル出荷", "テスト", "テスト運用", "テスト販売", "デモ展示", "運行実験", "参考出展", "参考展示", "試みる",
        "試験打ち上げ", "試験導入", "試行", "試作", "実証", "実証試験", "実証実験", "実証販売", "社会実験", "走行テスト", "走行試験",
        "耐寒テスト", "臨床試験", "開発・実証", "開発実証試験", "公道配送実証", "視認率計測実験", "人命救助実証試験", "相互運用性試験",
        "実験", "試験販売", "成功", "共同実証実験", "検証", "達成", "試験", "試験生産", "成功", "増強", "試験運用"
    ]

    # 製品
    seihin_dic = [
        "12商品発売", "2,489店舗展開", "20店舗展開", "2機種販売", "2種類発売", "2店舗同時オープン", "6機種発売", "90店舗展開", "API提供",
        "WEB先行発売", "YouTubeライブ配信", "アドバイスサービス", "ウェブ販売", "オープン", "オンデマンド配信", "オンライン配信",
        "キャリア支援", "グローバルサービス", "グローバル発売", "コーヒー製造", "コンテンツ販売", "ご提供", "サービス", "サービス開始",
        "サービス提供", "サブスクリプション提供", "サブスクリプション配信", "シェアリングサービス", "スタート", "ダウンロードサービス",
        "テークアウト", "デリバリーサービス", "パッケージ販売", "プレゼント", "プロデュース", "ライブ配信", "ラストワンマイル宅配",
        "リリース", "リリース", "レンタルサービス", "ローンチ", "わけて発売", "安定提供", "一般発売", "運営", "運航", "運行", "運用",
        "運用支援", "押印サービス", "花摘み体験", "開く", "開業", "開校", "開始", "開設", "開発、受注販売", "開発・提供", "開発・納入",
        "開発支援", "開発提供", "割引販売", "刊行", "完成", "完了", "企画、販売", "企画・販売", "期間限定発売", "供給", "共同提供", "掲載",
        "建設", "建築", "限定発売", "限定販売", "公開", "公開", "好評販売", "構築", "国内導入", "国内発売", "国内販売", "最終デザイン",
        "採用", "作製", "事業", "自社開発", "自社栽培", "自動化", "実演販売", "実施", "実施中", "実践", "実装", "実用化", "取りそろえる",
        "取り扱う", "取り込む", "取引", "手掛ける", "受け付け", "受け付ける", "受注", "受注販売", "受付け", "受付", "出荷",
        "出張サービス", "出展", "出店", "出店支援", "出版", "商品化", "小売り", "承認", "常設展示", "植栽", "新サービス", "新作", "新車", "新型",
        "新設", "新築", "新発売", "遂げる", "数量限定発売", "制作", "正式サービス", "正式リリース", "生産", "製作", "製作販売", "製造",
        "製造受託", "製造販売", "製品化", "製品発売", "請け負う", "設置", "先行オープン", "先行展示", "先行導入", "先行発売", "先行販売",
        "先行販売中", "先行予約", "先行予約受付中", "先行予約販売", "先行予約販売受付中", "全国運用", "全国展開", "全国発売", "創る",
        "創製", "打ち上げる", "代理店募集", "宅配サービス", "単体販売", "抽選販売", "注文受付", "直販", "提供", "提供サービス",
        "提供開始", "提供中", "展開", "展開中", "動画配信", "同時リリース", "同時発売", "特別サポート", "突破", "届ける", "届ける",
        "認証サービス", "納入", "配信", "配信中", "配達サービス", "配布", "買取りサービス", "売り出す", "売却", "発刊", "発行", "発信",
        "発売", "発売中", "発表", "発表、展示", "販売", "販売開始", "販売中", "披露", "複数展開", "放送", "本格サービス", "本格稼働",
        "本格提供", "本格展開", "本格導入", "本格販売", "無償提供", "無償配布", "無料オンライン開催", "無料提供", "無料配布",
        "有料生配信", "予約受付", "予約販売", "利用可能", "一般販売", "量産", "扱う", "展開", "商用提供開始", "システムサービス提供",
        "デザイン・施工", "プレオープン", "ホームページ制作サービス", "ホワイトペーパー提供", "マーケティングDX支援",
        "リニューアル新発売", "一般向け提供", "開発・運営", "開発・販売", "事業化", "新サービス提供", "新プラント建設", "製造・販売",
        "展開・開発", "販売及び技術サポート", "販路開拓支援", "無償ダウンロード提供", "商用提供",
        "登場", "リニューアル新発売", "始動", "投入", "量産", "量産化", "誕生"
    ]

    # 更新
    koushin_dic = [
        "アップ", "アップデート", "カスタマイズ", "サポート", "バージョンアップ", "バレンタイン仕様", "フルアップデート",
        "マイナーチェンジ", "ラインアップ", "ランアップ", "リニューアル", "リニューアル提案", "リニューアル発売", "延期",
        "改善", "改良", "拡充", "拡大", "拡張", "急拡大", "継続", "減らす", "効率化", "向上", "更改", "更新", "高める", "再販売",
        "再編", "削減", "刷新", "自動化", "受け継ぐ", "収益化", "収益化支援", "集約", "充実", "伸ばす", "進める", "推進", "整える",
        "整理", "積極化", "切り替える", "全面リニューアル", "増強", "増設", "促進", "続ける", "短縮", "値上げ", "注力", "追加",
        "追加リリース", "追加納入", "追加発売", "徹底", "転用", "発展", "復活", "変革", "変更", "本格化", "強化",
        "リニューアル新発売", "生産体制再編", "変形", "加速", "リニューアル新発売"
    ]

    # 中止
    tyuushi_dic = [
        "やめる", "休止", "廃止", "中止", "終了", "ストップ"
    ]

    # 参画
    sankaku_dic = [
        "参画", "参入", "乗り出す", "新サービス", "新作", "新設", "新築", "新発売", "新発売", "設立", "着手", "着目", "発足", "立ち上げる",
        "新サービス提供", "新プラント建設", "初", "乗りだす", "本格参入", "進出", "参加"
    ]

    # 利用
    riyou_dic = [
        "国内導入", "採用", "参照", "使う", "使用", "借り受ける", "取り込む", "取引", "取得", "受ける", "受け継ぐ", "受け入れる",
        "搭載", "導入", "本格導入", "利用", "利用可能"
    ]

    # 組織
    soshiki_dic = [
        "移す", "育成", "加える", "稼働", "起こす", "技術者輩出", "迎える", "公募", "構える", "採用", "支える", "支援", "事業", "取り込む",
        "集める", "集約", "新設", "進化", "設ける", "設立", "担当", "統合", "発足", "募る", "募集", "立ち上げる", "人材育成", "新規会員募集",
        "キャリア採用"
    ]

    # 連携
    renkei_dic = [
        "API連携", "シングルサインオン連携", "データ連携", "連携", "プロジェクト受付", "プロデュース", "果たす", "供給", "共同開発・投資",
        "共同開発", "共同提供", "協業", "迎える", "結ぶ", "合わせる", "合弁生産・販売", "参画", "参入", "支える", "支援", "借り受ける",
        "取り込む", "取引", "取得", "受け継ぐ", "受け入れる", "受注", "受注販売", "請け負う", "接触", "組む", "組合せる", "貸与", "投資",
        "投資募集", "納入", "募る", "募集", "融合", "預かる", "連載", "連載", "接続", "相互運用性試験", "提携", "共創活動", "協力"
    ]

    # 通知
    tsuuchi_dic = [
        "あきらか", "アナウンス", "お知らせ", "お披露目", "プレスリリース", "プロジェクト受付", "延期", "可能", "稼働",
        "解決", "解説", "開校", "開講", "開催", "開催中", "開始", "開設", "開発中", "確認", "記念", "掲載", "決定", "検証",
        "見せる", "見越す", "見据える", "公開", "公表", "公募", "示す", "実現", "実施中", "受け付け", "受け付ける", "受賞", "受付け",
        "受付", "授業", "出展", "準備", "承認", "紹介", "常設展示", "推奨", "説明", "先行販売中", "先行予約受付中",
        "先行予約販売受付中", "打出す", "代理店募集", "提供中", "展開中", "展示", "伝える", "投稿", "搭載", "届ける",
        "配信中", "発見", "発生", "発売中", "発表", "発表、展示", "販売中", "披露", "表示", "複数展開", "募る", "募集", "報ずる",
        "報告", "報道", "放映", "放送", "本格展開", "無料オンライン開催", "予約受付", "予約販売", "利用可能"
    ]

    # 手続き
    tetsuzuki_dic = [
        "延期", "確認", "決定", "示す", "承認", "申請", "制定", "設定", "設立", "操縦", "定義", "提案", "提案", "提示", "提出", "検討",
        "締結", "登録予約", "投資募集", "統一", "認める", "認証", "予約", "預かる", "立案", "グローバル事前登録", "先行予約受付", "合意"

    ]

    # その他
    sonota_dic = [
        "明らかにする", "アプリ開発", "ある", "いく", "いたす", "うける", "エントリー", "おこなう", "キーデバイス",
        "つかむ", "つくる", "つなげる", "とりいれる", "はじめ", "プロデュース", "ペイント", "もつ", "もの", "わけて発売",
        "位置", "延ばすこと", "演出", "応援", "応援", "応用", "価値向上", "加える", "科学", "果たす", "稼働",
        "花摘み体験", "解決", "開く", "獲得", "確認", "掛け合わせる", "活かす", "活動", "活用", "叶える",
        "感ずる", "含める", "企業理念", "記念", "記録", "起こす", "急ぐ", "強める", "強化", "駆使", "経る", "迎える", "決定",
        "検証", "見せる", "見越す", "見据える", "呼ぶ", "効率化", "構える", "考える", "行う", "行く", "行なう", "根本的解決",
        "最終デザイン", "作る", "作成", "撮影", "参照", "参入", "使う", "使用", "始める", "始動", "支える", "支援", "視野",
        "事業", "事前予約", "持ち帰る", "持つ", "次ぎ打ち出す", "示す", "実現", "実装", "借り受ける", "主業務", "取りそろえる",
        "取り組む", "取り組み", "受ける", "受け継ぐ", "受け入れる", "受賞", "受注", "授業", "収める", "収益化", "収益化支援", "集める", "集約",
        "充実", "出し抜く", "準備", "所有", "承認", "紹介", "上げる", "飾り付ける", "食べる", "深める", "進める", "図る",
        "推奨", "遂げる", "整える", "整備", "整理", "生かす", "生み出す", "請け負う", "積み重ねる", "切る", "接触", "設ける",
        "設定", "選択アドバイス", "狙う", "組み込む", "組む", "組合せる", "組成", "創る", "操縦", "早期アクセス", "装着", "送る",
        "促す", "続ける", "打ち上げる", "打出す", "体験", "体験学習", "対応", "貸与", "題", "達成", "担う", "担当", "探す", "短縮",
        "値上げ", "知る", "注ぐ", "調査", "頂く", "追求", "通す", "定義", "提", "提案", "提案", "徹底", "転用", "伝える", "登録予約",
        "投資", "投入", "統一", "統合", "踏まえる", "得る", "特別サポート", "突破", "入れる", "認める", "発見", "発生", "披露",
        "標準装備", "付ける", "分析", "編み出す", "保つ", "邦銀初", "防ぐ", "磨く", "明らか", "目指す", "目的", "融合", "予測",
        "予定", "余儀なくする", "与える", "預かる", "用いる", "用意", "浴びる", "落札", "利用", "立ち上げる", "立てる", "扱う",
        "虜", "虜になる", "ホームページ制作サービス", "可視化", "花粉飛散予報", "画面塗布サービス", "解析", "兼ね揃える", "見える化",
        "原盤企画及び制作", "出す", "生育データ収集", "生成", "接続", "送付", "即時デリバリーサービス", "添える", "熱源と", "配合",
        "変形", "防止、防汚効果・割れ", "模索", "創出", "普及", "めざし応援", "受注"
    ]

    phrase_rule = [{"label": '<構想・目標>', "words": kousou_dic},
                   {"label": '<研究>', "words": kenkyuu_dic},
                   {"label": '<開発>', "words": kaihatsu_dic},
                   {"label": '<実験>', "words": jikken_dic},
                   {"label": '<製品・サービス化>', "words": seihin_dic},
                   {"label": '<更新>', "words": koushin_dic},
                   {"label": '<中止>', "words": tyuushi_dic},
                   {"label": '<参画>', "words": sankaku_dic},
                   {"label": '<利用>', "words": riyou_dic},
                   {"label": '<組織変更>', "words": soshiki_dic},
                   {"label": '<連携>', "words": renkei_dic},
                   {"label": '<告知>', "words": tsuuchi_dic},
                   {"label": '<手続き>', "words": tetsuzuki_dic},
                   {"label": '<その他>', "words": sonota_dic}
                   ]

    """
    フェーズ処理の対象になる格
    """
    phase_analyze_case = ["を", "に", "について", "などに", "などを", "に対して", "に関して", "までを", "も", "が"]

    """
    時制に関する補助用言
    """
    kako = [""]
    genzai = [""]
    mirai = ["予定", "計画", "目指す"]

    """
    マルチラベルをシングルラベルに変換するルール
    """

    kenkyu = ['<構想・目標>', '<研究>', '<開発>', '<実験>', '<手続き>']
    seihin = ['<製品・サービス化>', '<更新>', '<参画>', '<利用>']
    sonota = ['<中止>', '<参画>', '<利用>', '<組織変更>', '<連携>', '<告知>', '<その他>']

    single_rule = [{"single": '製品化・サービス化', "labels": seihin},
                   {"single": '研究・開発', "labels": kenkyu},
                   {"single": 'その他', "labels": sonota}
                   ]
