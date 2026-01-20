from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.ai_model import MockMedicalAI
from app.utils.logger import setup_logger
# ↓ 追加: DB関連のインポート
from app.db import models
from app.db.database import engine, get_db

# ロガーのセットアップ
logger = setup_logger("medical_api")

# 起動時にデータベースのテーブルを作成（初回のみ）
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
async def analyze_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db) # ← 追加: データベースを使う準備
):
    """
    画像をアップロードし、AI解析結果を返す＆DBに保存する
    """
    logger.info(f"Analysis request received. Filename: {file.filename}")

    if not file.content_type.startswith("image/"):
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type.")

    # AI診断実行
    result = ai_model.analyze(file.filename)

    # ★ここが新機能: 診断結果をデータベースに保存
    try:
        db_log = models.DiagnosisLog(
            filename=result["filename"],
            diagnosis=result["diagnosis"],
            confidence=result["confidence"]
        )
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
    }