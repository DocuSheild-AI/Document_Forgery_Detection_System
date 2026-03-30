from fastapi import FastAPI, UploadFile, File
import shutil
import os
import numpy as np

from services.cnn_model import run_efficientnet
from services.copy_move import run_copy_move
from services.ela import run_ela
from services.ocr import run_ocr
from services.text_consistency import run_text_consistency
from services.domain_detection import run_domain_detection
from services.template_matching import run_template_matching
from services.layout_analysis import run_layout_analysis
from services.rule_based_validation import run_rule_based_validation
from services.field_extraction import extract_fields

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    else:
        return obj


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cnn_result = run_efficientnet(file_path)
        copy_move_result = run_copy_move(file_path)
        ela_result = run_ela(file_path)
        ocr_result = run_ocr(file_path)

        text = ocr_result.get("full_text", "")

        text_result = run_text_consistency(text)
        domain_result = run_domain_detection(text)

        template_result = run_template_matching(
            text,
            domain_result.get("domain", "")
        )

        layout_result = run_layout_analysis(
            ocr_result.get("text_detected", [])
        )

        # 🔥 NEW: FIELD EXTRACTION
        fields = extract_fields(text)

        # 🔥 NEW: RULE CHECK USING FIELDS
        rule_result = run_rule_based_validation(
            fields,
            domain_result.get("domain", "")
        )

        # -----------------------------
        # FINAL LOGIC
        # -----------------------------
        if rule_result.get("strong_violation", False):
            final_decision = "Forgery Detected"

        elif copy_move_result.get("clusters", 0) > 10 or ela_result.get("score", 0) > 50:
            final_decision = "Forgery Detected"

        elif template_result.get("suspicious", False) and layout_result.get("suspicious", False):
            final_decision = "Forgery Detected"

        else:
            final_decision = "No Forgery Detected"

        response = {
            "fields_extracted": fields,
            "cnn_result": cnn_result,
            "copy_move": copy_move_result,
            "ela": ela_result,
            "ocr": ocr_result,
            "text_consistency": text_result,
            "domain": domain_result,
            "template_matching": template_result,
            "layout_analysis": layout_result,
            "rule_validation": rule_result,
            "final_decision": final_decision
        }

        return convert_to_serializable(response)

    except Exception as e:
        return {"error": str(e)}