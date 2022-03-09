from modality_get import DependExtractor

txts = [
    "書く。書いた。書く本。書きます。書きました。書こう。書きたい。書ければよい。本を読んだ。部屋がきれいだ。学校だ。学校で勉強した。学校で勉強したかった。太郎が遊ぶ",
    "部屋から見える夜景が美しかった。",
    "立地は悪いが食事が美味しい。",
    "客室露天風呂は大人でも足がのばせてとても広かった。"
]


model = DependExtractor()
for text in txts:
    model.depend_get(text)