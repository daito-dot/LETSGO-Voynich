# 研究チェックポイント（日本語）

最終更新: 2026-09-06（Issue #134 / PR #137 後）

このファイルは日本語で現在地を素早く把握するための要約です。厳密な正本は `STATUS.md`、再開手順はルートの `RESUME.md`、次の順序は `ROADMAP.md` です。

## いま一番強く言えること

ヴォイニッチ写本は解読されていません。

ただし、表面文字列の予測・構築構造はかなり小さい観測可能な規則まで絞れました。

現在の最小像は次です。

1. certain visible space は ZL3b と独立 Takahashi/IT2a の双方で構築・生成上の境界として再現する。
2. 空白内の単位は、直前2つの占有スロットを見る小さい逐次文法で経験在庫の天井近くまで再現できる。
3. 単位間には edit-near recurrence/cache と、より遅い prior-paragraph / causal-prefix family inventory がある。
4. 同じ source line では、直前単位の末尾 raw symbol が次単位の先頭 raw symbol を予測する。
5. この短い raw 文脈は line break を越えると有効ではない。
6. terminal→initial edge の骨格は Currier A/B 双方にあるが、literal conditional table は一つの普遍表ではない。
7. Issue #134 でこの edge を corrected B3 に入れると、以前残っていた flexible residual は凍結済み比較では消えた。

## 基礎結果

### 空白で区切られた単位の内側

- 12スロット残差トポロジー R1 は ZL3b と独立 Takahashi/IT2a で再現する。
- 訓練側だけで選んだ「直前2つの占有スロットを見る逐次文法」（298個の計数確率）で経験在庫の天井近くまで再現できる。
- トークン内部の情報量は、形が約7.0 bit、形＋値で約9.7 bit/token。

したがって、トークン内部に複雑な潜在状態を置く必要は現在の証拠からはない。

### 見えている空白

ZL3b と IT2a の双方で、実際の空白位置は近傍へ1 atomずらした切れ目より明確に良い統計的リセットになる。

certain visible space は**構築・生成上の境界**として再現性がある。ただし自然言語の「単語境界」と証明されたわけではない。

### corrected predictive ladder

source-order 修正後の held-out code length:

- B0 V2: `9.7089061 bit/token`
- B1 local: `9.5943670`
- B2 longer history: `9.5461692`
- B3 + observable line/paragraph state: `9.5172688`

長い履歴の主成分は、細かな長文脈そのものではなく、過去の段落でどの近縁語形ファミリーが活性化していたかという遅い在庫状態です。実際の順序が持つ追加情報もありますが小さいです。

## Issue #118 から #130 まで

### flexible residual は実在した

Issue #118:

- `G_context = +0.0178533 bit/token`
- 5/5 foldで正

この時点では「B3の後にも説明できない系列情報が少し残る」と言えました。

### 短い文脈は同じ行の中だけ有効

Issue #121 で次数を `k=2, alpha=.01` に揃えても残差は残りました。

Issue #123:

- 同じ source line 内で空白を越えて文脈をつなぐ: `+0.0291614 bit/token`、5/5
- line break まで越えてつなぐ: 追加効果 `-0.0185292`、0/5

したがって、短い raw 文脈は同じ行の隣接単位では有効ですが、改行を越えると悪化します。

### flexible model の中身が明示規則になった

Issue #125 では固定 `k=2` の LINECONT2 を次の2要素に完全分解しました。

1. 行頭/行内などの一般的な onset/position: `+0.00889185 bit/token`
2. **直前の可視単位の末尾 raw symbol → 次の可視単位の先頭 raw symbol**: `+0.02026956 bit/token`

EDGE2 と LINECONT2 の token-logp 差は最大 `0.0`。

この範囲では、柔軟な系列モデルが拾っていた情報は観測可能な line position と terminal→initial edge に分解できます。

### Currier A/B では骨格は共通、具体表は同一ではない

Issue #127:

- terminal→initial edge 自体は A/B 両方で有効。
- 強さの scalar は、相手側の identity table を使えば双方向に互換。
- literal conditional table の移植は B→A のみ通る。

Issue #130 では学習量の差を previous-terminal class ごとに揃えました。

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

これは歴史的にBからAが作られたという意味ではありません。

## Issue #134 — residual closure

