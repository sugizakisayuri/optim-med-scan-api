\# Medical Image Analysis API (Optim Selection)



株式会社オプティム様の選考用ポートフォリオです。

医療DX（遠隔医療・画像診断支援）を想定し、X線画像をアップロードするとAIが解析結果を返すバックエンドシステムを開発しています。

「AI × Human」の協調ワークフローを意識し、AIの推論結果を医師が確認・修正できるプロセスを想定しています。



\## 🚀 技術スタック

\- \*\*Language\*\*: Python 3.9

\- \*\*Framework\*\*: FastAPI (非同期処理による高速化)

\- \*\*Infrastructure\*\*: Docker / Docker Compose

\- \*\*CI/CD\*\*: GitHub Actions (Lint/Test自動化)



\## 📂 ディレクトリ構成

.

├── app/

│   ├── main.py      # APIのエントリーポイント

│   └── models/      # AIモデル（Mock）

├── .github/         # CI/CD設定

├── Dockerfile       # コンテナ定義

└── requirements.txt # 依存ライブラリ



\## 📅 開発ロードマップ

1\. \[x] Docker環境構築 / FastAPIセットアップ

2\. \[ ] 画像アップロード機能の実装

3\. \[ ] 模擬AIモデル（ランダムな診断スコア出力）の実装

4\. \[ ] 監査ログ機能（誰がいつ診断したか）

