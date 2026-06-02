import os

class Settings:
    PROJECT_NAME: str = "AI-Powered Medical Assistant Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # A verified, working medical Vision Transformer (~340 MB)
    VISION_MODEL_NAME: str = "nickmuchi/vit-finetuned-chest-xray-pneumonia"
    NLP_MODEL_NAME: str = "Qwen/Qwen2.5-0.5B-Instruct"

settings = Settings()