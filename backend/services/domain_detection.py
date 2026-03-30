def run_domain_detection(full_text):
    try:
        text = full_text.lower()

        # Domain keywords
        if any(word in text for word in ["certificate", "marks", "board", "grade"]):
            domain = "education_certificate"

        elif any(word in text for word in ["government", "id", "dob", "aadhaar", "identity"]):
            domain = "id_card"

        elif any(word in text for word in ["invoice", "amount", "total", "bill"]):
            domain = "invoice"

        else:
            domain = "unknown"

        return {
            "domain": domain
        }

    except Exception as e:
        return {"error": str(e)}