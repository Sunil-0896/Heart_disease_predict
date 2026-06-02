import torch
from transformers import pipeline
from app.config import settings

class NlpEngine:
    def __init__(self):
        self.generator = None
        self.device = 0 if torch.cuda.is_available() else -1

    def load_model(self):
        """Load the text generation transformer into system memory."""
        if self.generator is None:
            self.generator = pipeline(
                "text-generation",
                model=settings.NLP_MODEL_NAME,
                device=self.device,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
            )

    def generate_response(self, user_message: str, prediction: str, confidence: float, chat_history: list) -> str:
        """Constructs context-injected template and processes text generation tokens."""
        if self.generator is None:
            raise RuntimeError("NLP model components are not loaded. Call load_model() first.")

        system_instructions = (
            "You are an advanced, deeply empathetic AI medical assistant specialized in clinical triage. "
            f"An image scan from this patient was analyzed by a vision engine, detecting '{prediction}' "
            f"with a confidence score of {confidence * 100:.1f}%.\n\n"
            "CRITICAL PROTOCOLS:\n"
            "1. You do not possess final medical diagnostic authority. Treat this finding as a preliminary triage indicator.\n"
            "2. Explicitly and smoothly advise the patient to seek professional consultation with a qualified physician.\n"
            "3. Answer the user's questions scientifically, explaining medical terminology in clear, straightforward prose.\n"
            "4. Maintain a supportive, reassuring, and completely calm demeanor."
        )

        messages = [{"role": "system", "content": system_instructions}]
        
        for message in chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
            
        messages.append({"role": "user", "content": user_message})

        outputs = self.generator(
            messages,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.3,
            top_p=0.9
        )
        
        generated_payload = outputs[0]["generated_text"]
        if isinstance(generated_payload, list):
            return generated_payload[-1]["content"]
        return generated_payload

nlp_engine = NlpEngine()