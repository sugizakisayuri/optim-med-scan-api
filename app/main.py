from fastapi import FastAPI

app = FastAPI(
    title="Medical Image Analysis API",
    description="AI Analysis System for Medical DX (Optim Selection)",
    version="0.1.0"
)

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