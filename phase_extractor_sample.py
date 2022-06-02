from phase_extractor import PhaseExtractor
model = PhaseExtractor() # KeywordExtractorのクラスのインスタンス化

text = '大手スーパーのベイシアは、小型店舗の「ベイシアマート」を除く全店舗で「アセロラ真鯛」の試験販売を始めた。'

phase = model.single_phase_extract(text) # フェーズの判別
print(text, phase)