Issue #134 は、ここまでに確定した観測可能な規則を corrected B3 に入れた後、それでも flexible residual が残るかを事前登録して再測定しました。

### 事前固定した core

- corrected B3
- Issue #125 の line-position/onset + terminal→initial edge
- `k=2, alpha=.01`
- Currier A/B は訓練側に同 regime の previous-terminal table があればそれを使用
- なければ pooled previous-terminal table
- それもなければ pooled `LINE_BODY` onset
- original 5 physical-leaf outer folds
- augmented core の `rho`、challenger の `(k,alpha)`、最終 `w` は inner folds だけで選択

Gate0 は predictive scorer を作る前に通過しました。

### first reveal

- scorer commit: `dbd787a457659b7d833dc06c3931f937031172b8`
- run: `34035108074` — SUCCESS
- artifact: `9990011421`
- result JSON SHA-256: `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`

平均 code length:

- B3: `9.517268842963203 bit/token`
- augmented observable core: `9.451900585480233`
- MIX_RESET: `9.451900585480233`
- MIX_LINE: `9.451900585480233`

augmented core は B3 を平均 `+0.06536825748296984 bit/token` 改善し、5/5 foldすべてで改善しました。

選択された `rho`:

`[0.19, 0.22, 0.20, 0.19, 0.21]`

その後の residual:

`G_residual = [0.0, 0.0, 0.0, 0.0, 0.0] bit/token`

- mean `0.0`
- positive folds `0/5`
- RESET と LINE の両 challenger が全5 foldで最終 `w=0.0`

凍結分類:

> **NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

これは raw RESET と raw LINE が同じという意味ではありません。inner validation が、augmented core の後にはどちらの challenger にも追加の重みを与えなかった、という結果です。

### 何が変わったか

Issue #118 の時点では「B3の外に小さな系列残差がある」でした。

Issue #134 後は、「その残差は、現在までに特定した observable edge を core に入れると、凍結済み challenger family では追加予測力を示さない」に更新されました。

したがって、この residual を理由に latent-state model へ進む根拠はなくなりました。

ただし、ヴォイニッチ写本に潜在状態が一切存在しないと証明したわけではありません。

## 現在の最小モデル

1. **空白**: 構築・生成上の境界
2. **単位内部**: 小さい2次逐次文法
3. **ごく近距離**: edit-near recurrence/cache
4. **同一 source line の隣接**: 行位置効果 + 直前末尾→次先頭 edge
5. **line break**: この短い raw 文脈をリセット
6. **より遅い履歴**: prior-paragraph / causal-prefix family inventory
7. **Currier A/B**: 機構の骨格は共有するが、強さや literal mapping の一部が異なる

このモデルは表面文字列の構築・予測モデルです。歴史的な生成手順や解読結果ではありません。

## 次の一手 — Issue #139

次は latent state ではなく、terminal→initial edge 自体の独立 transcription replication です。

Issue #139 の質問:

> **ZL3bで見つかった同一行の previous-terminal → next-initial architecture は、表現と判定基準を事前固定した Takahashi/IT2a でも再現するか？**

first deliverable は score-free contract です。IT2a の結果を見る前に以下を固定します。

- exact source/version/hash
- physical leaf / source line mapping
- uncertainty/editorial symbol の扱い
- visible certain space の扱い
- outer folds
- target population
- literal symbol representation
- POS2 / EDGE2 responsibility
- smoothing / fallback
- held-out stability rule

primary quantity:

`G_identity_IT2a = bits(POS2) - bits(EDGE2)`

判定は3つだけです。

- `INDEPENDENT EDGE REPLICATION PASSES`
- `INDEPENDENT EDGE REPLICATION FAILS`
- `INVALID INDEPENDENT REPLICATION`

## 解釈の限界

現在の結果から言ってはいけないこと:

- 平文や言語が特定された
- 意味がない
- 特定の暗号方式である
- 空白が自然言語の単語境界である
- Currier の一方が歴史的に他方から派生した
- writing hand が原因である
- 人工文・偽書である
- 潜在状態が絶対に存在しない
- 歴史的な生成アルゴリズムが分かった
- 解読した

現在わかっているのは、**表面文字列の生成・予測構造が小さな観測可能規則へかなり収束し、その規則を入れた後には今回の flexible residual が残らなかった**というところまでです。
