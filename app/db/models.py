from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base

class DiagnosisLog(Base):
<<<<<<< HEAD
    __tablename__ = "diagnosis_logs"
=======
    """
    診断履歴を保存するテーブル
    """
    __tablename__ = "diagnosis_logs"

>>>>>>> origin/main
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    diagnosis = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)