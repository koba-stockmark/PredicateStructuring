class SubVerbDic:
    """
    補助用言の辞書
    """

    # NG '発表', '実現', '拡大', '追加','計画'
    sub_verb_dic = ['開始', 'スタート', '始める', '始まる', '始動', '本格始動', '続ける', '終わる', '終る', 'する',
                    '掲げる', '目指す', '達成', '予定', '実施', '行なう', '行う', '進める', '推進', '加速',
                    '強化', '拡充', '活用', 'お知らせ', '決定', '記念',
                    '発表', '報ずる', '検討', '公開', '図る', 'いたす', 'いただく', '目的とする', '目標とする', '示す',
                    '乗り出す', '乗りだす', '着手', '取り組む', '参加', '公表', '成功', 'めどを付ける', '分かる', '出来る'
                    ]

    """
    主述部の場合はフェーズと判断していよい補助用言
    """
    special_sub_verb_dic = ['目指す', '目的とする', '目標とする']
