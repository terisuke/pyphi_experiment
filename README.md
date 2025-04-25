# PyPhi実験プロジェクト

## 概要
このプロジェクトは、統合情報理論（Integrated Information Theory, IIT）の計算ツールであるPyPhiを使用して、3ノードシステムのφ値（統合情報量）を計算する実験を行います。

## 実験内容
- 2ノードシステム（XORゲート）のφ値計算
- 3ノードシステムのφ値計算
- 異なる状態でのφ値の比較

## 主な成果
- TPM（遷移確率行列）の修正により、すべての状態でφ値が正しく計算できるようになりました
- 状態 `(0, 1, 1)` と `(1, 1, 1)` のφ値が0であることを確認
- システムの各状態において統合された情報が存在しないことを示唆

## 今後の課題
1. 他の状態（例：`(0, 0, 0)`、`(0, 0, 1)`など）のφ値の計算
2. より複雑な相互作用を持つTPMの設計
3. 非ゼロのφ値を持つ状態の作成

## 環境設定
- Python 3.x
- PyPhi 1.2.0
- NumPy 1.24.3

## 使用方法
```bash
# 環境構築
python -m venv pyphi_env
source pyphi_env/bin/activate  # Windows: pyphi_env\Scripts\activate
pip install -r requirements.txt

# 実験実行
python test_pyphi.py
```

## 参考リソース
- [PyPhi公式ドキュメント](https://pyphi.readthedocs.io)
- [PyPhiのGitHubリポジトリ](https://github.com/wmayner/pyphi)

## 環境要件
- macOS
- Anaconda
- Python 3.9
- PyPhi 1.2.0

## 環境構築手順

### 1. Anaconda環境の作成
Python 3.9の新しい環境を作成します：
```bash
conda create -n pyphi_env python=3.9 -y
```

### 2. 環境のアクティベート
```bash
conda activate pyphi_env
```

### 3. PyPhiのインストール
```bash
pip install pyphi
```

### 4. 依存関係の調整
PyPhiはNumPy 2.0.2との互換性に問題があるため、NumPy 1.24.3にダウングレードする必要があります：
```bash
pip uninstall -y numpy && pip install numpy==1.24.3
```

## 発生した問題と解決方法

### NumPy互換性エラー
**問題**：
```
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.0.2 as it may crash.
```

**解決方法**：
- NumPyを1.24.3バージョンにダウングレード
- これによりPyPhiの全機能が正常に動作するようになりました

## 動作確認

`test_pyphi.py`を実行して環境が正しく設定されていることを確認できます：
```bash
python test_pyphi.py
```

正常に動作する場合、以下のような出力が表示されます：
```
PyPhi version: 1.2.0
Network object created successfully:
...
PyPhi seems to be installed and working correctly!
```

## 日常的な使用方法

### 環境の開始
```bash
conda activate pyphi_env
```

### 環境の終了
```bash
conda deactivate
```

## 参考文献
PyPhiを研究で使用する場合は、以下の論文を引用してください：

> Mayner WGP, Marshall W, Albantakis L, Findlay G, Marchman R, Tononi G. (2018). PyPhi: A toolbox for integrated information theory. PLOS Computational Biology 14(7): e1006343. https://doi.org/10.1371/journal.pcbi.1006343

## 追加リソース
- [PyPhi公式ドキュメント](https://pyphi.readthedocs.io)
- [GitHubイシュートラッカー](https://github.com/wmayner/pyphi)
- [PyPhiユーザーグループ](https://groups.google.com/forum/#!forum/pyphi-users) 