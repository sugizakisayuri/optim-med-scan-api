import random
from typing import Dict

class MockMedicalAI:
    def __init__(self):
        # 模擬的な診断ラベル
        self.labels = ["Normal", "Pneumonia", "Covid-19"]

    def analyze(self, filename: str) -> Dict:
        """
        画像を受け取り、ランダムな診断スコアを返す模擬関数
        """
        # ランダムに診断結果を決定
        predicted_label = random.choice(self.labels)
        confidence_score = round(random.uniform(0.7, 0.99), 2)  # 70%~99%の信頼度

        return {
            "filename": filename,
            "diagnosis": predicted_label,
            "confidence": confidence_score,
            "ai_version": "v1.0.0-mock"
        }