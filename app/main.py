from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models.ai_model import MockMedicalAI

app = FastAPI(
    title="Medical Image Analysis API",
    description="AI Analysis System for Medical DX (Optim Selection)",
    version="0.1.0"
)

# AIモデルの準備
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
    画像をアップロードし、AI解析結果を返す
    """
    # 1. ファイル形式チェック（画像以外はエラーにする）
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # 2. Mock AIモデルで解析
    result = ai_model.analyze(file.filename)

    # 3. 結果を返す
    return {
        "status": "success",
        "analysis_result": result
    }