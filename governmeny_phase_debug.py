from government_news_analysis import GovernmentNewsAnalysis

gnp = GovernmentNewsAnalysis()

text = "JISは、鉱工業品、データ、サービスの品質、性能や試験方法などを定めた国家規格であり、社会的環境の変化に対応して、制定・改正しています。また、社会的に関心の高い重要な制定や改正を月に1回紹介しています。"
text = "経済産業省と国土交通省は24日、秋田県沖と千葉県沖の3つの海域で洋上風力発電を担う事業者の公募結果を発表した。"
text = "ウィスコンシン州政府が19日、フォックスコンと税優遇契約の見直しで大筋合意したと発表した。"
text = "韓国政府は外務省内に経済安全保障の専門部署を新設する計画だ。"
text = "国税庁が1日発表した2021年の路線価で、九州7県の標準宅地の評価基準額は前年比0.4%上昇した。"

# 政府活動のチェック
government_phase = gnp.government_phase_extract(text)
#government_phase = gnp.government_action_extract(text)
print(government_phase)