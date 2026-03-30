import easyocr

# Initialize reader (runs once)
reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image_path):
    try:
        # Read text from image
        results = reader.readtext(image_path)

        extracted_text = []

        for (bbox, text, prob) in results:
            extracted_text.append({
                "text": text,
                "confidence": round(prob, 2)
            })

        # Combine all text
        full_text = " ".join([item["text"] for item in extracted_text])

        # Simple logic for suspicious detection
        suspicious = False

        if len(full_text) < 10:
            suspicious = True

        return {
            "text_detected": extracted_text,
            "full_text": full_text,
            "suspicious": suspicious
        }

    except Exception as e:
        return {"error": str(e)}