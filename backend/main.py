from fastapi import FastAPI, UploadFile, File
import shutil
import os

# Import models
from services.cnn_model import run_efficientnet
from services.copy_move import run_copy_move
from services.ela import run_ela
from services.ocr import run_ocr
from services.text_consistency import run_text_consistency

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # RUN ALL MODELS
        # -----------------------------
        cnn_result = run_efficientnet(file_path)
        copy_move_result = run_copy_move(file_path)
        ela_result = run_ela(file_path)
        ocr_result = run_ocr(file_path)
        text_result = run_text_consistency(ocr_result.get("full_text", ""))

        # -----------------------------
        # IMPROVED DECISION LOGIC
        # -----------------------------
        suspicion_score = 0

        # Strong signals
        if copy_move_result.get("clusters", 0) > 5:
            suspicion_score += 2

        if ela_result.get("score", 0) > 25:
            suspicion_score += 2

        # Weak signals
        if ocr_result.get("suspicious", False):
            suspicion_score += 1

        if text_result.get("suspicious", False):
            suspicion_score += 1

        # Final decision
        if suspicion_score >= 3:
            final_decision = "Forgery Detected"
        else:
            final_decision = "No Forgery Detected"

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------
        return {
            "filename": file.filename,
            "cnn_result": cnn_result,
            "copy_move": copy_move_result,
            "ela": ela_result,
            "ocr": ocr_result,
            "text_consistency": text_result,
            "suspicion_score": suspicion_score,
            "final_decision": final_decision
        }

    except Exception as e:
        return {"error": str(e)}