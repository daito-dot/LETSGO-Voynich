# 研究チェックポイント（日本語）

最終更新: 2026-09-06（Issue #130 / PR #132 後）

このファイルは日本語で現在地を素早く把握するための要約です。厳密な正本は `STATUS.md`、再開手順はルートの `RESUME.md`、次の順序は `ROADMAP.md` です。

## いま一番強く言えること

ヴォイニッチ写本は解読されていません。

ただし、文字列の**作られ方の構造**はかなり小さな規則まで絞れています。

### 1. 空白で区切られた単位の内側

- 12スロット残差トポロジー R1 は ZL3b と独立 Takahashi/IT2a で再現する。
- 訓練側だけで選んだ「直前2つの占有スロットを見る逐次文法」（298個の計数確率）で経験在庫の天井近くまで再現できる。
- トークン内部の情報量は、形が約7.0 bit、形＋値で約9.7 bit/token。
- したがって、トークン内部に複雑な潜在状態を置く必要は現在の証拠からはない。

### 2. 見えている空白

ZL3b と IT2a の双方で、実際の空白位置は近傍へ1 atomずらした切れ目より明確に良い統計的リセットになる。

したがって、certain visible space は**構築・生成上の境界**として再現性がある。

ただし、自然言語の「単語境界」と証明されたわけではない。

### 3. 単位どうしの関係

source-order 修正後の held-out code length は:

- B0 V2: `9.7089061 bit/token`
- B1 local: `9.5943670`
- B2 longer history: `9.5461692`
- B3 + observable line/paragraph state: `9.5172688`

長い履歴の主成分は、細かな長文脈そのものではなく、過去の段落でどの近縁語形ファミリーが活性化していたかという**遅い在庫状態**。実際の順序が持つ追加情報はあるが小さい。

## Issue #118 以降で何が分かったか

B3 の後にも柔軟な byte 文脈が `+0.0178533 bit/token` 改善し、5/5 foldで正だった。

最初は「まだ説明できない系列情報がある」とだけ言えたが、その後の L1–L4b でかなり局在した。

### L1 — 同じ次数でも残る

RESET2 と CONT2 を同じ `k=2, alpha=.01` に固定しても、境界越し文脈の差は平均 `+0.0106322 bit/token`、5/5。

### L2 — 行の中だけが有効

- 空白を越えて同じ source line 内で文脈をつなぐ: `+0.0291614 bit/token`、5/5。
- line break まで越えてつなぐ: 追加効果 `-0.0185292`、0/5。

つまり短い raw 文脈は**同じ行の隣接単位**では有効だが、改行を越えるとむしろ悪化する。

### L3 — 柔軟モデルの中身が明示規則になった

固定 `k=2` の LINECONT2 は、次の2要素に完全分解できた。

1. 行頭/行内などの一般的な onset/position: `+0.00889185 bit/token`
2. **直前の可視単位の末尾 raw symbol → 次の可視単位の先頭 raw symbol**: `+0.02026956 bit/token`

EDGE2 と LINECONT2 の token-logp 差は最大 `0.0`。

つまり、この範囲では「柔軟な系列モデルが何か複雑な隠れ文脈を拾っている」のではなく、**行内の直前末尾→次先頭という観測可能な隣接規則**で説明できる。

### L4 / L4b — Currier A/B では規則の形は共通、具体表は同一ではない

Issue #127:

- この terminal→initial edge 自体は A/B 両方で有効。
- 強さの scalar は、相手側の identity table を使えば双方向に互換。
- しかし literal conditional table の移植は B→A のみ通る。

B の学習量が A の約2倍だったため、Issue #130 で previous-terminal class ごとに完全に学習量を揃えた。

各 seed で:

- A 8,728 edge events
- B 8,728 edge events
- 共通20 terminal classesごとに選択数を完全一致
- outcomeを見ない5種類の deterministic selection

それでも:

- A→B: seed PASS `0/5`、grand mean `+0.00693954` → FAIL
- B→A: seed PASS `5/5`、grand mean `+0.02697082` → PASS

凍結分類:

> **MATCHED_TABLE_TRANSPORT: B→A ONLY**

したがって、この非対称性を「Bのサンプルが多かっただけ」とは説明できない。

ただし、これは歴史的に B から A が作られた、A が B の部分集合である、といった主張ではない。

## 現在の最小モデル

いまの証拠を一番小さくまとめると:

1. **空白**: 構築・生成上の境界
2. **単位内部**: 小さい2次逐次文法
3. **ごく近距離**: edit-near recurrence/cache
4. **同一 source line の隣接**: 行位置効果 + 直前末尾→次先頭 edge
5. **line break**: この短い raw 文脈をリセット
6. **より遅い履歴**: prior-paragraph / causal-prefix family inventory
7. **Currier A/B**: 機構の骨格は共有するが、強さや literal mapping の一部が異なる

以前の「説明できない flexible sequence residual」は、かなりの部分がこの観測可能な規則へ縮退した。

## 次の一手

次は latent state を足すのではない。

**corrected B3 + line position + explicit terminal→initial edge** を新しい observable core として事前固定し、その上でまだ flexible residual が残るかをもう一度 held-out で測る。

Currier A/B の literal table が同一ではないことは #130 で分かったので、A/B table policy と unknown/other fallback を scoring 前に固定する。

判定:

- residual が消える / 安定性ゲートを落ちる → 潜在状態は不要。現在の観測可能な多階層規則を統合する。
- residual が残る → さらに observable/support/representation を局在してから、初めて latent-state challenger を検討する。

その後の高価値な独立確認は、terminal→initial edge 自体の IT2a/Takahashi replication。

## 解釈の限界

現在の結果から言ってはいけないこと:

- 平文や言語が特定された
- 意味がない
- 特定の暗号方式である
- 空白が自然言語の単語境界である
- Currier の一方が歴史的に他方から派生した
- writing hand が原因である
- 人工文・偽書である
- 歴史的な生成アルゴリズムが分かった
- 解読した

今わかっているのは、**表面文字列の生成・予測構造がかなり小さな観測可能規則まで絞れてきた**という段階です。