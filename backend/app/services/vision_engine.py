import io
import torch
from PIL import Image
from transformers import pipeline
from app.config import settings

class VisionEngine:
    def __init__(self):
        self.xray_classifier = None
        self.ecg_classifier = None
        self.device = 0 if torch.cuda.is_available() else -1

    def load_models(self):
        # print("Loading X-Ray Engine...")
        self.xray_classifier = pipeline("image-classification", model=settings.XRAY_MODEL_NAME, device=self.device)
        # print("Loading ECG Engine...")
        self.ecg_classifier = pipeline("image-classification", model=settings.ECG_MODEL_NAME, device=self.device)

    def analyze_image(self, image_bytes: bytes, scan_type: str) -> tuple[str, float]:
        """Routes the image to the correct AI model based on scan_type."""
        if self.xray_classifier is None or self.ecg_classifier is None:
            raise RuntimeError("Vision models are not loaded. Call load_models() first.")
        
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Route to the correct mathematical model depends whteher ift he uploaded is xray or ecg
        if scan_type == "xray":
            raw_results = self.xray_classifier(image, top_k=None)
        elif scan_type == "ecg":
            raw_results = self.ecg_classifier(image, top_k=None)
        else:
            raise ValueError(f"Unknown scan type requested: {scan_type}")
            
        top_prediction = raw_results[0]
        label = top_prediction['label']
        confidence = float(top_prediction['score'])

        # Confidence Threshold, to reject less sure predictoins
        if confidence < 0.85:
            return f"Unclear {scan_type.upper()} Scan - Please upload a clearer image.", confidence
            
        return label, confidence

vision_engine = VisionEngine()
