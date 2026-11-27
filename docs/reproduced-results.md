# 再検証結果（2026-11-27）

以下は初期実装をローカルの Python で実行した結果。以前の50万等の計算記録は引き継がない。

## テスト

    python3 -m unittest discover -s tests -v

7件成功: 既知の合同式排除、部分群生成の照合、局所合同式、法29の条件、小さい底の検査、二分探索、少数の指数での探索。

## 局所計算

    python3 scripts/verify.py local7

28 unit witnesses; N mod 49 = 1

q<1000 かつ q≡1 mod7 の全28素数について三座標が単元の合同式解を生成・再検査。

## 指数の合同式排除

    python3 scripts/verify.py sieve --bound 10000 --max-k 200

    bound=10000 max_k=200; excluded=1222 remaining=[7, 19, 31, 67, 317]

出力は各排除指数に対する補助素数を含む（全1223行）。これは底の大小を問わない排除。ただし p>10000 を対象としない。

## 最小の底を上限とする探索

    python3 scripts/verify.py search --bound 1000 --max-k 200

    bound=1000 max_k=200; excluded=161 remaining=[7, 19, 31, 67, 317]
    p=7: 7555 divisor candidates, solution=None
    p=19: 6006 divisor candidates, solution=None
    p=31: 5271 divisor candidates, solution=None
    p=67: 4114 divisor candidates, solution=None
    p=317: 1765 divisor candidates, solution=None
    No solution with min(|a|,|b|,|c|) <= 1000; not a global proof.

探索の完全性は docs/mathematics.md の第2・3節に依存する。
最大の底について探索上限を仮定していない。

## Lean

Lean/mathlib は実行環境に存在せず、今回コンパイルしていない。
再現手順（elan と git が導入済みであることを前提とする）:

    lake update
    lake exe cache get
    lake env lean Problem114514.lean

ツールチェーンは既存の安定版 v4.19.0 に固定する方針としたが、依存関係の取得とビルドは未検証。native_decide は信頼された実行機構を使用する。数学的な完全解答は未達成。
