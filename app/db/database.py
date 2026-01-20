from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Docker環境変数からDB接続情報を取得
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/medical_db")

# データベースエンジンを作成
engine = create_engine(DATABASE_URL)

# セッション（DBとの会話窓口）を作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テーブルの元となるクラス
Base = declarative_base()

# DBセッションを取得する関数（FastAPIで使う）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()