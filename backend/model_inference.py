# 
import io
from PIL import Image
import torch
from transformers import ViTImageProcessor, ViTForImageClassification

class DiagnosticModel:
    def __init__(self):
        self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
        self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
        self.labels = ["NORMAL", "CARDIOMEGALY", "ARRHYTHMIA"]
        
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Linear(num_features, len(self.labels))
        
        # FIX: Load your trained weights so the model isn't outputting random noise.
        # Uncomment and update the path once you have trained your model.
        # self.model.load_state_dict(torch.load("path_to_your_finetuned_weights.pt"))
        
        self.model.eval()

    def predict(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
            
        top_idx = torch.argmax(probabilities).item()
        
        return {
            "prediction": self.labels[top_idx],
            "confidence": float(probabilities[top_idx]),
            "all_probabilities": {self.labels[i]: float(probabilities[i]) for i in range(len(self.labels))}
        }