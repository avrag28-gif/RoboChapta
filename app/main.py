from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.detector import detect_captcha

app = FastAPI(
    title="RoboChapta QA Lab",
    version="0.1.0",
    description="Safe CAPTCHA classification and human-review handoff for owned test environments.",
)

class DetectRequest(BaseModel):
    type: str = Field(min_length=1, max_length=32)

class ReviewRequest(BaseModel):
    provider: str = Field(min_length=1, max_length=100)
    challenge_id: str = Field(min_length=1, max_length=128)

@app.get("/health")
def health():
    return {"status": "ok", "service": "robochapta-qa-lab"}

@app.post("/detect")
def detect(request: DetectRequest):
    result = detect_captcha({"type": request.type})
    return {
        "type": result.captcha_type.value,
        "confidence": result.confidence,
        "requires_human": result.requires_human,
        "status": "classified",
    }

@app.post("/review")
def review(request: ReviewRequest):
    # Deliberately does not interact with an external CAPTCHA provider.
    return {
        "status": "human_review_required",
        "provider": request.provider,
        "challenge_id": request.challenge_id,
        "next_step": "Complete the provider's official accessible verification flow.",
    }
