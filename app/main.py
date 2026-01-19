from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models.ai_model import MockMedicalAI
from app.utils.logger import setup_logger  # ← 追加: ロガーを読み込み

# ロガーの準備
logger = setup_logger("medical_api")

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
async def analyze_image(file: UploadFile = File(...)):
    """
    X線画像をアップロードし、AI解析結果を返す
    """
    # ★監査ログ: リクエスト受信を記録
    logger.info(f"Analysis request received. Filename: {file.filename}, Content-Type: {file.content_type}")

    # 1. ファイル形式チェック
    if not file.content_type.startswith("image/"):
        logger.warning(f"Invalid file upload attempt: {file.content_type}") # 警告ログ
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # 2. Mock AIモデルで解析
    result = ai_model.analyze(file.filename)

    # ★監査ログ: 解析結果を記録（これがトレーサビリティになります）
    logger.info(f"Analysis completed. Diagnosis: {result['diagnosis']}, Confidence: {result['confidence']}")

    return {
        "status": "success",
        "analysis_result": result
    }