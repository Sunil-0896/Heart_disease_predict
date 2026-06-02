from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.schemas.chat import AnalysisResponse, ChatRequest, ChatResponse
from app.services.vision_engine import vision_engine
from app.services.nlp_engine import nlp_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hook managing model loading during service startup sequence."""
    print("Initializing Pre-trained AI Models (Vision & NLP Engine)...")
    vision_engine.load_model()
    nlp_engine.load_model()
    print("Model compilation complete. System online.")
    yield
    print("Cleaning resources...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(f"{settings.API_V1_STR}/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_medical_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file encoding format. Please submit JPEG or PNG files."
        )
    try:
        file_bytes = await file.read()
        label, confidence = vision_engine.analyze_image(file_bytes)
        return AnalysisResponse(prediction=label, confidence=confidence)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference Pipeline Error: {str(e)}"
        )

@app.post(f"{settings.API_V1_STR}/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def converse_with_assistant(payload: ChatRequest):
    try:
        reply_text = nlp_engine.generate_response(
            user_message=payload.user_message,
            prediction=payload.prediction_context,
            confidence=payload.confidence_context,
            chat_history=payload.chat_history
        )
        return ChatResponse(reply=reply_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text Generation Pipeline Failure: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)