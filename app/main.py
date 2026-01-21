from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.ai_model import MockMedicalAI
from app.utils.logger import setup_logger
# DB関連のインポート
from app.db import models
from app.db.database import engine, get_db

# ロガーの準備
logger = setup_logger("medical_api")

# 起動時にデータベースのテーブルを作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Image Analysis API",
    description="AI Analysis System for Medical DX (Optim Selection)",
    version="0.1.0"
)

ai_model = MockMedicalAI()

@app.get("/")
def read_root():
    return {
        "system": "Medical DX API",
        "status": "online",
        "message": "Waiting for X-ray image upload..."
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    画像をアップロードし、AI解析結果を返す & DBに保存する
    """
    logger.info(f"Analysis request received. Filename: {file.filename}")

    if not file.content_type.startswith("image/"):
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # 1. AIモデルで解析
    result = ai_model.analyze(file.filename)

    # 2. 診断結果をデータベースに保存
    try:
        db_log = models.DiagnosisLog(
            filename=result["filename"],
            diagnosis=result["diagnosis"],
            confidence=result["confidence"]
        )
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
    }