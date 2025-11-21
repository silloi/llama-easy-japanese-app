# PromptOps - プロンプト最適化

このディレクトリには、Meta Llama PromptOpsを使用して「やさしい日本語翻訳ツール」のシステムプロンプトを最適化するための設定とデータが含まれています。

## 📋 概要

PromptOpsは、既存のプロンプトをLlama 3.3モデル向けに自動最適化するツールです。このツールを使用することで、より高品質な「やさしい日本語」の出力を実現できます。

## 🗂️ ファイル構成

```
promptops/
├── README.md              # このファイル
├── config.yaml           # PromptOps設定ファイル
├── dataset.json          # Few-shot examplesのJSON形式データセット
├── original_prompt.txt   # 現在のシステムプロンプト
├── optimized_prompt.txt  # 最適化後のプロンプト（実行後に生成）
└── results/              # 最適化結果と比較レポート（実行後に生成）
```

## 🚀 セットアップ

### 1. PromptOpsのインストール

**推奨: ソースからのインストール**

```bash
# 新しいconda環境を作成（推奨）
conda create -n prompt-ops python=3.10
conda activate prompt-ops

# PromptOpsをクローンしてインストール
git clone https://github.com/meta-llama/prompt-ops.git
cd prompt-ops
pip install -e .
cd ..
```

### 2. APIキーの設定

`.env`ファイルにGroq APIキーを追加（OpenRouter経由でアクセス可能）:

```bash
# プロジェクトルートの.envファイルに追加
GROQ_API_KEY=your_groq_api_key_here
```

または、OpenRouter APIキーを使用する場合:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 📊 データセット

`dataset.json`には、以下のカテゴリのFew-shot examplesが含まれています：

- 行政文書（在留カード、転入届など）
- 医療情報（発熱、受診手順など）
- 防災情報（地震、電話混雑など）
- 雇用関連（退職手続きなど）
- 住宅関連（賃貸契約など）

各例は`question`（原文）と`answer`（やさしい日本語）のペアで構成されています。

## ⚙️ 設定

`config.yaml`では以下の設定が可能です：

### モデル設定
- 出力モデル: `meta-llama/llama-3.3-70b-instruct`
- 温度: 0.3（安定性重視）
- Max tokens: 1500

### 評価指標
1. **Exact Match** (30%): 完全一致度
2. **Semantic Similarity** (40%): 意味的類似度
3. **Length Similarity** (10%): 長さの類似度
4. **Format Compliance** (20%): フォーマット準拠度

### カスタム指標
- **文の長さ**: 20-30文字が理想的か
- **箇条書き**: 箇条書きが使用されているか
- **振り仮名**: 振り仮名が適切に付けられているか

## 🔄 実行方法

### 基本的な実行

```bash
# promptopsディレクトリに移動
cd promptops

# PromptOpsを実行
prompt-ops migrate --config config.yaml
```

### カスタム設定での実行

```bash
# 特定のイテレーション数で実行
prompt-ops migrate --config config.yaml --iterations 5

# 詳細ログを表示
prompt-ops migrate --config config.yaml --verbose
```

## 📈 結果の確認

実行後、以下のファイルが生成されます：

1. **optimized_prompt.txt**: 最適化されたシステムプロンプト
2. **results/comparison.md**: Before/After比較レポート
3. **results/metrics.json**: 評価指標の詳細データ
4. **optimization.log**: 最適化プロセスのログ

### 比較レポートの例

```markdown
# Prompt Optimization Results

## Original Prompt Performance
- Exact Match: 0.75
- Semantic Similarity: 0.82
- Format Compliance: 0.70

## Optimized Prompt Performance
- Exact Match: 0.85 (+0.10)
- Semantic Similarity: 0.90 (+0.08)
- Format Compliance: 0.88 (+0.18)

## Key Improvements
- より明確な指示構造
- Llama 3.3の会話形式に最適化
- Few-shot examplesの効果的な配置
```

## 🔧 トラブルシューティング

### エラー: "API Key not found"

`.env`ファイルにAPIキーが正しく設定されているか確認してください。

```bash
# 環境変数を確認
echo $GROQ_API_KEY
# または
echo $OPENROUTER_API_KEY
```

### エラー: "Dataset format invalid"

`dataset.json`が正しいJSON形式であることを確認してください。

```bash
# JSONの妥当性を確認
python -m json.tool dataset.json
```

### 最適化が改善しない場合

1. イテレーション数を増やす
2. データセットの例を追加する（現在15例→30-50例推奨）
3. 評価指標の重みを調整する

## 📝 最適化されたプロンプトの適用

最適化が完了したら、以下の手順でメインアプリに適用できます：

1. **結果をレビュー**
```bash
cat optimized_prompt.txt
cat results/comparison.md
```

2. **config.pyを更新**
```python
# config.pyのSYSTEM_PROMPTを更新
SYSTEM_PROMPT = """
[optimized_prompt.txtの内容をコピー]
"""
```

3. **アプリをテスト**
```bash
streamlit run app.py
```

4. **品質を比較**
- サンプルテキストで変換を実行
- 出力品質を評価
- 必要に応じて微調整

## 🎯 最適化の目標

このPromptOps設定の主な目標：

1. **文化庁ガイドライン準拠度の向上**
   - 一文20-30文字の遵守率向上
   - 箇条書きの適切な使用
   - 振り仮名の一貫性向上

2. **Llama 3.3との互換性向上**
   - モデル特有の会話形式に最適化
   - Few-shot learningの効果最大化

3. **出力の安定性向上**
   - より一貫した出力フォーマット
   - エラー率の低減

## 📚 参考資料

- [PromptOps GitHub](https://github.com/meta-llama/prompt-ops)
- [Llama 3.3 Documentation](https://www.llama.com/docs/)
- [文化庁ガイドライン](https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/pdf/92484001_01.pdf)

## 🤝 貢献

最適化の改善提案やバグ報告は、GitHubのIssuesでお願いします。

---

**Note**: PromptOpsは実験的な機能です。最適化結果は必ずレビューし、実際のユースケースでテストしてから本番環境に適用してください。
