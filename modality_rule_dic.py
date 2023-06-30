class ModalityRule:

    ################################################
    #   モダリティルール辞書
    #
    #　　　　<断定>, <不確実>, <命令>, <過去>, <否定>, <意思・願望>, <勧誘>, <推量>, <仮定>,
    # 　　　<感情付与>, <容易>, <困難>, <限定>, <当然>, <過剰>, <使役>, <受け身>, <試行>,
    # 　　　<継続>, <経験>, <可能>, <疑問>, <引用>, <目標>, <原因・方法>, <委任>
    # 　　　<こと>, <とは>,
    #
    #      [#] は [norm != orth] が条件でのorth
    #      [%] は [norm == lemma] が条件でのorth
    #      [D] は　タグの削除ルール
    #      [活用=]　は　活用に関する規則
    #      [.*] などの正規表現が可能
    #
    ################################################


    modality_rule = [
        # 断定
        {
            "tag": "<断定>",
            "rule": [
                ["で", "ある"],
                ["です"],
                ["だ"]
            ]
        },
        # 不確実
        {
            "tag": "<不確実>",
            "rule": [
                ["か", "も"]
            ]
        },
        # 命令
        {
            "tag": "<命令>",
            "rule": [
                ["活用=命令形"],
                ["活用=終止形", "な"]
            ]
        },
        # 過去
        {
            "tag": "<過去>",
            "rule": [
                ["て", "い", "た"],
                ["で", "い", "た"],
                ["て", "あっ", "た"],
                ["で", "あっ", "た"],
                ["て", "み", "た"],
                ["で", "み", "た"],
                ["て", "おい", "た"],
                ["で", "おい", "た"],
                ["て", "もらっ", "た"],
                ["で", "もらっ", "た"],
                ["だっ", "た"],
                ["活用=連用形", "た"],
                ["活用=連用形", "だ"]
            ]
        },
        # 否定
        {
            "tag": "<否定>",
            "rule": [
                ["ず"],
                ["ぬ"],
                ["ない"],
                ["なかっ"],
                ["ませ", "ん"],
                ["活用=終止形", "な"],
                ["Dいい", "じゃ", "ない"]  # いいじゃない　は外す
            ]
        },
        # 告知
        {
            "tag": "<告知>",
            "rule": [
                ["ぞ"],
                ["よ"]
            ]
        },
        # 意思
        {
            "tag": "<意思・願望>",
            "rule": [
                ["たい"],
                # ["活用=終止形", "よう"],
                # ["活用=連体形", "よう"],
                ["期待", "する"],
                ["ほしい"]
            ]
        },
        # 勧誘
        {
            "tag": "<勧誘>",
            "rule": [
                ["活用=意志推量形"],
                ["ば", "いい"],
                ["ましょう"],
                ["ください"],
                ["を", "!"],
                ["を", "。"],
                ["を", "$"]
            ]
        },
        # 推量
        {
            "tag": "<推量>",
            "rule": [
                ["か", "も", "しれ", "ない"],
                ["で", "あろう"],
                ["だろう"]
            ]
        },
        # 仮定
        {
            "tag": "<仮定>",
            "rule": [
                ["ば"],
                ["活用=連用形", "たら"]
            ]
        },
        # 感情付与
        {
            "tag": "<感情付与>",
            "rule": [
                ["活用=連体形", "の", "！"],
#                ["POS=NOUN", "！"],
#                ["活用=終止形", "！"],
                ["活用=終止形", "ね"],
                ["活用=終止形", "よ"]
            ]
        },
        # 容易
        {
            "tag": "<容易>",
            "rule": [
                ["やすい"]
            ]
        },
        # 困難
        {
            "tag": "<困難>",
            "rule": [
                ["にくい"]
            ]
        },
        # 限定
        {
            "tag": "<限定>",
            "rule": [
                ["だけ"],
                ["まで"]
            ]
        },
        # 当然
        {
            "tag": "<当然>",
            "rule": [
                ["べから"],
                ["べく"],
                ["べし"],
                ["べき"]
            ]
        },
        # 過剰
        {
            "tag": "<過剰>",
            "rule": [
                [".*すぎる"],
                ["すぎる"]
            ]
        },
        # 使役
        {
            "tag": "<使役>",
            "rule": [
                ["させる"],
                ["活用=サ行変格;未然形-サ", "せ"],
                ["活用=サ行変格;未然形-サ", "せる"]
            ]
        },
        # 委任
        {
            "tag": "<委任>",
            "rule": [
                ["て", "もらう"],
                ["て", "もらっ"]
            ]
        },
        # 受け身
        {
            "tag": "<受け身>",
            "rule": [
                [".*か", "れ"],
                [".*か", "れる"],
                [".*が", "れ"],
                [".*が", "れる"],
                [".*さ", "れ"],
                [".*さ", "れる"],
                [".*ざ", "れ"],
                [".*ざ", "れる"],
                [".*た", "れ"],
                [".*た", "れる"],
                [".*だ", "れ"],
                [".*だ", "れる"],
                [".*な", "れ"],
                [".*な", "れる"],
                [".*は", "れ"],
                [".*は", "れる"],
                [".*ば", "れ"],
                [".*ば", "れる"],
                [".*ま", "れ"],
                [".*ま", "れる"],
                [".*や", "れ"],
                [".*や", "れる"],
                [".*ら", "れ"],
                [".*ら", "れる"],
                [".*わ", "れ"],
                [".*わ", "れる"]
            ]
        },
        # 試行
        {
            "tag": "<試行>",
            "rule": [
                [".*て", "みる"]
            ]
        },
        # 継続
        {
            "tag": "<継続>",
            "rule": [
                [".*て", "いる"]
            ]
        },
        # 方向
        {
            "tag": "<方向>",
            "rule": [
                [".*て", "くる"]
            ]
        },
        # 経験
        {
            "tag": "<経験>",
            "rule": [
                [".*る", "こと", "が"],
                [".*た", "こと", "が"],
                [".*だ", "こと", "が"]
            ]
        },
        # 可能
        {
            "tag": "<可能>",
            "rule": [
                #        ["!する", "れる"],
                ["D.*さ", "#.*れる"],
                ["D.*あ", "ない"],
                ["D.*か", "ない"],
                ["D.*が", "ない"],
                ["D.*さ", "ない"],
                ["D.*ざ", "ない"],
                ["D.*た", "ない"],
                ["D.*だ", "ない"],
                ["D.*な", "ない"],
                ["D.*ば", "ない"],
                ["D.*ま", "ない"],
                ["D.*や", "ない"],
                ["D.*ら", "ない"],
                ["D.*わ", "ない"],
                ["D%.*てる", "ない"],
                ["でき"],
                ["できる"],
                ["でき", "た"],
                ["られる"],
                ["#.*える"],
                ["#.*ける"],
                ["#.*げる"],
                ["#.*せる"],
                ["#.*ぜる"],
                ["#.*てる"],
                ["#.*でる"],
                ["#.*ねる"],
                ["#.*べる"],
                ["#.*める"],
                ["#.*れる"],
                ["#.*え", "ず"],
                ["#.*け", "ず"],
                ["#.*げ", "ず"],
                ["#.*せ", "ず"],
                ["#.*ぜ", "ず"],
                ["#.*て", "ず"],
                ["#.*で", "ず"],
                ["#.*ね", "ず"],
                ["#.*べ", "ず"],
                ["#.*め", "ず"],
                ["#.*れ", "ず"],
                ["活用=未然形", "ない"],
                ["D活用=サ行変格;未然形-サ", "活用=未然形", "ない"]
            ]
        },
        # 疑問
        {
            "tag": "<疑問>",
            "rule": [
                ["の", "か", "。"],
                ["の", "か", "、"],
                ["の", "か", "?"],
                ["の", "か", "("],
                ["の", "か", "$"],
                ["いかに", "?"],
                ["か", "。"],
                ["か", "$"],
                ["か", "?"],
                ["か", "？"],
                ["か", "」"],
                ["は", "?"],
                ["は", "?"],
                ["た", "?"],
                ["だ", "?"],
                [".*", "?"],
                [".*", "!", "?"],
                ["と", "は", "$"],
                ["と", "は", "。"],
                ["だ", "の", "か"],
                ["か", "どう", "か"],
                ["べし", "か"],  # べきか
                ["た", "か"],  # たろうか
                ["だ", "か"],  # だろうか
                ["なぜ", "$"],
                ["なぜ", "?"],
                ["なぜ", "？"],
                ["なぜ", "!"],
                ["なぜ", "！"],
                ["なぜ", "。"]
            ]
        },
        # 引用
        {
            "tag": "<引用>",
            "rule": [
                ["TAG=サ変可能", "より"],
                ["TAG=一般", "より"]
            ]
        },
        # 目標
        {
            "tag": "<目標>",
            "rule": [
                ["に", "。"],
                ["に", "$"],
                ["へ", "。"],
                ["へ", "$"]
            ]
        },
        # 原因・方法
        {
            "tag": "<原因・方法>",
            "rule": [
                ["活用=連体形", "こと", "で"],
                ["活用=連体形", "こと", "に", "よる"],
                ["活用=連体形", "ため"],
                ["活用=終止形", "から"],
                ["活用=連体形", "の", "で"]
            ]
        },
        # こと
        {
            "tag": "<こと>",
            "rule": [
                ["活用=連体形", "こと", "。"],
                ["活用=連体形", "こと", "$"]
            ]
        },
        # とは
        {
            "tag": "<とは>",
            "rule": [
                ["と", "は", "。"],
                ["と", "は", "?"],
                ["と", "は", "？"],
                ["と", "は", "("],
                ["と", "は", "$"]
            ]
        }
    ]
