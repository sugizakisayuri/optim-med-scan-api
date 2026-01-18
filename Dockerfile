# Pythonの軽量版イメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# サーバーを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]