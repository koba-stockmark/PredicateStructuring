from phase_extractor import PhaseExtractor
from government_news_analysis import GovernmentNewsAnalysis

p_e = PhaseExtractor()
gnp = GovernmentNewsAnalysis()

text = '大手スーパーのベイシアは、小型店舗の「ベイシアマート」を除く全店舗で「アセロラ真鯛」の試験販売を始めた。'
text2 = '文部科学省、厚生労働省及び経済産業省は、「人を対象とする生命科学・医学系研究に関する倫理指針」を一部改正し、本日（3月10日）の官報にて告示しましたので、お知らせします。。'


# 商品化フェーズのチェック
phase = p_e.single_phase_extract(text)
print(phase)

# 政府活動のチェック
government_phase = gnp.government_phase_extract(text2)
print(government_phase)

# 政府ニュースのチェック
gnp.government_news_analysis("sample_input.json")
with open("news_out.json") as f:
    print(f.read())
