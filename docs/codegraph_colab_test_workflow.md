# CodeGraph Colab Test Workflow

この手順は、Colab 側では notebook の変更を保存せず、セルを実行するだけで
CodeGraph の IrealKG 証拠基盤としての有用性を確認するためのもの。

GitHub から開けるノートブック:

```text
notebooks/codegraph_colab_test.ipynb
```

Colab のメニューでは「ファイル」->「ノートブックを開く」->「GitHub」で
`KazuhTAKEH/-knowledge-state-reviewer` を指定し、
`notebooks/codegraph_colab_test.ipynb` を選ぶ。

## 目的

CodeGraph を教育概念判定器として使うのではなく、次を確認する。

```text
sample code
  -> CodeGraph local index
  -> search / callers / callees / impact / status
  -> code evidence
  -> CodeOntology-like structure
  -> local_thesis-style educational concept alignment
```

検査する教育概念候補は、まず `loop`, `condition`, `function_call` とする。

## Colab で実行するセル

### 1. リポジトリ取得

```python
!rm -rf /content/-knowledge-state-reviewer
!git clone https://github.com/KazuhTAKEH/-knowledge-state-reviewer.git /content/-knowledge-state-reviewer
%cd /content/-knowledge-state-reviewer
```

### 2. CodeGraph テスト実行

```python
!PYTHONIOENCODING=utf-8 python scripts/run_codegraph_colab_test.py --install
```

出力:

```text
colab_outputs/latest_codegraph_test.json
colab_outputs/latest_codegraph_test.md
```

### 3. 結果をGitHubへpush

Colab の Secrets に `GITHUB_TOKEN` を入れてから実行する。

```python
from google.colab import userdata
import os

token = userdata.get("GITHUB_TOKEN")
assert token, "Colab Secrets に GITHUB_TOKEN を設定してください。"

repo = "KazuhTAKEH/-knowledge-state-reviewer"
os.environ["GIT_AUTHOR_NAME"] = "Colab CodeGraph Test"
os.environ["GIT_AUTHOR_EMAIL"] = "colab-codegraph-test@example.invalid"
os.environ["GIT_COMMITTER_NAME"] = os.environ["GIT_AUTHOR_NAME"]
os.environ["GIT_COMMITTER_EMAIL"] = os.environ["GIT_AUTHOR_EMAIL"]
os.environ["GITHUB_TOKEN"] = token

!git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/{repo}.git
!git add -f colab_outputs/latest_codegraph_test.json colab_outputs/latest_codegraph_test.md
!git commit -m "Add latest CodeGraph Colab test output" || echo "No changes to commit"
!git push origin HEAD:main
```

## Codex 側の確認

ユーザが push cell を実行した後、Codex は GitHub から pull して
次を確認する。

```text
colab_outputs/latest_codegraph_test.json
colab_outputs/latest_codegraph_test.md
```

見る観点:

| criterion | meaning |
|---|---|
| structural coverage | サンプル中の関数・構造を検索できるか |
| queryability | `status`, `query`, `callers`, `callees`, `impact` が実行できるか |
| source traceability | 結果からファイル・行・コード断片へ戻れるか |
| educational mappability | `loop`, `condition`, `function_call` へ接続できる証拠があるか |

## 注意

- Colab 側で notebook ファイルは保存しない。
- CodeGraph は刊行論文ではなく OSS 実装として評価する。
- CodeGraph 出力を IrealKG の教育概念として直接採用しない。
- CodeOntology-like な構造語彙と local_thesis-style な概念正規化で解釈する。
