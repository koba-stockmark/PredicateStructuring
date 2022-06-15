from phase_extractor import PhaseExtractor

p_e = PhaseExtractor()  # KeywordExtractorのクラスのインスタンス化

text = '大手スーパーのベイシアは、小型店舗の「ベイシアマート」を除く全店舗で「アセロラ真鯛」の試験販売を始めた。'

phase = p_e.single_phase_extract(text)  # フェーズのチェック
print(phase)
