from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
<<<<<<< HEAD
from typing import List
from app.models.ai_model import MockMedicalAI
from app.utils.logger import setup_logger
# DB関連のインポート
=======
from app.models.ai_model import MockMedicalAI
from app.utils.logger import setup_logger
# ↓ 追加: DB関連のインポート
>>>>>>> origin/main
from app.db import models
from app.db.database import engine, get_db

# ロガーのセットアップ
logger = setup_logger("medical_api")

<<<<<<< HEAD
# 起動時にデータベースのテーブルを作成
=======
# 起動時にデータベースのテーブルを作成（初回のみ）
>>>>>>> origin/main
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Image Analysis API",
    description="AI Analysis System for Medical DX (Optim Selection)",
    version="0.1.0"
)

ai_model = MockMedicalAI()

@app.get("/")
def read_root():
    return {"system": "Medical DX API", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
<<<<<<< HEAD
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    画像をアップロードし、AI解析結果を返す & DBに保存する
=======
async def analyze_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db) # ← 追加: データベースを使う準備
):
    """
    画像をアップロードし、AI解析結果を返す＆DBに保存する
>>>>>>> origin/main
    """
    logger.info(f"Analysis request received. Filename: {file.filename}")

    if not file.content_type.startswith("image/"):
        logger.warning(f"Invalid file type: {file.content_type}")
<<<<<<< HEAD
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # 1. AIモデルで解析
    result = ai_model.analyze(file.filename)

    # 2. 診断結果をデータベースに保存
=======
        raise HTTPException(status_code=400, detail="Invalid file type.")

    # AI診断実行
    result = ai_model.analyze(file.filename)

    # ★ここが新機能: 診断結果をデータベースに保存
>>>>>>> origin/main
    try:
        db_log = models.DiagnosisLog(
            filename=result["filename"],
            diagnosis=result["diagnosis"],
            confidence=result["confidence"]
        )
<<<<<<< HEAD
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        logger.info(f"Saved to DB with ID: {db_log.id}")
    except Exception as e:
        logger.error(f"Database save error: {str(e)}")

    return {
        "status": "success",
        "analysis_result": result,
        "db_record_id": db_log.id
    }

@app.get("/history")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    保存された診断履歴を最新順に取得する
    """
    # データベースから最新順に取得
    logs = db.query(models.DiagnosisLog).order_by(models.DiagnosisLog.created_at.desc()).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(logs),
        "history": logs
=======
        db.add(db_log)     # 保存リストに追加
        db.commit()        # 確定（保存実行）
        db.refresh(db_log) # 保存されたデータを読み直す
        
        logger.info(f"Data saved to DB. ID: {db_log.id}, Diagnosis: {result['diagnosis']}")
    except Exception as e:
        logger.error(f"DB Save Error: {str(e)}")
        # DB保存に失敗しても、診断結果自体はユーザーに返す
    
    return {
        "status": "success",
        "analysis_result": result,
        "db_record_id": db_log.id # 保存されたIDも返す
>>>>>>> origin/main
    }