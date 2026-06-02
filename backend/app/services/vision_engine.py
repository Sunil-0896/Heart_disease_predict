import io
import torch
from PIL import Image
from transformers import pipeline
from app.config import settings

class VisionEngine:
    def __init__(self):
        self.classifier = None
        self.device = 0 if torch.cuda.is_available() else -1

    def load_model(self):
        """Load the vision model into system memory on startup."""
        if self.classifier is None:
            self.classifier = pipeline(
                "image-classification",
                model=settings.VISION_MODEL_NAME,
                device=self.device
            )

    def analyze_image(self, image_bytes: bytes) -> tuple[str, float]:
        """Process raw image byte-stream and execute inference."""
        if self.classifier is None:
            raise RuntimeError("Vision model components are not loaded. Call load_model() first.")
        
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        raw_results = self.classifier(image)
        
        if not raw_results:
            return "Inconclusive / No features identified", 0.0
            
        top_prediction = raw_results[0]
        return top_prediction['label'], float(top_prediction['score'])

vision_engine = VisionEngine()