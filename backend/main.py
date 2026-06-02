# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from model_inference import DiagnosticModel
# from chatbot_engine import MedicalChatEngine

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# diagnostic_model = DiagnosticModel()
# chat_engine = MedicalChatEngine()

# @app.post("/predict")
# async def predict_image(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     result = diagnostic_model.predict(image_bytes)
#     return result

# @app.post("/chat")
# async def chat_endpoint(
#     message: str = Form(...),
#     diagnosis: str = Form(...),
#     confidence: float = Form(...)
# ):
#     reply = chat_engine.generate_explanation(diagnosis, confidence, message)
#     return {"reply": reply}
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from model_inference import DiagnosticModel
from chatbot_engine import MedicalChatEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to ["http://localhost:5173"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

diagnostic_model = DiagnosticModel()
chat_engine = MedicalChatEngine()

# FIX: Define schemas to accept JSON chat history
class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    history: List[ChatMessage]
    diagnosis: str
    confidence: float

# FIX: Removed 'async' so heavy PyTorch code runs in a background thread
@app.post("/predict")
def predict_image(file: UploadFile = File(...)):
    # file.read() is async, so we use file.file.read() for synchronous endpoints
    image_bytes = file.file.read() 
    result = diagnostic_model.predict(image_bytes)
    return result

# FIX: Changed endpoint to accept a JSON payload rather than Form data
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # Pass the history (as a list of dicts) to the engine
    history_dicts = [{"sender": msg.sender, "text": msg.text} for msg in request.history]
    reply = chat_engine.generate_explanation(
        request.diagnosis, 
        request.confidence, 
        history_dicts
    )
    return {"reply": reply}